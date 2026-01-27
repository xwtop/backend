from app.models.base_model import BaseModel
from app.extensions import db


class SysRole(BaseModel):
    # 系统角色模型：定义用户角色信息
    __tablename__ = 'sys_role'
    
    code = db.Column(db.String(64), unique=True, nullable=False, comment='角色编码')
    name = db.Column(db.String(64), nullable=False, comment='角色名称')
    sort = db.Column(db.Integer, default=0, nullable=False, comment='显示顺序')
    remark = db.Column(db.String(255), nullable=True, comment='备注')
    status = db.Column(db.Integer, default=1, nullable=False, comment='状态（0禁用，1启用）')
    
    users = db.relationship('SysUser', secondary='sys_user_role', back_populates='roles', lazy='dynamic')
    permissions = db.relationship('SysPermission', secondary='sys_role_permission', back_populates='roles', lazy='dynamic')
