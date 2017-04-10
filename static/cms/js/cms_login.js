$(function () {
    $('#login_submit').click(function (event) {
        event.preventDefault();

        var email = $('input[name=email]').val();
        var password = $('input[name=password]').val();

        xtajax.post({
            'url':'/login/',
            'data':{
                'email': email,
                'password': password
            },
            'success': function (data) {
                var code = data['code'];
                if(code == 200){
                    // 跳转到首页
                    window.location = '/';
                }else{
                    var message = data['message'];
                    // alert(message);
                    var errorTag = $('.error-info');
                    errorTag.text(message);
                }
            }
        })
    });
});

