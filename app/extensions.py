from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# 导入日志配置
from app.common.config import init_logging

db = SQLAlchemy()  # 数据库
ma = Marshmallow()  # 用于序列化/反序列化数据


def init_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    # 配置CORS以支持所有来源的跨域请求
    # 设置origins为"*"以允许所有来源
    CORS(app,
         resources={r"/*": {"origins": "*"}},
         supports_credentials=False,  # 当允许所有来源时，不能同时支持凭据
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"])

    # 初始化日志
    init_logging(app)
