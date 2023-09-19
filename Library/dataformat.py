from fastapi import Body, FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import re
import random, string
import pytz
import os
import gc
import re
import traceback
import sys
import json
import os.path
import gettext
import ssl
import boto3
import collections 
from datetime import datetime,timedelta,timezone
import urllib.request
import requests
import hashlib
import base64
# gc.set_debug(gc.DEBUG_STATS|gc.DEBUG_LEAK)
localedir = os.path.join(os.getcwd())+'/locale'
ssl._create_default_https_context = ssl._create_unverified_context

AWS_S3_URL=os.getenv('AWS_S3_URL','')
AWS_S3_BUCKET=os.getenv('AWS_S3_BUCKET','')
AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID','')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY','')

def MultipleRows2Json(data):
    rows = []
    for x in data:
        a = x.to_json()
        rows.append(x.to_json())
    if len(rows) == 0:
        return Response("", status=204)
    else:    
        return JSONResponse(status_code=200, content=rows)
        # return Response(jsonable_encoder({"data":rows}, sort_keys=False), status=200, mimetype='application/json') 

 
def OneRow2Json(data):
    if data is None:
        return Response("", status=204)
    else:
        row = data.to_json()
        if len(row) == 0:
            return Response("", status=204)
        else:
            return Response(jsonable_encoder({"data":row}, sort_keys=False), status=200, mimetype='application/json')

def RowsFormat(data):
    rows = []
    for x in data:
        a = x.to_json()
        rows.append(x.to_json())
    return rows


def StripTags(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()

def clean_script(html):
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    return cleaned.strip()


def Request_Format(request):
    response = {}
    for key in request:
        response[key] =  StripTags(request[key])
    return response

def Random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
    # return ''.join(random.choice(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z','2','3','4','5','6','7','8','9']) for x in range(length))
# def random_string(set_range):
#     return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(set_range))


def Response_result(content,code):
    if content == "":
        return Response(content, status=code, mimetype='application/json')
    else:
        return JSONResponse(status_code=code, content=content)
        # return Response(jsonable_encoder(content, sort_keys=False), status=code, mimetype='application/json')



def get_time_for_now():
    new_timezone = pytz.timezone("Asia/Taipei")
    TS = datetime.now(new_timezone).timestamp()
    return TS

def generateID():
    return str(int(datetime.utcnow().timestamp() * 1000000))+str(random.randint(11,99))

def generateUID():
    return str(int(datetime.utcnow().timestamp() * 10000))+str(random.randint(11,99))


def check_token(request):
    try: 
        for h in request.headers.keys():
            if (h == 'authorization') or (h == 'authorization-'):
                token_type, access_token = request.headers.get(h).split(' ')
                if token_type != 'Bearer' or token_type is None:
                    return False
                else:
                    return access_token
        return False
    except:
        return False


def get_lang(request):
    allow_lan = ['zh','en']
    setLang = 'zh'
    try: 
        lang = request.headers.get('Accept-Language')
        if lang is not None:
            if lang in allow_lan:
                setLang = lang
            else:
                setLang = 'zh'
    except:
        setLang = 'zh'

    msgLang = gettext.translation('messages', localedir, languages=[setLang])
    msgLang.install()
    return setLang



def abort_msg(e):
    """500 bad request for exception

    Returns:
        500 and msg which caused problems
    """
    error_class = e.__class__.__name__ # 引發錯誤的 class
    detail = e.args[0] # 得到詳細的訊息
    cl, exc, tb = sys.exc_info() # 得到錯誤的完整資訊 Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] # 取得最後一行的錯誤訊息
    fileName = lastCallStack[0] # 錯誤的檔案位置名稱
    lineNum = lastCallStack[1] # 錯誤行數 
    funcName = lastCallStack[2] # function 名稱
    # generate the error message
    errMsg = "Exception raise in file: {}, line {}, in {}: [{}] {}. Please contact the member who is the person in charge of project!".format(fileName, lineNum, funcName, error_class, detail)
    # return 500 code
    abort(500, errMsg)




def format_timezone(time, tzinfo=None):
    time_beijing = time.astimezone(tzinfo)
    print(time_beijing)




def getS3File(folder,filename,ext,AWS_S3_URL='',AWS_S3_BUCKET=''):
    if AWS_S3_URL == '':
        AWS_S3_URL=os.getenv('AWS_S3_URL','')

    if AWS_S3_BUCKET == '':
        AWS_S3_BUCKET=os.getenv('AWS_S3_BUCKET','')


    return AWS_S3_URL+"/"+AWS_S3_BUCKET+"/"+folder+"/"+filename+"."+ext


def id_rand():
    rand = random.randint(11111,99999)
    no = int(datetime.utcnow().timestamp() * 1000)
    return str(no)+str(rand)


def downloadImage(url,filename):
    # urllib.request.urlretrieve(url,filename)
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)


def base64ToImage(encoded_data,filename):
    decoded_data=base64.b64decode((encoded_data))
    #write the decoded data back to original format in  file
    img_file = open(filename, 'wb')
    img_file.write(decoded_data)
    img_file.close()

# 上傳檔案到 S3 
def uploadImage(file_name,file):
    s3_resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,region_name='ap-east-1')
    s3_resource.meta.client.upload_file(file, AWS_S3_BUCKET,file_name)


def removeFile(file):
    os.remove(file)

# sha1 加密 (加密用戶密碼)
def sha1Password(pwd):
    sha = hashlib.sha1()
    sha.update(pwd.encode('utf-8'))
    hexPass = sha.hexdigest()
    return hexPass




