# -*-coding:utf-8-*-
from exts import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# 权限表
class CMSPermission(object):
    ADMINISTRATOR = 255
    OPERATOR = 1
    PERMISSION_MAP = {
        ADMINISTRATOR: (u'超级管理权限', u'拥有最高权限'),
        OPERATOR: (u'普通管理权限', u'可以查看并删除用户、帖子、评论'),
    }

cms_user_role = db.Table('cms_user_role',
                         db.Column('role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
                         db.Column('user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True))


# 角色表
class CMSRole(db.Model):
    __tablename__ = 'cms_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    permissions = db.Column(db.Integer, default=CMSPermission.OPERATOR, nullable=False)


class CMSUser(db.Model):
    __tablename__ = 'cms_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    last_login_time = db.Column(db.DateTime, nullable=True)
    roles = db.relationship('CMSRole', secondary=cms_user_role, backref='users')

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        # 它调用的就是下面那个setter的password函数里的方法
        self.password = password

    # property将方法变成一个属性，适用于没有参数的函数
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, rawpwd):
        self._password = generate_password_hash(rawpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self.password, rawpwd)

    @property
    def is_superadmin(self):
        return self.has_permission(CMSPermission.ADMINISTRATOR)

    def has_permission(self, permission):
        all_permission = 0
        if not self.roles:
            return False
        for role in self.roles:
            all_permission |= role.permissions
        return all_permission & permission == permission

    @property
    def permission(self):
        all_permission = 0
        permission_dicts = []
        if not self.roles:
            return None
        for role in self.roles:
            all_permission |= role.permissions
        for permission, permission_info in CMSPermission.PERMISSION_MAP.iteritems():
            if all_permission & permission == permission:
                permission_dicts.append({permission: permission_info})
        return permission_dicts






