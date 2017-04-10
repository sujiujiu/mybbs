# -*-coding:utf-8-*-
from flask import Blueprint
from exts import db, mail
from flask import render_template, views, jsonify
import flask
from forms.cmsforms import CMSLoginForm, CMSResetpwdForm, CMSAddUserForm, CMSResetmailForm, CMSBlackUserForm, CMSEditBoardForm, CMSHightlightPostForm
from models.cmsmodels import CMSUser, CMSRole
from models.frontmodels import FrontUser
from models.commonmodels import BoardModel, PostModel, HighlightPostModel, CommentModel
from models.basemodels import PostModelHelper
import constants
from decorators.cmsdecorators import login_required, superadmin_required
from utils import xtjson, xtcache, xtmail, assets
from flask_mail import Mail, Message
import string
import random

bp = Blueprint('cms', __name__, subdomain='cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


class CMSLoginView(views.MethodView):

    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = CMSLoginForm(flask.request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                # 判断当前用户是否被拉黑
                if not user.is_active:
                    flask.abort(401)
                flask.session[constants.CMS_SESSION_ID] = user.id
                if remember:
                    flask.session.permanent = True
                else:
                    flask.session.permanent = False
                return flask.redirect(flask.url_for('cms.index'))
            else:
                return self.get(message=u'邮箱或密码错误！')
        else:
            message = form.get_error()
            return self.get(message=message)


# 注销
@bp.route('/logout/')
@login_required
def logout():
    flask.session.pop(constants.CMS_SESSION_ID)
    return flask.redirect(flask.url_for('cms.login'))


# 个人中心
@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


# 重置密码
@bp.route('/resetpwd/', methods=['GET', 'POST'])
@login_required
def resetpwd():
    if flask.request.method == 'GET':
        return render_template('cms/cms_resetpwd.html')
    else:
        form = CMSResetpwdForm(flask.request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            # 验证如果旧密码与数据库中的密码相等，就可以修改新密码
            if flask.g.cms_user.check_password(oldpwd):
                flask.g.cms_user.password = newpwd
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(u'密码错误！')
        else:
            message = form.get_error()
            return xtjson.json_params_error(message)


# CMS用户管理
@bp.route('/cmsusers/')
@login_required
def cms_users():
    users = CMSUser.query.all()
    context = {
        'users':users
    }
    return render_template('cms/cms_cmsusers.html', **context)


# 增加CMS用户
class AddCMSUserView(views.MethodView):

    decorators = [login_required]

    def get(self):
        roles = CMSRole.query.all()
        context = {
            'roles': roles
        }
        return render_template('cms/cms_addcmsuser.html', **context)

    def post(self):
        form = CMSAddUserForm(flask.request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            username = form.username.data
            roles = flask.request.form.getlist('roles[]')
            if not roles:
                return xtjson.json_params_error(message=u'必须指定最少一个分组！')
            user = CMSUser(email=email, username=username, password=password)
            for role_id in roles:
                role = CMSRole.query.get(role_id)
                role.users.append(user)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


class ResetMailView(views.MethodView):

    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetmail.html')

    def post(self):
        form = CMSResetmailForm(flask.request.form)
        if form.validate():
            email = form.email.data
            if flask.g.cms_user.email == email:
                return xtjson.json_params_error(message=u'新邮箱与老邮箱一致，无需修改！')
            flask.g.cms_user.email = email
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())

bp.add_url_rule('/login/', view_func=CMSLoginView.as_view('login'))
bp.add_url_rule('/add_cmsuser/', view_func=AddCMSUserView.as_view('add_cmsuser'))
bp.add_url_rule('/resetmail/', view_func=ResetMailView.as_view('resetmail'))


# 邮箱验证
@bp.route('/mail_captcha/')
def mail_captcha():
    email = flask.request.args.get('email')
    if xtcache.get(email):
        return xtjson.json_params_error(u'该邮箱已经发送验证码了！')

    source = list(string.letters)
    for x in xrange(0, 10):
        source.append(str(x))
    captcha_list = random.sample(source, 4)
    captcha = ''.join(captcha_list)
    if xtmail.send_mail(subject=u'潭州Python学院邮件验证码', receivers=email, body=u'邮箱验证码是：'+captcha):
        xtcache.set(email, captcha)
        return xtjson.json_result()
    else:
        return xtjson.json_server_error()


# 编辑cms用户
@bp.route('/edit_cmsuser/', methods=['GET', 'POST'])
@login_required
@superadmin_required
def edit_cmsuser():
    if flask.request.method == 'GET':
        user_id = flask.request.args.get('user_id')
        if not user_id:
            flask.abort(404)
        user = CMSUser.query.get(user_id)
        roles = CMSRole.query.all()
        current_roles = [role.id for role in user.roles]
        context = {
            'user': user,
            'current_roles':current_roles,
            'roles':roles
        }
        return render_template('cms/cms_edit_user.html', **context)
    else:
        user_id = flask.request.form.get('user_id')
        roles = flask.request.form.getlist('roles[]')
        print type(roles)
        # for role in roles
        if not user_id:
            return xtjson.json_params_error(message=u'没有指定id！')
        if not roles:
            return xtjson.json_params_error(message=u'必须指定最少一个分组！')
        user = CMSUser.query.get(user_id)
        # 把所有的roles的元素清空
        user.roles[:]=[]
        for role_id in roles:
            role_model = CMSRole.query.get(role_id)
            users.role.append(role_model)
        db.session.commit()
        return xtjson.json_result()


# 拉黑CMS用户管理
@bp.route('/black_user/', methods=['POST'])
@login_required
@superadmin_required
def black_user():
    form = CMSBlackUserForm(flask.request.form)
    if form.validate():
        user_id = form.user_id.data
        # 自己不能编辑自己
        if user_id == flask.g.cms_user.id:
            return xtjson.json_params_error(message=u'不能拉黑自己！')
        is_black = form.is_black.data
        user = CMSUser.query.get(user_id)
        user.is_active = not is_black
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


# 管理前台用户
@bp.route('/front_users/')
@login_required
def front_users():
    sort = flask.request.args.get('sort')
    front_users = None
    # 默认按时间降序排序，最新的为上，
    # 1为按时间，2为按帖子量，3为按评论量
    if not sort or sort == '1':
        front_users = FrontUser.query.order_by(FrontUser.join_time.desc())
    elif sort == '2':
        front_users = db.session.query(FrontUser).outerjoin(PostModel).group_by(FrontUser.id).order_by(db.func.count(PostModel.id).desc(),FrontUser.join_time.desc())
        # posts = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
        #     db.func.count(CommentModel.id).desc(), PostModel.create_time.desc())
    elif sort == '3':
        front_users = db.session.query(FrontUser).outerjoin(CommentModel).group_by(FrontUser.id).order_by(db.func.count(CommentModel.id).desc(),FrontUser.join_time.desc())
    else:
        front_users = FrontUser.query.order_by(PostModel.create_time.desc())

    front_users = front_users.filter(PostModel.is_removed == False)
    context = {
        'front_users': front_users,
        'current_sort' : sort,
        # 'post_count': PostModel.query.filter(PostModel.author).count()
    }
    return render_template('cms/cms_frontusers.html', **context)


# 编辑前台用户
@bp.route('/edit_frontuser/')
@login_required
def edit_front_user():
    user_id = flask.request.args.get('id')
    if not user_id:
        flask.abort(404)
    user = FrontUser.query.get(user_id)
    if not user:
        flask.abort(404)
    return render_template('cms/cms_edit_frontuser.html',current_user=user)


# 拉黑前台用户
@bp.route('/black_fontuser/', methods=['POST'])
@login_required
def black_front_user():
    form = CMSBlackUserForm(flask.request.form)
    if form.validate():
        user_id = form.user_id.data
        is_black = form.is_black.data
        user = FrontUser.query.get(user_id)
        if not user:
            flask.abort(404)
        user.is_active = not is_black
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


# 版块管理
@bp.route('/boards/')
@login_required
def boards():
    all_boards = BoardModel.query.all()
    context = {
        'boards': all_boards
    }
    return render_template('cms/cms_boards.html', **context)


# 增加版块
@bp.route('/add_board/', methods=['POST'])
@login_required
def add_board():
    # 从表单中获取并判断输入框中版块的名字是否存在
    name = flask.request.form.get('name')
    if not name:
        return xtjson.json_params_error(message=u'必须指定板块的名称！')
    # 再判断数据库中是否存在
    board = BoardModel.query.filter_by(name=name).first()
    if board:
        return xtjson.json_params_error(message=u'该板块已经存在，不能重复添加！')
    # 如果不存在则创建
    board = BoardModel(name=name)
    # 创建者为当前登录的cms用户
    board.author = flask.g.cms_user
    db.session.add(board)
    db.session.commit()
    return xtjson.json_result()


# 编辑版块
@bp.route('/edit_board/', methods=['POST'])
@login_required
def edit_board():
    form = CMSEditBoardForm(flask.request.form)
    if form.validate():
        block_id = form.board_id.data
        name = form.name.data
        # 从数据库中获取此版块的id
        board = BoardModel.query.get(block_id)
        # 改变版块的名称，并保存到数据库中
        board.name = name
        db.session.add(board)
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())



# 删除版块
@bp.route('/delete_board/', methods=['POST'])
@login_required
def delete_board():
    board_id = flask.request.form.get('board_id')
    if not board_id:
        return xtjson.json_params_error(message=u'没有指定板块id！')
    # 从数据库中查找版块名是否存在，不存在就不能删掉
    board = BoardModel.query.filter_by(id=board_id).first()
    if not board:
        return xtjson.json_params_error(message=u'该板块不存在，删除失败！')

    # 之后还有判断该版块下是否有帖子数而决定是否能被删除，如果有就不能删掉

    # 删掉对应的版块
    db.session.delete(board)
    db.session.commit()
    return xtjson.json_result()


# 管理帖子
@bp.route('/posts/')
@login_required
def posts():
    # 按类别排序
    sort = flask.request.args.get('sort', 1, type=int)
    # 按版块
    board_id = flask.request.args.get('board', 0, type=int)
    # 页数
    page = flask.request.args.get('page', 1, type=int)
    context = PostModelHelper.post_list(page,sort,board_id)
    return render_template('cms/cms_posts.html',**context)


# 精华帖管理
@bp.route('/highlight/', methods=['POST'])
@login_required
def highlight():
    form = CMSHightlightPostForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        is_highlight = form.is_highlight.data
        post_model = PostModel.query.get(post_id)
        if is_highlight:
            if post_model.highlight:
                return xtjson.json_params_error(message=u'该帖子已经加精！')
            highlight_model = HighlightPostModel()
            post_model.highlight = highlight_model
            db.session.commit()
            return xtjson.json_result()
        else:
            if not post_model.highlight:
                return xtjson.json_params_error(message=u'该帖子没有加精！')
            db.session.delete(post_model.highlight)
            db.session.commit()
            return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


# 移除帖子，但不删除数据
@bp.route('/remove_post/', methods=['POST'])
@login_required
def remove_post():
    post_id = flask.request.args.get('post_id',1,type=int)
    if not post_id:
        return xtjson.json_params_error(message=u'必须输入帖子id！')
    post_model = PostModel.query.get(post_id)
    post_model.is_removed = True
    db.session.commit()
    return xtjson.json_result()


# 评论管理
@bp.route('/comments/', methods=['GET'])
@login_required
def comments():
    page = flask.request.args.get('page',1,type=int)
    # page从1开始，而不是0,start和end分别为每一页的第一条和最后一条数据
    start = (page - 1) * constants.PAGE_NUM
    end = start + constants.PAGE_NUM
    # 所有的评论
    comments = CommentModel.query.filter_by(is_removed=False)
    # 获取所有的评论
    total_comments = comments.count()
    # 得到所有的页数
    total_page = total_comments / constants.PAGE_NUM
    # 若有余数则页数加一页
    if total_comments % constants.PAGE_NUM > 0:
        total_page += 1
    # pages用来装一个列表，为当前页数及其前后共五页的数据
    pages = []
    '''
    我们假定每一列页数显示五页，例如8这个数，在第二列页数里，为6到10，左边不会出现5，而右边会包括10，
    以此类推，每一列页数都一样，所以分为两部分，一部分往前8找，一部分往8后找，
    往前找，最左边不能小于1，往后不能大于最大的页数，最左边是5的倍数-1，最右边是5的倍数，
    所以左边的判断：对5求余，如果不为0，就将数据存在pages里，为0就不添加
    而对右边的判断：余为0就添加然后跳出循环，因为后面没有数据，而如果不是也要添加数据到列表，而不跳出
    '''
    # 左边的判断
    left_page = page - 1
    while left_page >= 1:
        if left_page % 5 == 0:
            break
        pages.append(left_page)
        left_page -= 1

    # 右边的判断
    right_page = page
    while right_page <= total_page:
        if right_page % 5 == 0:
            pages.append(right_page)
            break
        else:
            pages.append(right_page)
            right_page += 1

    # 数据传到前台页面前，先对其排序
    pages.sort()

    context = {
        'comments': comments.slice(start, end),
        'pages': pages,
        # c_page为当前页面
        'c_page': page,
        # t_page为总共的页数
        't_page': total_page
    }
    return render_template('cms/cms_comments.html', **context)


# 移除评论
@bp.route('/remove_comment/', methods=['POST'])
@login_required
def remove_comment():
    comment_id = flask.request.args.get('comment_id',1,type=int)
    if not comment_id:
        return xtjson.json_params_error(message=u'必须输入评论id！')
    comment_model = CommentModel.query.get(comment_id)
    comment_model.is_removed = True
    db.session.commit()
    return xtjson.json_result()



# 像用户名这种整个模板都会用到的，放在上下文处理器当中
@bp.context_processor
def cms_context_processor():
    id = flask.session.get(constants.CMS_SESSION_ID)
    if id:
        user = CMSUser.query.get(id)
        return {'cms_user': user}
    else:
        return {}


# 每次请求的时候都会请求对应的函数，其他视图函数也可能用得到当前登录的这个用户
@bp.before_request
def cms_before_request():
    id = flask.session.get(constants.CMS_SESSION_ID)
    if id:
        user = CMSUser.query.get(id)
        # 获取了这个用户的id便把它绑定在g这个对象上去
        flask.g.cms_user = user


@bp.errorhandler(404)
def cms_not_find(error):
    return render_template('common/error/404.html'), 404

@bp.errorhandler(401)
def cms_auth_forbidden(error):
    if flask.request.is_xhr:
        return xtjson.json_unauth_error()
    else:
        return render_template('common/error/401.html'), 401