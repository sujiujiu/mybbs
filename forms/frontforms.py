# -*-coding:utf-8-*-
from utils import xtcache
from wtforms import StringField, ValidationError, BooleanField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length, URL
from models.frontmodels import FrontUser
from commonforms import GraphCaptchaForm
from baseforms import BaseForm


class FrontRegisterForm(GraphCaptchaForm):
    telephone = StringField(validators=[InputRequired(message=u'必须输入手机号码！'), Length(11, 11, message=u'手机号码格式不对，长度应为11位！')])
    sms_captcha = StringField(validators=[InputRequired(message=u'必须输入短信验证码！')])
    username = StringField(validators=[InputRequired(message=u'必须输入用户名！')])
    password = PasswordField(validators=[InputRequired(message=u'必须输入密码！'), Length(6, 20, message=u'密码长度必须在6-20个字符之间！')])
    password_repeat = PasswordField(validators=[EqualTo('password')])

    # 手机号码验证
    def validate_telephone(self, field):
        telephone = field.data
        user = FrontUser.query.filter(FrontUser.telephone == telephone).first()
        if user:
            raise ValidationError(u'该手机已经注册，不能重复注册！')

    # 短信验证码验证
    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data
        cache_captcha = xtcache.get(telephone)
        if not cache_captcha or cache_captcha.lower() != sms_captcha.lower():
            raise ValidationError(message=u'短信验证码错误!')
        return True


class FrontLoginForm(GraphCaptchaForm):
    telephone = StringField(
        validators=[InputRequired(message=u'必须输入手机号码！'), Length(11, 11, message=u'手机号码格式不对，长度应为11位！')])
    password = PasswordField(validators=[InputRequired(message=u'必须输入密码！'),
                                         Length(6, 20, message=u'密码长度必须在6-20个字符之间！')])
    remember = BooleanField()


class SettingsForm(BaseForm):
    username = StringField(validators=[InputRequired(message=u'必须输入用户名！')])
    realname = StringField()
    qq = StringField()
    avatar = StringField(validators=[URL(message=u'头像格式不对！')])
    signature = StringField()
    gender = BooleanField()
