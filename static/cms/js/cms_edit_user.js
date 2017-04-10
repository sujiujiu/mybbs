/**
 * Created by Administrator on 2017/3/20.
 */

// 修改用户信息
$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        // 获取所有的分组
        var roleInputs = $(':checkbox:checked');
        var roles = [];
        roleInputs.each(function () {
            var role_id = $(this).val();
            roles.push(role_id);
        });

        // 发送ajax请求
        var user_id = $(this).attr('data-user-id');
        xtajax.post({
            'url': '/edit_cmsuser/',
            'data': {
                'roles': roles,
                'user_id': user_id
            },
            'success': function (data) {
                if(data['code'] != 200){
                    xtalert.alertInfoToast(data['message']);
                }else{
                    xtalert.alertSuccessToast('CMS用户信息修改成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }
            }
        });
    });
});

// 操作管理黑名单
$(function () {
   $('#black-list-btn').click(function (event) {
       event.preventDefault();
        var user_id = $(this).attr('data-user-id');
        var is_active = parseInt($(this).attr('data-is-active'));

        var is_black = is_active;

        xtajax.post({
            'url': '/black_user/',
            'data':{
                'user_id': user_id,
                'is_black': is_black
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    if(is_black){
                        msg = '恭喜！已经将该用户拉入黑名单！'
                    }else{
                        msg = '恭喜！已经将该用户移出黑名单！'
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
   })
});