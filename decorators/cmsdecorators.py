# -*-coding:utf-8-*-
import flask
import constants
from functools import wraps
from utils import xtjson
from models.cmsmodels import CMSPermission


def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        cms_id = flask.session.get(constants.CMS_SESSION_ID)
        if cms_id:
            return func(*args, **kwargs)
        else:
            return flask.redirect(flask.url_for('cms.login'))

    return wrapper


# 权限限制
def permission_required(permission):
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if flask.g.cms_user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                flask.abort(401)
        return wrapper
    return deco


# 超级管理员权限
def superadmin_required(func):
    return permission_required(CMSPermission.ADMINISTRATOR)(func)
