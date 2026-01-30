from flask import Blueprint, request
from marshmallow import ValidationError

from app.common.Results import Result, PageResult
from app.middleware.auth import token_required
from app.schemas import ArticleCommentFormSchema, ArticleCommentPageQuerySchema
from app.services.article_comment_service import ArticleCommentService

article_comment_bp = Blueprint('articleComment', __name__)


@article_comment_bp.route('/add', methods=['POST'])
@token_required
def save_comment():
    try:
        data = ArticleCommentFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = ArticleCommentService.save_comment(data)

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@article_comment_bp.route('/<string:comment_id>/delete', methods=['DELETE'])
@token_required
def delete_comment(comment_id):
    result, error = ArticleCommentService.delete_comment(comment_id)

    if error:
        return Result.bad_request(error)

    return Result.success(True)


@article_comment_bp.route('/<string:comment_id>/form', methods=['GET'])
@token_required
def get_comment_form(comment_id):
    result, error = ArticleCommentService.get_comment_vo(comment_id)

    if error:
        return Result.not_found(error)

    return Result.success(result)


@article_comment_bp.route('/page', methods=['POST'])
def page_comment():
    try:
        data = ArticleCommentPageQuerySchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = ArticleCommentService.page_comment(data)

    if error:
        return Result.server_error(error)

    return PageResult.success(result)


@article_comment_bp.route('/article/<string:article_id>/tree', methods=['GET'])
def get_comment_tree(article_id):
    result, error = ArticleCommentService.get_comment_tree(article_id)

    if error:
        return Result.server_error(error)

    return Result.success(result)


@article_comment_bp.route('/user/<string:user_id>', methods=['GET'])
@token_required
def get_user_comments(user_id):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)

    result, error = ArticleCommentService.get_user_comments(user_id, page, page_size)

    if error:
        return Result.server_error(error)

    return PageResult.success(result)
