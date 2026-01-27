from app.models.base_model import BaseModel
from app.extensions import db


class SysPermission(BaseModel):
    # 系统权限模型：定义系统权限信息
    __tablename__ = 'sys_permission'
    
    code = db.Column(db.String(64), unique=True, nullable=False, comment='权限编码')
    name = db.Column(db.String(64), nullable=False, comment='权限名称')
    resource = db.Column(db.String(255), nullable=True, comment='资源标识')
    action = db.Column(db.String(32), nullable=True, comment='操作')
    type = db.Column(db.String(32), nullable=False, comment='类型（API/MENU/BUTTON）')
    remark = db.Column(db.String(255), nullable=True, comment='备注')
    status = db.Column(db.Integer, default=1, nullable=False, comment='状态（0禁用，1启用）')
    
    roles = db.relationship('SysRole', secondary='sys_role_permission', back_populates='permissions', lazy='dynamic')
