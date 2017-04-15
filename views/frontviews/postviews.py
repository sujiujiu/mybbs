#-*-coding:utf-8-*-
from flask import Blueprint, render_template
import flask
from decorators.frontdecorators import login_required
from exts import db
import constants
from models.frontmodels import FrontUser
from models.commonmodels import BoardModel, PostModel, CommentModel, PostStarModel
from models.basemodels import PostModelHelper
from forms.commonforms import AddPostForm, AddCommentForm, PostStarForm, ReplyCommentForm
from utils import xtjson
import qiniu
from time import sleep

bp = Blueprint('post', __name__)


# 默认显示第一页
@bp.route('/')
def index():
    return post_list(1, 1, 0)


# 帖子页数
@bp.route('/post_list/<int:page>/<int:sort>/<int:board_id>/')
def post_list(page, sort, board_id):
    context = PostModelHelper.post_list(page, sort, board_id)
    return render_template('front/front_index.html', **context)


# 发帖
@bp.route('/add_post/', methods=['GET', 'POST'])
@login_required
def add_post():
    if flask.request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_addpost.html', boards=boards)
    else:
        form = AddPostForm(flask.request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            # 将帖子标题及内容保存到数据库中
            post_model = PostModel(title=title, content=content)
            # 查询版块id是否存在，如果不存在就抛出异常，如果存在就将版块id和当前用户即作者存入数据库
            board_model = BoardModel.query.filter_by(id=board_id).first()
            if not board_model:
                return xtjson.json_params_error(message=u'没有该板块!')
            post_model.board = board_model
            post_model.author = flask.g.front_user
            db.session.add(post_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


# 帖子详情页
@bp.route('/post_detail/<int:post_id>/')
def post_detail(post_id):
    post_model = PostModel.query.filter(PostModel.is_removed==False, PostModel.id==post_id).first()
    if not post_model:
        flask.abort(404)
    # 如果帖子存在，阅读量没刷新一次加一
    post_model.read_count += 1
    db.session.commit()
    # 获取所有给这篇文章点赞的作者
    star_author_ids = [star_model.author.id for star_model in post_model.stars]
    context = {
        'post': post_model,
        'star_author_ids': star_author_ids
    }
    return flask.render_template('front/front_postdetail.html', **context)


# 添加评论
@bp.route('/add_comment/', methods=['GET', 'POST'])
@login_required
def add_comment():
    if flask.request.method == 'GET':
        post_id = flask.request.args.get('post_id',type=int)
        post = PostModel.query.get(post_id)
        # comment_id = flask.request.args.get('comment_id', type=int)
        context = {
            'post': post,
            # 'comment': comment_model
        }
        # if comment_id:
        #     context['origin_comment'] = CommentModel.query.get(comment_id)
        return render_template('front/front_postdetail.html', **context)
    else:
        form = AddCommentForm(flask.request.form)
        if form.validate():
            post_id = form.post_id.data
            content = form.content.data
            # comment_id = form.comment_id.data
            comment_model = CommentModel(content=content)
            post_model = PostModel.query.get(post_id)
            comment_model.post = post_model
            comment_model.author = flask.g.front_user
            # if comment_id:
            #     origin_comment = CommentModel.query.filter_by(id=comment_id).first()
            #     comment_model.origin_comment = origin_comment
            db.session.add(comment_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


# 回复评论
@bp.route('/reply/',methods=['GET', 'POST'])
def reply():
    if flask.request.method == 'GET':
        post_id = flask.request.args.get('post_id', type=int)
        post = PostModel.query.get(post_id)
        comment_id = flask.request.args.get('comment_id', type=int)
        context = {
            'post': post,
            # 'comment': comment_model
        }
        if comment_id:
            context['origin_comment'] = CommentModel.query.get(comment_id)
        return render_template('front/front_postdetail.html', **context)
    else:
        form = ReplyCommentForm(flask.request.form)
        if form.validate():
            post_id = form.post_id.data
            content = form.content.data
            comment_id = form.comment_id.data
            comment_model = CommentModel(content=content)
            post_model = PostModel.query.get(post_id)
            comment_model.post = post_model
            comment_model.author = flask.g.front_user
            if comment_id:
                origin_comment = CommentModel.query.get(comment_id)
                comment_model.origin_comment = origin_comment
            db.session.add(comment_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


# 回复评论
# @bp.route('/reply/', methods=['GET', 'POST'])
# @login_required
# def reply_comment():
#     if flask.request.method == 'GET':
#         return render_template('front/front_postdetail.html')
#     else:
#         pass


# 点赞
@bp.route('/post_star/', methods=['POST'])
@login_required
def post_star():
    form = PostStarForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        is_star = form.is_star.data
        post_model = PostModel.query.get(post_id)
        star_model = PostStarModel.query.filter_by(author_id=flask.g.front_user.id, post_id=post_id).first()
        # 如果表单中获取到点赞的信息，再去判断数据库中这个点赞是否存在，若存在，则提示已点赞，否则添加
        if is_star:
            if star_model:
                return xtjson.json_params_error(message=u'您已经给这篇帖子点赞了，无需再点！')
            star_model = PostStarModel()
            star_model.author = flask.g.front_user
            star_model.post = post_model
            db.session.add(star_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            # 如果表单中不存在点赞的信息，再去数据库中查是否存在，如果存在就将它删掉，若不存在就是还没有点赞
            if star_model:
                db.session.delete(star_model)
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'你尚未对该帖子进行点赞！')
    else:
        return xtjson.json_params_error(message=form.get_error())




# 测试，生成多篇文章
@bp.route('/test/')
def test():
    author = FrontUser.query.first()
    board = BoardModel.query.first()
    for x in xrange(0, 25):
        title = '帖子标题：%s' % x
        content = '帖子内容：%s' % x
        post_model = PostModel(title=title, content=content)
        post_model.author = author
        post_model.board = board
        db.session.add(post_model)
        sleep(1)
    db.session.commit()
    return 'success'


# 七牛
@bp.route('/qiniu_token/')
def qiniu_token():
    # 授权
    q = qiniu.Auth(constants.QINIU_ACCESS_KEY, constants.QINIU_SECRET_KEY)
    # 选择七牛的云空间
    bucket_name = 'mybbs-post'
    # 生成token
    token = q.upload_token(bucket_name)
    return flask.jsonify({'uptoken': token})


