/**
 * Created by Administrator on 2017/3/24.
 */

$(function () {
    $('#back-list-btn').click(function (event) {
        event.preventDefault();

        var is_active = parseInt($(this).attr('data-is-active'));
        var user_id = $(this).attr('data-user-id');

        var is_black = is_active;

        xtajax.post({
            'url': '/black_front_user/',
            'data': {
                'user_id': user_id,
                'is_black': is_black
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    if(is_black){
                        msg = '恭喜！已经将该用户加入黑名单！';
                    }else{
                        msg = '恭喜！已经将该用户移出黑名单！';
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
