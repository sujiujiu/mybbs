# -*-coding:utf-8-*-
from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    def get_error(self):
        _, values = self.errors.popitem()
        message = values[0]
        return message
