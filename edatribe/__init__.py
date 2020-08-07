from flask import Flask
from edatribe.config import config
import os
from edatribe.extensions import db, login_manager
from edatribe.blueprints.admin import admin_bp
from edatribe.blueprints.home import home_bp
from edatribe.blueprints.auth import auth_bp
import click


# 定义工厂函数（工厂函数也是一个函数，config_filename是函数的型参，应用函数时导入实际配置文件。
def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # 从对象导入,配置文件里有个字典对象

    register_extensions(app)  # 注册扩展（扩展初始化）
    register_blueprints(app)  # 注册蓝本
    register_commands(app)  # 注册命令
    return app


# 扩展初始化
def register_extensions(app): 
    db.init_app(app)
    login_manager.init_app(app)



# 蓝本
def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


# 注册命令
def register_commands(app):

    # 注册管理员命令
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
    def admin(username, password):
        """Create user."""
        db.create_all()

        from edatribe.models import Admin
        user = Admin.query.first()
        if user is not None:
            click.echo('Updating user...')
            user.username = username
            user.set_password(password)  # 设置密码
        else:
            click.echo('Creating user...')
            user = Admin(username=username)
            user.set_password(password)  # 设置密码
            db.session.add(user)

        db.session.commit()  # 提交数据库会话
        click.echo('Done.')

    # 初始化数据库命令
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')