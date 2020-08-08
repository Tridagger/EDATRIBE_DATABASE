# 扩展类实例化
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()  # 数据库实例化
login_manager = LoginManager()  #扩展登录功能
bootstrap = Bootstrap() #扩展Bootstrap
csrf = CSRFProtect() #CSRF保护

# 用户加载函数
@login_manager.user_loader
def load_user(user_id):
    from edatribe.models import Admin
    user = Admin.query.get(int(user_id))
    return user

# 页面保护 -> 登录视图
login_manager.login_view = 'auth.login'