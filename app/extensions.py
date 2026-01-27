from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# 导入日志配置
from app.config.logger_config import configure_logging

db = SQLAlchemy()  # 数据库
ma = Marshmallow()  # 用于序列化/反序列化数据


def init_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    # 配置CORS以支持OPTIONS请求和其他跨域需求
    # 使用通配符来允许所有来源和方法
    CORS(app,
         resources={r"/*": {"origins": app.config['CORS_ORIGINS']}},
         supports_credentials=True,
         methods=['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE'],
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'])

    # 配置日志
    configure_logging(app)
