from flask import Blueprint, request
from marshmallow import ValidationError

from app.common.Results import Result, PageResult
from app.middleware.auth import token_required, permission_required
from app.schemas import SysRoleFormSchema, SysRolePageQuerySchema
from app.services.sys_role_service import SysRoleService

role_bp = Blueprint('role', __name__)


@role_bp.route('/add', methods=['POST'])
@token_required
@permission_required('system:add')
def save_sys_role():
    # 添加角色接口：创建新角色

    try:
        data = SysRoleFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = SysRoleService.save_sys_role(data)

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@role_bp.route('/<string:role_id>/update', methods=['PUT'])
@token_required
@permission_required('system:update')
def update_sys_role(role_id):
    # 更新角色接口：修改指定角色信息

    try:
        data = SysRoleFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = SysRoleService.update_sys_role(role_id, data)

    if error:
        return Result.bad_request(error)

    return Result.success(True)


@role_bp.route('/<path:ids>/delete', methods=['DELETE'])
@token_required
@permission_required('system:delete')
def delete_sys_role(ids):
    # 删除角色接口：逻辑删除指定角色

    result, error = SysRoleService.delete_sys_role(ids)

    if error:
        return Result.server_error(error)

    return Result.success(True)


@role_bp.route('/<string:role_id>/form', methods=['GET'])
@token_required
@permission_required('system:get')
def get_sys_role_form(role_id):
    # 获取角色详情接口：根据ID获取角色详细信息

    result, error = SysRoleService.get_sys_role_vo(role_id)

    if error:
        return Result.not_found(error)

    return Result.success(result)


@role_bp.route('/page', methods=['POST'])
@token_required
@permission_required('system:page')
def page_sys_role():
    try:
        data = SysRolePageQuerySchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = SysRoleService.page_sys_role(data)

    if error:
        return Result.server_error(error)

    # 使用PageResult格式返回分页数据
    return PageResult.success(result)


@role_bp.route('/list', methods=['GET'])
@token_required
@permission_required('system:list')
def list_all_roles():
    result, error = SysRoleService.list_all_roles()

    if error:
        return Result.bad_request(error)

    return Result.success(result)
