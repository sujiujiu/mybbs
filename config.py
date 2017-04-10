# -*-coding:utf-8-*-
import os

SECRET_KEY = os.urandom(24)

# ASSETS_DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'mybbs'
# DB_CHARSET = 'charset=utf8'

# DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_CHARSET)
DB_URI = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

SERVER_NAME = 'mybbs.com:5000'

# 配置邮箱
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USERNAME = '1835198009@qq.com'
MAIL_PASSWORD = 'dd'
MAIL_DEFAULT_SENDER = '1835198009@qq.com'
MAIL_USE_TLS = True
# MAIL_USE_SSL = False 这两种都可以，这个端口是465
