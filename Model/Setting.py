from sqlalchemy import *
from database  import *
from sqlalchemy.orm import relationship, backref 
from sqlalchemy.types import UserDefinedType
import datetime
import decimal


class Job(Base):
	__tablename__ = 'job'
	__table_args__ = {'schema': 'scheduler'}
	id=Column('id',Integer, primary_key=True)
	cron_expression=Column('cron_expression',String(20))
	api_path=Column('api_path',String(200))
	api_method=Column('api_method',String(20))
	description=Column('description',String(100))
	state=Column('state',String(20))
	update_date=Column('update_date',Date)


class JobLog(Base):
	__tablename__ = 'job_log'
	__table_args__ = {'schema': 'scheduler'}
	id=Column('id',Integer, primary_key=True)
	job_id=Column('job_id',Integer)
	msg=Column('msg',Text)
	execute_time=Column('execute_time',Date)

