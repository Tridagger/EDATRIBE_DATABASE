# 主页蓝图
from flask import Blueprint


home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    return "这是主页"