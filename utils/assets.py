# -*-coding:utf-8-*-
from flask_assets import Bundle

bundles = {
    'cms_css': Bundle(
        'cms/css/cms_base.css',
        'cms/css/cms_cmsuser.css',
        'cms/css/lib/ie10-viewport-bug-workaround.css',
        # output为打包后的存放路径，所有路径前缀为/static/
        output='assets/js/cms.css',
        filters='cssmin'

    ),
    'cms_js': Bundle(
        'cms/js/cms_addcmsuser.js',
        'cms/js/cms_base.js',
        'cms/js/cms_edit_user.js',
        'cms/js/cms_resetmail.js',
        'cms/js/cms_resetpwd.js',
        'cms/js/cms_login.js',
        'cms/js/lib/ie10-viewport-bug-workaround.js',
        'cms/js/lib/ie-emulation-modes-warning.js',
        output='assets/js/cms.js',
        filters='jsmin'
    ),
    'common_css': Bundle(
        'common/css/lib/sweetalert.css',
        output='assets/js/common.css',
        filters='cssmin'
    ),
    'common_js': Bundle(
        'common/js/xtajax.js',
        'common/js/xtalert.js',
        'common/js/lib/sweetalert.min.js',
        output='assets/js/common.js',
        filters='jsmin'

    )
}

# cms_css = Bundle(
#     'cms/css/cms_base.css',
#     'cms/css/cms_cmsuser.css',
#     'cms/css/signin.css',
#     'cms/css/lib/ie10-viewport-bug-workaround.css',
#     # output为打包后的存放路径，所有路径前缀为/static/
#     output='assets/js/cms.css',
#     filters='cssmin'
# )
# cms_js = Bundle(
#     'cms/js/cms_addcmsuser.js',
#     'cms/js/cms_base.js',
#     'cms/js/cms_edit_user.js',
#     'cms/js/cms_resetmail.js',
#     'cms/js/cms_resetpwd.js',
#     'cms/js/cms_login.js',
#     'cms/js/lib/ie10-viewport-bug-workaround.js',
#     'cms/js/lib/ie-emulation-modes-warning.js',
#     output='assets/js/cms.js',
#     filters='jsmin'
# )
# common_css = Bundle(
#     'common/css/lib/sweetalert.css',
#     output='assets/js/common.css',
#     filters='cssmin'
# )
# common_js = Bundle(
#     'common/js/xtajax.js',
#     'common/js/xtalert.js',
#     'common/js/lib/sweetalert.min.js',
#     output='assets/js/common.js',
#     filters='jsmin'
#
# )

