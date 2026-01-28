from datetime import datetime

import jwt
from flask import current_app


def generate_token(user_id, real_name, roles):
    # 生成JWT令牌：创建包含用户信息的访问令牌
    payload = {
        'user_id': user_id,
        'real_name': real_name,
        'roles': [role.code for role in roles],
        'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token


def verify_token(token):
    # 验证JWT令牌：检查访问令牌的有效性
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, 'Token已过期'
    except jwt.InvalidTokenError:
        return False, '无效的Token'


def decode_token(token):
    # 解码JWT令牌：解析并验证访问令牌
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
