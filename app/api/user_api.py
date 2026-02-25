from flask import Blueprint, request
from marshmallow import ValidationError

from app.common.Results import Result, PageResult
from app.middleware.auth import token_required, permission_required
from app.schemas import SysUserFormSchema, SysUserPageQuerySchema
from app.services.sys_user_service import SysUserService

user_bp = Blueprint('user', __name__)


@user_bp.route('/add', methods=['POST'])
@token_required
@permission_required('system:add')
def save_sys_user():
    # 添加用户接口：创建新用户

    try:
        data = SysUserFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = SysUserService.save_sys_user(data)

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@user_bp.route('/<string:user_id>/update', methods=['PUT'])
@token_required
@permission_required('normal:update', 'system:update')
def update_sys_user(user_id):
    # 更新用户接口：修改指定用户信息

    try:
        data = SysUserFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = SysUserService.update_sys_user(user_id, data)

    if error:
        return Result.bad_request(error)

    return Result.success(True)


@user_bp.route('/<path:ids>/delete', methods=['DELETE'])
@token_required
@permission_required('system:delete')
def delete_sys_user(ids):
    # 删除用户接口：逻辑删除指定用户
    result, error = SysUserService.delete_sys_user(ids)
    if error:
        return Result.server_error(error)

    return Result.success(True)


@user_bp.route('/<string:user_id>/form', methods=['GET'])
@token_required
@permission_required('normal:get', 'system:get')
def get_sys_user_form(user_id):
    # 获取用户详情接口：根据ID获取用户详细信息
    result, error = SysUserService.get_sys_user_vo(user_id)

    if error:
        return Result.not_found(error)

    return Result.success(result)


@user_bp.route('/page', methods=['POST'])
@token_required
@permission_required('system:page')
def page_sys_user():
    try:
        data = SysUserPageQuerySchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = SysUserService.page_sys_user(data)

    if error:
        return Result.server_error(error)

    # 使用PageResult格式返回分页数据
    return PageResult.success(result)
