#gunicorn -c gunicorn.conf.py main:app -k uvicorn.workers.UvicornWorker --daemon

import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing
bind = '0.0.0.0:2222'      
backlog = 512                
timeout = 120      
debug = True
workers = 1
worker_class = 'gevent' 
thread = 1
loglevel = 'error' 
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'    
reload = False
errorlog = '-'
accesslog = '-'
