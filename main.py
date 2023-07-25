from fastapi import FastAPI,Request,Header,APIRouter, Depends, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from pytz import utc
import datetime
import json
from database import SMaster
from Model.Setting import *
from traceback import format_tb
import collections 
import requests, pickle
app = FastAPI()


scheduled_jobs_map = {}

def RunTest():
	print('test')
	return {"status":"success","msg":"test"}

def schedule_jobs(scheduler):
	# 取得所有排程
    jobs = getSchedules()

    for job in jobs: 
        add_job_if_applicable(job, scheduler)

    print("refreshed scheduled jobs")

# 取得所有排程
def getSchedules():
	try: 
		# 從資料表 Job 取得排程設定
		Session = SMaster()
		rows = Session.query(Job).filter(Job.state=='run').all()
		Session.close()
		schedules = []
		for r in rows:
			jobs=collections.OrderedDict()
			jobs['id'] = r.id
			jobs["cron_expression"] = r.cron_expression
			jobs["api_path"] = r.api_path
			jobs["api_method"] = r.api_method
			jobs["update_date"] = r.update_date
			schedules.append(jobs)
		print(schedules)
		return schedules 

	except Exception as error:
		print(str(error))

# 增加排程應用
def add_job_if_applicable(job, scheduler): 

	job_id = str(job['id'])
	# 如果排程沒有在表列中，則新增
	if (job_id not in scheduled_jobs_map):
		scheduled_jobs_map[job_id] = job
		scheduler.add_job(lambda: execute_job(job), CronTrigger.from_crontab(job['cron_expression'], timezone='Asia/Taipei'), id=job_id)

		print("added job with id: " + str(job_id))
	# 如果已存在，則判斷是否更新
	else:
		# 取得排程表中的更新時間點
		last_date = scheduled_jobs_map[job_id]['update_date']
		# 目前排程的最後更新時間點
		update_date = job['update_date']
		# 如果排程時間點不同，則覆蓋原設定
		if (update_date != last_date):
			scheduled_jobs_map[job_id]['update_date'] = update_date
			scheduler.remove_job(job_id)
			scheduler.add_job(lambda: execute_job(job), CronTrigger.from_crontab(job['cron_expression'], timezone='Asia/Taipei'), id=job_id)
			print("updated job with id: " + str(job_id))


def execute_job(job):
	print("executing job with id: " + str(job['id']))
	print(datetime.datetime.now())
	if job['api_method'] == "GET":
		result = requests.get(job['api_path'],allow_redirects=False,timeout=10)
		saveJobLog(job,result.text)
	elif job['api_method'] == "POST":
		result = requests.post(job['api_path'],allow_redirects=False,timeout=10)
		saveJobLog(job,result.text)
	elif job['api_method'] == "PUT":
		result = requests.put(job['api_path'],allow_redirects=False,timeout=10)	
		saveJobLog(job,result.text)
	elif job['api_method'] == "PATCH":
		result = requests.patch(job['api_path'],allow_redirects=False,timeout=10)
		saveJobLog(job,result.text)
	elif job['api_method'] == "DELETE":
		result = requests.delete(job['api_path'],allow_redirects=False,timeout=10)
		saveJobLog(job,result.text)
	elif job['api_method'] == "LOCAL":
		result = eval(job['api_path']+"()")
		print(result)
		saveJobLog(job,result)

def saveJobLog(job,result):
	insert_log = JobLog(
		job_id=job['id'],
		msg=str(result),
		execute_time=datetime.datetime.utcnow()
	)
	Session = SMaster()
	Session.add(insert_log)
	Session.commit()
	Session.close()


#####################################################
# 執行 Schedler
#####################################################
scheduler = BackgroundScheduler(timezone="Asia/Taipei")
scheduler.add_job(lambda: schedule_jobs(scheduler), 'interval', seconds=10, next_run_time=datetime.datetime.now(), id='scheduler-job-id')
scheduler.start()


if __name__ == '__main__':
	import uvicorn
	uvicorn.run(app, host='0.0.0.0', port=2222)
