from dotenv import load_dotenv
import os,sys
import logging
import secrets

load_dotenv()

server_env=os.getenv('server_env','dev')


# system
DEBUG = os.getenv("DEBUG", False)
SECRET_KEY  = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALLOWED_HOSTS  = os.getenv("ALLOWED_HOSTS", "*")
API_PREFIX  = os.getenv("API_PREFIX", "/api")


# token
JWT_TOKEN_PREFIX  = os.getenv("JWT_TOKEN_PREFIX","Token")  # noqa: S105
JWT_ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES  = 60 * 24 * 3  # 三天
# ACCESS_TOKEN_EXPIRE_MINUTES  = 1  # 三天