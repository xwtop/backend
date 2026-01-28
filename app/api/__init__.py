from flask import Blueprint, request, jsonify, g
from app.schemas import LoginSchema, RegisterSchema, TokenVOSchema, SysUserFormSchema, SysUserPageQuerySchema, SysRoleFormSchema, SysRolePageQuerySchema, SysPermissionFormSchema, SysPermissionPageQuerySchema, CategoryFormSchema, CategoryPageQuerySchema
from app.middleware.auth import token_required


# 从子模块导入蓝图
from .auth_api import auth_bp
from .user_api import user_bp
from .role_api import role_bp
from .permission_api import permission_bp
from .category_api import category_bp

__all__ = ['auth_bp', 'user_bp', 'role_bp', 'permission_bp', 'category_bp']
