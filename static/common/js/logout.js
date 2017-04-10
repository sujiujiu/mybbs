/**
 * Created by Administrator on 2017/4/1.
 */

// 确定是否注销，若取消，则取消操作回到原来的位置，若确定，则删除cookie信息，回到未登录的状态
// $(function () {
//    $("#logout-submit").click(function (event) {
//        event.preventDefault();
//        xtalert.alertConfirm({
//            'msg': '确定要注销？',
//            'cancelText': '确定',
//            'confirmText': '取消',
//            'cancelCallback': function () {
//                // 获取并删除cookie信息
//                $.cookie('the_cookie', '', { expires: -1 });
//                window.location = '/';
//                // top.location.href
//            },
//            'confirmCallback': function () {
//                // 取消操作
//                window.event.returnValue = false;
//            }
//        });
//    });
// });