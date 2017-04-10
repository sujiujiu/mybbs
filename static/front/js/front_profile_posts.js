/**
 * Created by Administrator on 2017/4/8.
 */
$(function () {
    $('#post-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        if(!self.hasClass('current')){
            self.addClass('current');
            var post_list = $(".post-list");
            var comment_list = $('.comment-list');
            post_list.show();
            comment_list.hide();
            $('#comment-btn').removeClass('current');
        }
    });
    $('#comment-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        if(!self.hasClass('current')){
            self.addClass('current');
            var post_list = $(".post-list");
            var comment_list = $('.comment-list');
            post_list.hide();
            comment_list.show();
            $('#post-btn').removeClass('current');
        }
    });
});