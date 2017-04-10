/**
 * Created by Administrator on 2017/3/31.
 */

// 加精和取消加精
$(function () {
    $('.hightlight-btn').click(function (event) {
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        var is_highlight = parseInt($(this).attr('data-is-highlight'));
        xtajax.post({
            'url': '/highlight/',
            'data': {
                'post_id': post_id,
                'is_highlight': !is_highlight
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    if(is_highlight){
                        msg = '取消加精成功！';
                    }else{
                        msg = '加精成功！';
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


// 移除帖子
$(function () {
    $(".remove-btn").click(function (event) {
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        xtajax.post({
            'url': '/remove_post/',
            'data':{
                'post_id': post_id
            },
            'success':function (data) {
                if(data['code'] == 200){
                    var msg = '帖子移除成功！';
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

// 排序的事件
$(function () {
    $('#sort-select').change(function (event) {
       var value = $(this).val();
       var newHref = xtparam.setParam(window.location.href,'sort',value);
       window.location = newHref;
   });
});

// 板块过滤
$(function () {
    $("#board-filter-select").change(function (event) {
       var value = $(this).val();
       var newHref = xtparam.setParam(window.location.href,'board',value);
        var newHref = xtparam.setParam(newHref,'page',1);
       window.location = newHref;
   });
});