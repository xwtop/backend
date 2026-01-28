from flask import Blueprint, request
from marshmallow import ValidationError

from app.common.Results import Result, PageResult
from app.middleware.auth import token_required
from app.schemas import SysPermissionFormSchema, SysPermissionPageQuerySchema
from app.services.sys_permission_service import SysPermissionService

permission_bp = Blueprint('permission', __name__)


@permission_bp.route('/tree', methods=['GET'])
@token_required
def get_permission_tree():
    result, error = SysPermissionService.get_permission_tree()

    if error:
        return Result.server_error(error)

    return Result.success(result)


@permission_bp.route('/add', methods=['POST'])
@token_required
def save_sys_permission():
    try:
        data = SysPermissionFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = SysPermissionService.save_sys_permission(data)

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@permission_bp.route('/<string:permission_id>/update', methods=['PUT'])
@token_required
def update_sys_permission(permission_id):
    # 更新权限接口：修改指定权限信息

    try:
        data = SysPermissionFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = SysPermissionService.update_sys_permission(permission_id, data)

    if error:
        return Result.bad_request(error)

    return Result.success(True)


@permission_bp.route('/<path:ids>/delete', methods=['DELETE'])
@token_required
def delete_sys_permission(ids):
    # 删除权限接口：逻辑删除指定权限

    result, error = SysPermissionService.delete_sys_permission(ids)

    if error:
        return Result.server_error(error)

    return Result.success(True)


@permission_bp.route('/<string:permission_id>/form', methods=['GET'])
@token_required
def get_sys_permission_form(permission_id):
    # 获取权限详情接口：根据ID获取权限详细信息

    result, error = SysPermissionService.get_sys_permission_vo(permission_id)

    if error:
        return Result.not_found(error)

    return Result.success(result)


@permission_bp.route('/page', methods=['POST'])
@token_required
def page_sys_permission():
    try:
        data = SysPermissionPageQuerySchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = SysPermissionService.page_sys_permission(data)

    if error:
        return Result.server_error(error)

    # 使用PageResult格式返回分页数据
    return PageResult.success(result)


@permission_bp.route('/list', methods=['GET'])
@token_required
def list_all_permissions():
    # 获取所有未删除的权限列表
    result, error = SysPermissionService.list_all_permissions()

    if error:
        return Result.bad_request(error)

    return Result.success(result)
