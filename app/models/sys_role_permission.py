from app.models.base_model import BaseModel
from app.extensions import db


class SysRolePermission(BaseModel):
    # 角色权限关联模型：建立角色与权限的多对多关系
    __tablename__ = 'sys_role_permission'
    
    role_id = db.Column(db.BigInteger, db.ForeignKey('sys_role.id'), nullable=False, comment='角色ID')
    permission_id = db.Column(db.BigInteger, db.ForeignKey('sys_permission.id'), nullable=False, comment='权限ID')
