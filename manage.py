# -*-coding:utf-8-*-
from exts import db
from mybbs import app
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_assets import ManageAssets
from models import cmsmodels
from models import commonmodels
from models import frontmodels

CMSUser = cmsmodels.CMSUser
CMSRole = cmsmodels.CMSRole

FrontUser = frontmodels.FrontUser

migrate = Migrate(app, db)
manager = Manager(app)
server = Server(port=5000)
manager.add_command('runserver', server)
manager.add_command('db', MigrateCommand)
# manager.add_command('assets', ManageAssets(assets_env))


@manager.option('-e', '--email', dest='email')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_cms_user(email, username, password):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        print u'该用户已经存在！'
        return
    else:
        user = CMSUser(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        print u'添加用户成功!'


@manager.option('-n', '--name', dest='name')
@manager.option('-d', '--desc', dest='desc')
@manager.option('-p', '--permissions', dest='permissions')
def create_role(name, desc, permissions):
    role = CMSRole(name=name.decode('gbk').encode('utf8'), desc=desc.decode('gbk').encode('utf8'), permissions=permissions)
    db.session.add(role)
    db.session.commit()
    print u'添加角色成功!'


@manager.option('-e', '--email', dest='email')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-r', '--role', dest='role')
def create_user_role(email, username, password, role):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        print u'该邮箱已经存在！'
        return
    roles = CMSRole.query.filter_by(name=role.decode('gbk').encode('utf8')).first()
    if not roles:
        print u'该角色不存在！'
        return
    user = CMSUser(email=email, username=username, password=password)
    user.roles.append(roles)
    db.session.add(user)
    db.session.commit()
    print u'添加cms用户与角色成功!'


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_font_user(telephone, username, password):
    user = FrontUser.query.filter_by(telephone=telephone).first()
    if user:
        print u'该用户已经存在！'
        return
    else:
        user = FrontUser(telephone=telephone, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        print u'添加用户成功!'




if __name__ == '__main__':
    manager.run()
