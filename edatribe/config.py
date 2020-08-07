"""

工厂函数所需要的配置文件

"""
# 根据不同系统配置数据库路径
import os
import sys

"""

os.path.dirname(__file__)  获取当前文件的路径
os.path.abspath  返回绝对路径

"""
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 获取当前目录的路径

"""

sys.platform  操作系统类型 
startswith  方法用于检查字符串是否是以指定子字符串开头，如果是则返回 True，否则返回 False

"""

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'



# 基本配置
class BaseConfig(object):
    # os.getenv  获取环境变量 若存在为'SECRET_KEY'，否则取默认值'dev key'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    # 要拦截重定向？ 不！
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 可以用于显式地禁用或者启用查询记录。查询记录 在调试或者测试模式下自动启用。
    SQLALCHEMY_RECORD_QUERIES = True



# 开发环境配置
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')



# 测试环境配置
class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 内存型数据库


# 生产环境配置
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))



# 配置字典(配置实例化)
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}