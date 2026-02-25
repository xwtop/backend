from flask import Blueprint, request
from marshmallow import ValidationError

from app.common.Results import Result, PageResult
from app.middleware.auth import token_required
from app.schemas import ArticleLikeFormSchema
from app.services.article_like_service import ArticleLikeService

article_like_bp = Blueprint('articleLike', __name__)


@article_like_bp.route('/toggle', methods=['POST'])
@token_required
def toggle_like():
    try:
        data = ArticleLikeFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = ArticleLikeService.toggle_like(data)

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@article_like_bp.route('/check', methods=['POST'])
@token_required
def check_like():
    try:
        data = ArticleLikeFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    article_id = data.get('article_id')
    user_id = data.get('user_id')

    result, error = ArticleLikeService.check_like(article_id, user_id)

    if error:
        return Result.server_error(error)

    return Result.success(result)


@article_like_bp.route('/article/<string:article_id>', methods=['GET'])
@token_required
def get_article_likes(article_id):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)

    result, error = ArticleLikeService.get_article_likes(article_id, page, page_size)

    if error:
        return Result.server_error(error)

    return PageResult.success(result)


@article_like_bp.route('/user/<string:user_id>', methods=['GET'])
@token_required
def get_user_likes(user_id):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)

    result, error = ArticleLikeService.get_user_likes(user_id, page, page_size)

    if error:
        return Result.server_error(error)

    return PageResult.success(result)
