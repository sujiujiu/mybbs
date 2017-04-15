/**
 * Created by Administrator on 2017/4/5.
 */
// 点赞
$(function () {
    $('#star-btn').click(function (event) {
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        var is_star = parseInt($(this).attr('data-is-star'));
        var is_login = parseInt($(this).attr('data-is-login'));
        if(!is_login){
            window.location = '/account/login/';
            return;
        }

        xtajax.post({
            'url': '/post_star/',
            'data': {
                'post_id': post_id,
                'is_star': !is_star
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    if(is_star){
                        msg = '取消赞成功！';
                    }else {
                        msg = '点赞成功！';
                    }
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
    });
});


// 确认提交
$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();

        // var contentInput = $('#comment-content');

        var post_id = $(this).attr('data-post-id');
        // var content = contentInput.val();
        var content = window.editor.$txt.html();

        xtajax.post({
            'url': '/add_comment/',
            'data': {
                'post_id': post_id,
                'content': content
            },
            'success': function (data) {
                if(data['code'] == 200){
                    if(content.length !=0){
                        xtalert.alertSuccessToast('恭喜！评论成功！');
                        setTimeout(function () {
                            window.location = '/post_detail/'+post_id+'/';
                            // contentInput.val('').focus();
                            window.editor.clear();
                            window.location.reload();
                        },500);
                    }else{
                        xtalert.alertInfoToast('内容不能为空！')
                    }
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
    });
});

// 取消提交评论
$(function () {
    $("#cancel-comment-reply").click(function (event) {
        event.preventDefault();

        // var contentInput = $('input[name=comment-content]');

        var post_id = $(this).attr('data-post-id');
        // var content = contentInput.val();

        var content = window.editor.$txt.html();

        xtajax.post({
            'url': '/add_comment/',
            'data':{
                'post_id': post_id,
                'content':content
            },
            'success':function (data) {
                if(data['code'] == 200){
                    if(content.length !=0){
                        // contentInput.val('');
                        window.editor.clear();
                        window.event.returnValue = false;
                    }else{
                        xtalert.alertInfoToast('内容不能为空！')
                    }
                }else{
                   xtalert.alertInfoToast(data['message']);
               }
            }
        });
    });
});

// 点击回复显示评论框
$(function () {
    $('.reply-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        $('.reply-comment').eq(self.index()).show();

     });
});


// 回复评论
$(function () {
    $('.reply-submit').click(function (event) {
        event.preventDefault();

        var self = $(this);
        var commentInput = $('.comment-content').eq(self.index());
        console.log(self.index());
        var comment_id = $('.origin-comment-group').attr('data-comment-id');
        var content = commentInput.val();

        xtajax.post({
            'url': '/reply/',
            'data': {
                'comment_id': comment_id,
                'content': content
            },
            'success': function (data) {
                if(data['code'] == 200){
                    if(comment.length !=0){
                        xtalert.alertSuccessToast('恭喜！评论成功！');
                        setTimeout(function () {
                            window.location = '/post_detail/'+post_id+'/';
                            commentInput.val('');
                            window.location.reload();
                        },500);
                    }else{
                        xtalert.alertInfoToast('内容不能为空！')
                    }
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });

     });
});