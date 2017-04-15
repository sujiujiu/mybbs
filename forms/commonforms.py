# -*-coding:utf-8-*-
from baseforms import BaseForm
from utils import xtcache
from wtforms import StringField, ValidationError, IntegerField, BooleanField
from wtforms.validators import InputRequired


class GraphCaptchaForm(BaseForm):
    graph_captcha = StringField(validators=[InputRequired(message=u'必须输入图形验证码！')])

    # 图形验证码验证
    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        cache_captcha = xtcache.get(graph_captcha.lower())
        if not cache_captcha or cache_captcha.lower() != graph_captcha.lower():
            raise ValidationError(message=u'短信验证码错误!')
        return True


class AddPostForm(GraphCaptchaForm):
    title = StringField(validators=[InputRequired(message=u'必须输入标题！')])
    content = StringField(validators=[InputRequired(message=u'必须输入内容！')])
    board_id = IntegerField(validators=[InputRequired(message=u'必须输入板块id！')])


class AddCommentForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'必须输入帖子id！')])
    content = StringField(validators=[InputRequired(message=u'必须输入内容！')])


class PostStarForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'必须输入帖子id！')])
    is_star = BooleanField(validators=[InputRequired(message=u'必须输入赞的行为！')])


class ReplyCommentForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'必须输入帖子id！')])
    content = StringField(validators=[InputRequired(message=u'必须输入内容！')])
    comment_id = IntegerField()
