# 用户登录认证蓝图
from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from edatribe.forms import LoginForm
from edatribe.models import Admin


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    return "这是登录页"


# 登录
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:  # 没输入用户名或密码
            return redirect(url_for('login'))

        user = Admin.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            return redirect('/')  # 重定向

        return redirect(url_for('auth.login'))  # 重定向回登录页面

    return render_template('auth/login.html')  # 请求为非POST就返回到这里了

# 注销
@auth_bp.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()
    return redirect('/')
