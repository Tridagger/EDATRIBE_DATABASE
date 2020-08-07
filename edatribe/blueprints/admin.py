# 管理页蓝图
from flask import Blueprint


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
def index():
    return "这是管理页"
