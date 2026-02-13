from app.extensions import db
from app.models.base_model import BaseModel


class NotificationReminder(BaseModel):
    __tablename__ = 'notification_reminders'

    title = db.Column(db.String(255), nullable=False, comment='提醒标题')
    content = db.Column(db.Text, nullable=False, comment='提醒内容')
    remind_time = db.Column(db.DateTime, nullable=False, comment='提醒时间')
    repeat = db.Column(db.SmallInteger, nullable=False, default=0, comment='重复方式（0-一次性，1-每天，2-每周，3-每月）')
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='状态（1-启用，0-禁用）')
    target_type = db.Column(db.SmallInteger, nullable=False, default=0, comment='目标类型（0-全员，1-指定角色）')
    target_role = db.Column(db.String(50), nullable=True, comment='目标角色代码（当target_type为1时必填）')
