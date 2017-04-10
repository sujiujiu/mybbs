/**
 * Created by Administrator on 2017/4/8.
 */
$(function () {
    xtqiniu.setUp({
        'browse_btn': 'avatar-img',
        'success': function (up,file,info) {
            var imgTag = $('#avatar-img');
            imgTag.attr('src',file.name);
        }
    });
});

$(function () {
    $("#submit-btn").click(function (evnet) {
        event.preventDefault();

        var gender_radio = $('input[name="sex"]');

        var username = $('input[name=username]').val();
        var realname = $('input[name=realname]').val();
        var qq = $('input[name=qq]').val();
        var signature = $('#signature-area').val();
        var avatar = $('#avatar-img').attr('src');
        var gender = $("input[name='sex']:checked").val();

        xtajax.post({
            'url': '/account/settings/',
            'data':{
                'username': username,
                'realname': realname,
                'qq': qq,
                'signature': signature,
                'avatar':avatar,
                'gender': gender
            },
            'success': function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('恭喜！修改成功！');
                    for (var i =0;i<gender_radio.length;i++){
                        if (gender_radio[i].checked)
                            return gender_radio[i].value;
                    }
                    // gender_radio.attr('checked', 'true');
                    window.location.reload();
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});