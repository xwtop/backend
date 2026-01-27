from app.schemas.auth_schema import LoginSchema, RegisterSchema, TokenVOSchema
from app.schemas.user_schema import SysUserFormSchema, SysUserPageQuerySchema, SysUserVOSchema
from app.schemas.role_schema import SysRoleFormSchema, SysRolePageQuerySchema, SysRoleVOSchema
from app.schemas.permission_schema import SysPermissionFormSchema, SysPermissionPageQuerySchema, SysPermissionVOSchema

__all__ = [
    'LoginSchema',
    'RegisterSchema',
    'TokenVOSchema',
    'SysUserFormSchema',
    'SysUserPageQuerySchema',
    'SysUserVOSchema',
    'SysRoleFormSchema',
    'SysRolePageQuerySchema',
    'SysRoleVOSchema',
    'SysPermissionFormSchema',
    'SysPermissionPageQuerySchema',
    'SysPermissionVOSchema',
]
