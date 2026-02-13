import os
from datetime import timedelta
from dotenv import load_dotenv
from datetime import timezone, timedelta as td

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

# 设置时区为东八区（北京时间）
CHINA_TZ = timezone(td(hours=8))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'echo': False,
    }

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS').split(',')
    
    # 设置时区
    TIMEZONE = CHINA_TZ
