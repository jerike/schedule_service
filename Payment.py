from sqlalchemy import *
from database  import *
from sqlalchemy.orm import relationship, backref 
from sqlalchemy.types import UserDefinedType
import datetime
import decimal



class PackagePayment(Base):
    __tablename__ = 'db_package_payment'
    payment_id = Column('payment_id',Integer, primary_key=True)
    payment_no = Column('payment_no',String(20))
    invoice_id = Column('invoice_id',Integer)
    assign_ts = Column('assign_ts',Date)
    trade_id = Column('trade_id',Integer)
    card_number = Column('card_number',String(20))
    order_number = Column('order_number',String(20))
    order_pay_no = Column('order_pay_no',String(50))
    ref_number = Column('ref_number',String(64))
    is_agreement = Column('is_agreement',Integer)
    pay_day = Column('pay_day',Date)
    period = Column('period',Integer)
    payment_name = Column('payment_name',String(100))
    payment_note = Column('payment_note',String(4000))
    location_id = Column('location_id',Integer)
    staff_id = Column('staff_id',Integer)
    payment_category = Column('payment_category',String(20))
    payment_ts = Column('payment_ts',Date)
    payment_amount = Column('payment_amount',Integer)
    payment_discount = Column('payment_discount',Integer)
    payment_price = Column('payment_price',Integer)
    sno_id = Column('sno_id',Integer)
    merchant_id = Column('merchant_id',String(32))
    payment_provider = Column('payment_provider',String(100))
    payment_mode = Column('payment_mode',String(20))
    refund_id = Column('refund_id',String(20))
    refund_ts = Column('refund_ts',Date)
    refund_amount = Column('refund_amount',Integer)
    refund_mode = Column('refund_mode',String(20))
    refund_reason = Column('refund_reason',String(20))
    meta = Column('meta',Text)
    is_fail = Column('is_fail',Integer)
    bankres_code = Column('bankres_code',String(10))
    batch_id = Column('batch_id',Integer)
    pending_refund = Column('pending_refund',Integer)
    status = Column('status',String(20))
    approve_member_id = Column('approve_member_id',Integer)
    state = Column('state',String(20))
    alter_ts = Column('alter_ts',Date)
    build_ts = Column('build_ts',Date)