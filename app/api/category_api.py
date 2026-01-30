from flask import Blueprint, request
from marshmallow import ValidationError

from app.common.Results import Result, PageResult
from app.middleware.auth import token_required
from app.schemas import CategoryFormSchema, CategoryPageQuerySchema
from app.services.category_service import CategoryService

category_bp = Blueprint('category', __name__)


@category_bp.route('/add', methods=['POST'])
@token_required
def save_category():
    try:
        data = CategoryFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = CategoryService.save_category(data)

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@category_bp.route('/<string:category_id>/update', methods=['PUT'])
@token_required
def update_category(category_id):
    try:
        data = CategoryFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = CategoryService.update_category(category_id, data)

    if error:
        return Result.bad_request(error)

    return Result.success(True)


@category_bp.route('/<path:ids>/delete', methods=['DELETE'])
@token_required
def delete_category(ids):
    result, error = CategoryService.delete_category(ids)

    if error:
        return Result.server_error(error)

    return Result.success(True)


@category_bp.route('/<string:category_id>/form', methods=['GET'])
@token_required
def get_category_form(category_id):
    result, error = CategoryService.get_category_vo(category_id)

    if error:
        return Result.not_found(error)

    return Result.success(result)


@category_bp.route('/tree', methods=['GET'])
@token_required
def get_category_tree():
    result, error = CategoryService.get_category_tree()

    if error:
        return Result.server_error(error)

    return Result.success(result)


@category_bp.route('/page', methods=['POST'])
@token_required
def page_category():
    try:
        data = CategoryPageQuerySchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = CategoryService.page_category(data)

    if error:
        return Result.server_error(error)

    return PageResult.success(result)
