# -*-coding:utf-8-*-
from flask import Flask, render_template
import flask
from exts import db, mail, assets_env
import config
from views.cmsviews import cmsviews
from views.frontviews import postviews, accountviews
from flask_wtf import CSRFProtect
from utils import xtjson
import constants
from models.frontmodels import FrontUser
from webassets.loaders import PythonLoader
# import os
from utils import assets
from datetime import datetime

app = Flask(__name__,static_folder='static')
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
CSRFProtect(app)
# assets_env.init_app(app)
# assets_env.register(bundles)

app.register_blueprint(cmsviews.bp)
app.register_blueprint(accountviews.bp)
app.register_blueprint(postviews.bp)


# 将打包对象注册到Environment中
# assets_loader = PythonLoader(assets)
# for name, bundle in assets_loader.load_bundles().iteritems():
#     assets_env.register(name, bundle)


# assets_env.register('cms_js', cms_js)
# assets_env.register('common_js', common_js)
# assets_env.register('cms_css', cms_css)
# assets_env.register('common_css', common_css)


@app.before_request
def post_before_request():
    id = flask.session.get(constants.FRONT_SESSION_ID)
    if id:
        user = FrontUser.query.get(id)
        flask.g.front_user = user


@app.context_processor
def post_context_processor():
    if hasattr(flask.g, 'front_user'):
        return {'front_user': flask.g.front_user}
    return {}


@app.errorhandler(401)
def post_auth_forbidden(error):
    if flask.request.is_xhr:
        return xtjson.json_unauth_error()
    else:
        return flask.redirect(flask.url_for('account.login'))


@app.errorhandler(404)
def post_not_find(error):
    if flask.request.is_xhr:
        return xtjson.json_params_error()
    else:
        return render_template('common/error/404.html'), 404


# 自定义一个时间过滤器
@app.template_filter('haddle_time')
def haddle_time(time):
    if type(time) == datetime:
        now = datetime.now()
        # 帖子发布的时间距此刻时间的总秒数
        timestamp = (now - time).total_seconds()
        if timestamp < 60:
            return u'刚刚'
        elif timestamp > 60 and timestamp < 60*60:
            minutes = timestamp / 60
            return u'%s分钟前'% int(minutes)
        elif timestamp >60*60 and timestamp <60*60*24:
            hours = timestamp / (60*60)
            return u'%s小时前' % int(hours)
        elif timestamp >60*60*24 and timestamp <60*60*24*30:
            days = timestamp / (60*60*24)
            return u'%s天前' % int(days)
        elif now.year == time.year:
            return time.strftime('%m-%d %H:%M:%S')
        else:
            return time.strftime('%Y-%m-%d %H:%M:%S')



if __name__ == '__main__':
    app.run(debug=True)
