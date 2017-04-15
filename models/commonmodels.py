#-*-coding:utf-8-*-
from datetime import datetime
from exts import db
import constants


# 版块模型
class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('cms_user.id'))

    author = db.relationship('CMSUser', backref='boards')

    def __init__(self, name, author):
        self.name = name
        self.author = author


# 帖子相关模型
class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    read_count = db.Column(db.Integer, default=0)
    is_removed = db.Column(db.Boolean, default=False)

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))
    highlight_id = db.Column(db.Integer, db.ForeignKey('highlight_post.id'))
    #lazy默认为select，它的意义等同于原来的用法，
    # 如果想要在模板中使用filter方法，就要将它改为dynamic，可以将它变为一个query对象，可以使用filter方法
    board = db.relationship('BoardModel', backref=db.backref('posts', lazy='dynamic'))
    author = db.relationship('FrontUser', backref='posts')
    # 一对一的关系，使用uselist=False
    highlight = db.relationship('HighlightPostModel', backref='post', uselist=False)

    def __init__(self, title, content, author, board):
        self.title = title
        self.content = content
        self.author = author
        self.board = board


# 精华帖
class HighlightPostModel(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)


# 评论
class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_removed = db.Column(db.Boolean, default=False)

    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    origin_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    author = db.relationship('FrontUser', backref=db.backref('comments',lazy='dynamic'))
    post = db.relationship('PostModel', backref='comments')
    # 原始评论，即当二级评论时被引用
    origin_comment = db.relationship('CommentModel', backref='replys', remote_side=[id])

    # def __init__(self,content, author, post, origin_comment=None):
    #     self.content = content
    #     self.author = author
    #     self.post = post
    #     self.origin_comment = origin_comment



# 点赞
class PostStarModel(db.Model):
    __tablename__ = 'post_star'
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.String(30), db.ForeignKey('front_user.id'), nullable=False)

    author = db.relationship('FrontUser', backref='stars')
    post = db.relationship('PostModel', backref='stars')


