# 辅助函数
from flask import request, redirect, url_for, current_app


# 重定向返回上个页面
def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))