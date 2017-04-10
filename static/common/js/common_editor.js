/**
 * Created by Administrator on 2017/4/1.
 */
// 初始化编辑器
$(function () {
    var editor = new wangEditor('editor');
    editor.create();
    window.editor = editor;
});


// 初始化七牛的事件
$(function () {
    var progressBox = $('#progress-box');
    var progressBar = progressBox.children(0);
    var uploadBtn = $('#upload-btn');
    xtqiniu.setUp({
       'browse_btn': 'upload-btn',
       'success': function (up,file,info) {
           var fileUrl = file.name;
           if(file.type.indexOf('video') >= 0){
               // 视频
               var videoTag = "<video width='640' height='480' controls><source src="+fileUrl+"></video>";
               window.editor.$txt.append(videoTag);
           }else{
                var imgTag = "<img src="+fileUrl+">"
                window.editor.$txt.append(imgTag);
           }
       },
        // 上传文件显示进度条
       'fileadded': function () {
           progressBox.show();
           uploadBtn.button('loading');
       },
        // 进度条的进度
       'progress': function (up,file) {
           var percent = file.percent;
           progressBar.attr('aria-valuenow',percent);
           progressBar.css('width',percent+'%');
           progressBar.text(percent+'%');
       },
        // 上传完成就把进度条隐藏
       'complete': function () {
           progressBox.hide();
           progressBar.attr('aria-valuenow',0);
           progressBar.css('width','0%');
           progressBar.text('0%');
           uploadBtn.button('reset');
       }
   });
});
