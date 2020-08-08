# 管理页蓝图
from flask import Blueprint, render_template
from flask_login import login_required


admin_bp = Blueprint('admin', __name__)


# 番剧管理
@admin_bp.route('/anime')
@login_required
def anime():
    return render_template('admin/anime.html')


# 字幕管理 
@admin_bp.route('/cc')
@login_required
def cc():
    return render_template('admin/cc.html')

# 标签管理 
@admin_bp.route('/tab')
@login_required
def tab():
    return render_template('admin/tab.html')

# 标签管理 
@admin_bp.route('/other')
@login_required
def other():
    return render_template('admin/other.html')

# 新增番剧
@admin_bp.route('/post')
@login_required
def post():
    return render_template('admin/post.html')

