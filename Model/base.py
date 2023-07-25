from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer

from database import SMaster

@as_declarative()
class Base(object):

    
    @declared_attr
    def __tablename__(cls) -> str:
        # 將 table 名稱改成小寫
        return cls.__name__.lower()

    # 默认字段
    id = Column(Integer, primary_key=True, index=True)


    def __repr__(self) -> str:
        values = ", ".join("%s=%r" % (n, getattr(self, n)) for n in self.__table__.c.keys())
        print(values)
        return "%s(%s)" % (self.__class__.__name__, values)


    @classmethod
    def query(cls, db: Session = SMaster()):
        return db.query(cls).filter_by(deleted=False) if hasattr(cls, "deleted") else db.query(cls)

    @classmethod
    def create(cls, db: Session = SMaster(), **kw):
        obj = cls(**kw)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def save(self, db: Session = SMaster()):
        db.add(self)
        db.commit()
        db.refresh(self)

    @classmethod
    def checkCount(cls, db: Session = SMaster(), **kw):
        sql = cls.query(db).filter_by(**kw)

        return sql.count()

    @classmethod
    def get_by(cls, db: Session = SMaster(), **kw):
        sql = cls.query(db).filter_by(**kw)
        return sql.first()

    @classmethod
    def get_or_create(cls, db: Session = SMaster(), **kw):
        obj = cls.get_by(db, **kw)
        if not obj:
            obj = cls.create(db, **kw)
        return obj

    @classmethod
    def get_or_404(cls, db: Session = SMaster(), **kw):
        obj = cls.get_by(db, **kw)
        if not obj:
            return 404
        return obj

    @classmethod
    def filter_by(cls, db: Session = SMaster(), **kw):
        return cls.query(db).filter_by(**kw).all()

    @classmethod
    def all(cls, db: Session = SMaster()):
        return cls.query(db).all()

    @classmethod
    def update_by(cls, db: Session = SMaster(), *, user_id: int, update_fields: dict):
        cls.query(db).filter_by(id=user_id).update(update_fields)
        db.commit()

    @classmethod
    def delete_by(cls, db: Session = SMaster(),  *, user_id: int):
        cls.query(db).filter_by(id=user_id).delete(synchronize_session=False)
        db.commit()

    def delete(self, db: Session = SMaster()):
        db.delete(self)
        db.commit()
