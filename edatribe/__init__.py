from flask import Flask, render_template
from edatribe.config import config
import os
from edatribe.extensions import db, login_manager, bootstrap, csrf
from edatribe.blueprints.admin import admin_bp
from edatribe.blueprints.home import home_bp
from edatribe.blueprints.auth import auth_bp
import click
from flask_wtf.csrf import CSRFError


# 定义工厂函数（工厂函数也是一个函数，config_filename是函数的型参，应用函数时导入实际配置文件。
def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # 从对象导入,配置文件里有个字典对象

    register_extensions(app)  # 注册扩展（扩展初始化）
    register_blueprints(app)  # 注册蓝本
    register_commands(app)  # 注册命令
    register_errors(app) # 注册错误处理
    return app


# 扩展初始化
def register_extensions(app): 
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)



# 蓝本
def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

# 错误处理
def register_errors(app):
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

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

    # 生成测试数据
    @app.cli.command()
    def forge():
        """Generate fake data."""
        db.create_all()
        from edatribe.models import Anime

        # 全局的两个变量移动到这个函数内anime
        anime = [
            {'name_en': 'My Neighbor Totoro', 'filesize': '1988'},
            {'name_en': 'Dead Poets Society', 'filesize': '1989'},
            {'name_en': 'A Perfect World', 'filesize': '1993'},
            {'name_en': 'Leon', 'filesize': '1994'},
            {'name_en': 'Mahjong', 'filesize': '1996'},
            {'name_en': 'Swallowtail Butterfly', 'filesize': '1996'},
            {'name_en': 'King of Comedy', 'filesize': '1999'},
            {'name_en': 'Devils on the Doorstep', 'filesize': '1999'},
            {'name_en': 'WALL-E', 'filesize': '2008'},
            {'name_en': 'The Pork of Music', 'filesize': '2012'},
        ]

        for i in anime:
            anime = Anime(name_en=i['name_en'], filesize=i['filesize'])
            db.session.add(anime)

        db.session.commit()
        click.echo('Done.')