from app.models.base_model import BaseModel
from app.extensions import db


class SysUserRole(BaseModel):
    # 用户角色关联模型：建立用户与角色的多对多关系
    __tablename__ = 'sys_user_role'
    
    user_id = db.Column(db.BigInteger, db.ForeignKey('sys_user.id'), nullable=False, comment='用户ID')
    role_id = db.Column(db.BigInteger, db.ForeignKey('sys_role.id'), nullable=False, comment='角色ID')
