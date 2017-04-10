# -*-coding:utf-8-*-
import flask
from exts import db
from flask import Blueprint, render_template, views
from utils.captcha.xtcaptcha import Captcha
from utils import xtcache
from utils import xtjson
import top.api
import constants
from forms.frontforms import FrontRegisterForm, FrontLoginForm, SettingsForm
from models.frontmodels import FrontUser, GenderType
from decorators.frontdecorators import login_required
from datetime import datetime

try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO

bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/')
def index():
    return 'font account page'


class RegisterView(views.MethodView):

    # 可以返回一些用户已经填入的信息
    def get(self, message=None, **kwargs):
        context = {
            'message': message
        }
        context.update(**kwargs)
        return render_template('front/front_register.html', **context)

    def post(self):
        form = FrontRegisterForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return flask.redirect(flask.url_for('post.index'))
        else:
            telephone = flask.request.form.get('telephone')
            username = flask.request.form.get('username')
            return self.get(message=form.get_error(), telephone=telephone, username=username)


class LoginView(views.MethodView):

    def get(self, message=None):
        return render_template('front/front_login.html', message=message)

    def post(self):
        form = FrontLoginForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data

            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                flask.session[constants.FRONT_SESSION_ID] = user.id
                if remember:
                    flask.session.permanent = True
                return flask.redirect(flask.url_for('post.index'))
            else:
                return self.get(message=u'手机号码或密码错误！')
        else:
            return self.get(message=form.get_error())


bp.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))


# 注销
@bp.route('/logout/')
@login_required
def logout():
    # 使用pop而不是del方法，del如果不存在这个用户名会保存，而pop会返回None
    flask.session.pop(constants.FRONT_SESSION_ID)
    return flask.redirect(flask.url_for('post.index'))


# 个人设置
@bp.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    if flask.request.method == 'GET':
        return render_template('front/front_settings.html')
    else:
        form = SettingsForm(flask.request.form)
        if form.validate():
            username = form.username.data
            realname = form.realname.data
            qq = form.qq.data
            avatar = form.avatar.data
            signature = form.signature.data
            gender = form.gender.data
            # 用户登录之后只要获取当前用户的信息，然后就可以直接传入数据
            user_model = flask.g.front_user
            # 只有用户名是必填项，其他可以不填，所以需要判断,而性别是有默认选项
            user_model.username = username
            user_model.gender = gender
            if realname:
                user_model.realname = realname
            if qq:
                user_model.qq = qq
            if avatar:
                user_model.avatar = avatar
            if signature:
                user_model.signature = signature
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


# 个人信息页
@bp.route('/profile/<user_id>/', methods=['GET'])
def profile(user_id):
    if not user_id:
        return flask.abort(404)
    user = FrontUser.query.get(user_id)
    if user:
        # 如果上上次登录时间存在，这次登录之后，显示的上次登录时间就是上上次，如果不存在，或者从未登录过，就设为当前时间
        if user.old_login_time:
            user.last_login_time = user.old_login_time
        user.old_login_time = datetime.now()
        db.session.commit()
        context = {
            'current_user': user,
        }
        return render_template('front/front_profile.html', **context)
    else:
        return flask.abort(404)


# 显示个人发布所有帖子页
@bp.route('/profile/posts/', methods=['GET'])
def profile_posts():
    user_id = flask.request.args.get('user_id')
    if not user_id:
        return flask.abort(404)

    user = FrontUser.query.get(user_id)
    if user:
        context = {
            'current_user': user,
        }
        return render_template('front/front_profile_posts.html', **context)
    else:
        return flask.abort(404)



# 图形验证码
@bp.route('/graph_captcha/')
def graph_captcha():
    # 验证码和图片
    text, image = Captcha.gene_code()
    out = StringIO()
    image.save(out, 'png')
    # 将StringIO的指针指向开始的位置
    out.seek(0)
    # 把图片流给读出来
    response = flask.make_response(out.read())
    # 指定响应的类型
    response.content_type = 'image/png'
    xtcache.set(text.lower(), text.lower(), timeout=2*60)
    return response


# 短信验证码
@bp.route('/sms_captcha/')
def sms_captcha():
    telephone = flask.request.args.get('telephone')
    # 获取用户名，用于发送短信验证码显示用户名
    # username = flask.request.args.get('username')
    if not telephone:
        return xtjson.json_params_error(message=u'必须指定手机号码！')
    if xtcache.get(telephone):
        return xtjson.json_params_error(message=u'验证码已发送，请1分钟后重复发送！')
    # if not username:
    #     return xtjson.json_params_error(message=u'必须输入用户名！')
    # 阿里大于APP_KEY及APP_SECRET
    app_key = constants.APP_KEY
    app_secret = constants.APP_SECRET
    req = top.setDefaultAppInfo(app_key, app_secret)
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.extend = ""
    req.sms_type = 'normal'
    # 签名名称
    req.sms_free_sign_name = constants.SIGN_NAME
    # 随即生成字符串
    captcha = Captcha.gene_text()
    # 设置短信的模板
    req.sms_param = "{code:%s}" % captcha
    # req.sms_param = "{username:%s,code:%s}" % (username, captcha)
    req.rec_num = telephone.decode('utf-8').encode('ascii')
    req.sms_template_code = constants.TEMPLATE_CODE
    try:
        resp = req.getResponse()
        xtcache.set(telephone, captcha)
        return xtjson.json_result()
    except Exception, e:
        print e
        return xtjson.json_server_error()



