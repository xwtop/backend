from flask import Blueprint, request, g
from marshmallow import ValidationError

from app.common.Results import Result
from app.middleware.auth import token_required
from app.schemas import LoginSchema, RegisterSchema, ChangePasswordSchema
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    # 用户登录接口：验证用户名密码并返回访问令牌
    try:
        data = LoginSchema().load(request.json)
    except ValidationError as err:

        return Result.bad_request(str(err.messages))

    result, error = AuthService.login(data['username'], data['password'])

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@auth_bp.route('/register', methods=['POST'])
def register():
    # 用户注册接口：创建新用户账户
    try:
        data = RegisterSchema().load(request.json)
    except ValidationError as err:

        return Result.bad_request(str(err.messages))

    result, error = AuthService.register(
        data['username'],
        data['password'],
        data['real_name'],
        data['email'],
        data['email_code']
    )

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    # 用户登出接口：处理用户退出登录
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
    else:
        token = None

    result, error = AuthService.logout(token)

    if error:
        return Result.server_error(error).to_json()

    return Result.success()


@auth_bp.route('/changePassword', methods=['POST'])
@token_required
def change_password():
    # 修改密码接口：用户修改自己的密码
    try:
        data = ChangePasswordSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    # 验证新密码和确认密码是否一致
    if data['new_password'] != data['confirm_password']:
        return Result.bad_request('新密码和确认密码不一致')

    result, error = AuthService.change_password(g.user_id, data['old_password'], data['new_password'])

    if error:
        return Result.bad_request(error)

    return Result.success(True)
