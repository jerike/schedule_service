from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from typing import Generator
import os,sys
import logging
import pymysql
import datetime
pymysql.install_as_MySQLdb()

app = FastAPI()

scheduler = None

log_filename = datetime.datetime.now().strftime("error-%Y-%m-%d_%H.log")
logging.basicConfig(level=logging.DEBUG,filename="system_log/"+log_filename, filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    )
 

load_dotenv()

DB_MASTER_USERNAME=os.getenv('RDS_USERNAME','root')
DB_MASTER_PASSWORD=os.getenv('RDS_PASSWORD','root')
DB_MASTER_HOST=os.getenv('RDS_HOSTNAME','fitbutler-instance-1.cqentfgcpvxw.ap-east-1.rds.amazonaws.com')
DB_MASTER_PORT=os.getenv('RDS_PORT','3306')
DB_MASTER_NAME=os.getenv('RDS_DB_NAME','fitbutler')


DB_MASTER_ADDR='mysql+pymysql://'+DB_MASTER_USERNAME+':'+DB_MASTER_PASSWORD+'@'+DB_MASTER_HOST+':'+DB_MASTER_PORT+'/'+DB_MASTER_NAME+'?charset=utf8mb4'

master = create_engine(DB_MASTER_ADDR, connect_args={'connect_timeout': 5},max_overflow=10,pool_size=50,pool_timeout=900,pool_recycle=600, pool_pre_ping=True) 
SMaster = sessionmaker(autocommit=False,autoflush=False,bind=master)
# print(DB_MASTER_ADDR)
# print(master)
Base = declarative_base()



def get_db() -> Generator:
    """
    每次請求處理完畢後會關閉目前連結，不同請求創建不同的連結
    """
    try:
        db = SMaster()
        yield db
    finally:
        db.close()
