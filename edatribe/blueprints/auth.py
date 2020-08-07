# 用户登录认证蓝图
from flask import render_template, flash, redirect, url_for, Blueprint, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from edatribe.forms import LoginForm
from edatribe.models import Admin
from edatribe.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    return "这是登录页"


# 登录
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin)
                flash('Welcome back.', 'info')
                return redirect(url_for('home.index'))
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)

# 注销
@auth_bp.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()
    return redirect('/')
