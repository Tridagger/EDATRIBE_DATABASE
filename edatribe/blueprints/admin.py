# 管理页蓝图
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from edatribe.forms import PostForm
from edatribe.extensions import db
from edatribe.models import Anime


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
@admin_bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_post = Anime(name_cn=form.name_cn.data,
                            is_dual=form.is_dual.data,
                            name_en=form.name_en.data,
                            episodes=form.episodes.data,
                            filesize=form.filesize.data)
            db.session.add(new_post)
            db.session.commit()
            flash("success", 'success')
            return redirect(url_for('admin.post'))
    else:
        return render_template('admin/post.html', form=form)

