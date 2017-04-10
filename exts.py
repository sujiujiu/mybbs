# -*-coding:utf-8-*-
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_assets import Environment

db = SQLAlchemy()
mail = Mail()
assets_env = Environment()
