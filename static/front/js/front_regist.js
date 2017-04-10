/**
 * Created by Administrator on 2017/3/20.
 */

$(function () {
   $('#send-captcha-btn').click(function (event) {
       event.preventDefault();
       var self = $(this);
       // 获取手机号码
       var telephone = $('input[name=telephone]').val();

       if(!telephone){
           xtalert.alertInfoToast('请输入手机号码！');
           return;
       }

       xtajax.get({
           'url': '/account/sms_captcha/',
           'data': {
               'telephone': telephone
           },
           'success': function (data) {
               if(data['code'] == 200){
                   xtalert.alertSuccessToast('验证码已发送，请注意查收！');
                   var timeCount = 60;
                   self.attr('disabled','disabled');
                   self.css('cursor','default');
                   var timer = setInterval(function () {
                       self.text(timeCount);
                       timeCount--;
                       if(timeCount <= 0){
                           self.text('发送验证码');
                           self.removeAttr('disabled');
                           clearInterval(timer);
                           self.css('cursor','pointer');
                       }
                   },1000);
               }else{
                   xtalert.alertInfoToast(data['message']);
               }
           }
       });
   });
});

// $(function () {
//     var btn = $('#graph-captcha-btn');
//     btn.css('cursor','pointer');
//     btn.click(function (event) {
//         event.preventDefault();
//         var imgTag = $(this).children('img');
//         var oldSrc = imgTag.attr('src');
//         var newSrc = oldSrc + '?xx=' + Math.random();
//         imgTag.attr('src',newSrc);
//     });
// });
