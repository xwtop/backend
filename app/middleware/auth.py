from functools import wraps

from flask import request, g

from app.common.utils.jwt_utils import decode_token
from app.common.Result import Result


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return Result.unauthorized('未提供认证令牌')
        
        payload = decode_token(token)
        if not payload:
            return Result.unauthorized('认证令牌无效或已过期')
        
        g.user_id = payload.get('user_id')
        g.real_name = payload.get('real_name')
        g.roles = payload.get('roles', [])
        
        return f(*args, **kwargs)
    
    return decorated_function


def permission_required(permission_code):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app.models import SysUser
            from app.extensions import db
            
            user = db.session.query(SysUser).filter_by(id=g.user_id, deleted=0).first()
            if not user:
                return Result.forbidden('用户不存在')
            
            has_permission = False
            for role in user.roles:
                if role.status == 1:
                    for permission in role.permissions:
                        if permission.code == permission_code and permission.status == 1:
                            has_permission = True
                            break
                if has_permission:
                    break
            
            if not has_permission:
                return Result.forbidden('权限不足')
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
