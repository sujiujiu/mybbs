# -*-coding:utf-8-*-
from functools import wraps
import flask
import constants


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = flask.session.get(constants.FRONT_SESSION_ID)
        if user_id:
            return func(*args, **kwargs)
        else:
            flask.abort(401)
    return wrapper
