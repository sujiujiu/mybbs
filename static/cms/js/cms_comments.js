/**
 * Created by Administrator on 2017/4/5.
 */
$(function () {
    $('.remove-btn').click(function (event) {
        event.preventDefault();

        var comment_id = $(this).attr('data-comment-id')
        xtalert.alertConfirm({
            'msg': '你确定要移除这条评论吗？',
            'confirmCallback': function () {
                // 发送ajax
                xtajax.post({
                    'url': '/remove_comment/',
                    'data': {
                        'id': comment_id
                    },
                    'success': function (data) {
                        if(data['code'] != 200){
                            xtalert.alertInfoToast(data['message']);
                        }else{
                            xtalert.alertSuccessToast('移除成功！');
                            setTimeout(function () {
                                window.location.reload();
                            },1000);
                        }
                    }
                });
            }
        });
    });
});