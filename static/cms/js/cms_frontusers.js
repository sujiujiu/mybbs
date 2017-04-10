/**
 * Created by Administrator on 2017/3/24.
 */

$(function () {
   $('.sort-select').change(function (event) {
       var value = $(this).val();
       var newHref = xtparam.setParam(window.location.href,'sort',value);
       window.location = newHref;
   });
});
