# -*-coding:utf-8-*-
from exts import db
import shortuuid
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


class GenderType(object):
    MAN = 1
    WOMAN = 2
    SECRET = 3


class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid())
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(100))
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    last_login_time = db.Column(db.DateTime, nullable=True)
    old_login_time = db.Column(db.DateTime)
    qq = db.Column(db.String(20))
    realname = db.Column(db.String(20))
    gender = db.Column(db.Integer, default=GenderType.SECRET)
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    points = db.Column(db.Integer, default=0)

    def __init__(self, telephone, username, password):
        self.telephone = telephone
        self.username = username
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, rawpwd):
        self._password = generate_password_hash(rawpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self._password, rawpwd)


