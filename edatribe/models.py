"""

这里说数据模型

"""
from datetime import datetime
from edatribe.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# 管理员模型
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

# 密码进行哈希加密存储
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 番剧模型
class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_cn = db.Column(db.String)
    name_en = db.Column(db.String)
    episodes = db.Column(db.Integer)
    filesize = db.Column(db.Integer)  # 字节
    update_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_dual = db.Column(db.Boolean)
    
