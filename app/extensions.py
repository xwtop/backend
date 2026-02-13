from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler

# 导入日志配置
from app.common.config import init_logging

db = SQLAlchemy()  # 数据库
ma = Marshmallow()  # 用于序列化/反序列化数据
socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')  # WebSocket支持
scheduler = BackgroundScheduler()  # 定时任务调度器


def init_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
    # 配置CORS以支持所有来源的跨域请求
    # 设置origins为"*"以允许所有来源
    CORS(app,
         resources={r"/*": {"origins": "*"}},
         supports_credentials=False,  # 当允许所有来源时，不能同时支持凭据
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"])

    # 初始化日志
    init_logging(app)
    
    # 初始化定时任务
    if not scheduler.running:
        from app.tasks.reminder_task import check_reminders
        
        # 每分钟检查一次定时提醒
        scheduler.add_job(
            func=check_reminders,
            args=[app],
            trigger="interval",
            minutes=1,
            id="check_reminders",
            name="检查并发送到期的定时提醒",
            replace_existing=True
        )
        
        scheduler.start()
        print("定时任务调度器已启动")

