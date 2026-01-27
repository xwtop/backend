from app.models.base_model import BaseModel
from app.extensions import db


class SysUser(BaseModel):
    # 系统用户模型：存储用户基本信息
    __tablename__ = 'sys_user'
    
    username = db.Column(db.String(64), unique=True, nullable=False, comment='学号')
    password = db.Column(db.String(255), nullable=False, comment='密码哈希')
    real_name = db.Column(db.String(64), nullable=True, comment='真实姓名')
    email = db.Column(db.String(128), nullable=True, comment='邮箱')
    phone = db.Column(db.String(32), nullable=True, comment='手机号')
    avatar = db.Column(db.String(255), nullable=True, comment='头像URL')
    gender = db.Column(db.Integer, default=0, nullable=False, comment='性别（0-未知，1-男，2-女）')
    birthday = db.Column(db.Date, nullable=True, comment='生日')
    introduction = db.Column(db.Text, nullable=True, comment='个人简介')
    status = db.Column(db.Integer, default=1, nullable=False, comment='状态（0禁用，1启用）')
    
    roles = db.relationship('SysRole', secondary='sys_user_role', back_populates='users', lazy='dynamic')
