from flask import Blueprint, request
from marshmallow import ValidationError

from app.common.Results import Result, PageResult
from app.middleware.auth import token_required, permission_required
from app.schemas import ArticleFormSchema, ArticlePageQuerySchema
from app.services.article_service import ArticleService

article_bp = Blueprint('article', __name__)


@article_bp.route('/add', methods=['POST'])
@token_required
@permission_required('normal:add', 'system:add')
def save_article():
    try:
        data = ArticleFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = ArticleService.save_article(data)

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@article_bp.route('/<string:article_id>/update', methods=['PUT'])
@token_required
@permission_required('normal:update', 'system:update')
def update_article(article_id):
    try:
        data = ArticleFormSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = ArticleService.update_article(article_id, data)

    if error:
        return Result.bad_request(error)

    return Result.success(True)


@article_bp.route('/<path:ids>/delete', methods=['DELETE'])
@token_required
@permission_required('normal:delete', 'system:delete')
def delete_article(ids):
    result, error = ArticleService.delete_article(ids)

    if error:
        return Result.server_error(error)

    return Result.success(True)


@article_bp.route('/<string:article_id>/form', methods=['GET'])
@token_required
@permission_required('normal:get', 'system:get')
def get_article_form(article_id):
    result, error = ArticleService.get_article_vo(article_id)

    if error:
        return Result.not_found(error)

    return Result.success(result)


@article_bp.route('/page', methods=['POST'])
@token_required
@permission_required('normal:page', 'system:page')
def page_article():
    try:
        data = ArticlePageQuerySchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = ArticleService.page_article(data)

    if error:
        return Result.server_error(error)

    return PageResult.success(result)


@article_bp.route('/<string:article_id>/publish', methods=['POST'])
@token_required
@permission_required('system:publish')
def publish_article(article_id):
    result, error = ArticleService.publish_article(article_id)

    if error:
        return Result.bad_request(error)

    return Result.success(True)


@article_bp.route('/<string:article_id>/unpublish', methods=['POST'])
@token_required
@permission_required('system:unpublish')
def unpublish_article(article_id):
    result, error = ArticleService.unpublish_article(article_id)

    if error:
        return Result.bad_request(error)

    return Result.success(True)


@article_bp.route('/<string:article_id>/top', methods=['POST'])
@token_required
def set_top(article_id):
    is_top = request.json.get('isTop', 1)
    result, error = ArticleService.set_top(article_id, is_top)

    if error:
        return Result.bad_request(error)

    return Result.success(True)


@article_bp.route('/<string:article_id>/hot', methods=['POST'])
@token_required
def set_hot(article_id):
    is_hot = request.json.get('isHot', 1)
    result, error = ArticleService.set_hot(article_id, is_hot)

    if error:
        return Result.bad_request(error)

    return Result.success(True)


@article_bp.route('/<string:article_id>/view', methods=['POST'])
def increment_view_count(article_id):
    result, error = ArticleService.increment_view_count(article_id)

    if error:
        return Result.bad_request(error)

    return Result.success(True)


@article_bp.route('/hot', methods=['GET'])
def get_hot_articles():
    limit = request.args.get('limit', 10, type=int)
    result, error = ArticleService.get_hot_articles(limit)

    if error:
        return Result.server_error(error)

    return Result.success(result)


@article_bp.route('/top', methods=['GET'])
def get_top_articles():
    limit = request.args.get('limit', 10, type=int)
    result, error = ArticleService.get_top_articles(limit)

    if error:
        return Result.server_error(error)

    return Result.success(result)


@article_bp.route('/rank', methods=['GET'])
def get_rank_articles():
    time_range = request.args.get('time_range', 'daily', type=str)
    limit = request.args.get('limit', 10, type=int)
    result, error = ArticleService.get_rank_articles(time_range, limit)

    if error:
        return Result.server_error(error)

    return Result.success(result)


@article_bp.route('/search', methods=['POST'])
@token_required
def search_articles():
    keyword = request.json.get('keyword', '').strip()
    search_type = request.json.get('search_type', 'all')
    page = request.json.get('page', 1)
    page_size = request.json.get('page_size', 10)

    if not keyword:
        return Result.bad_request('搜索关键词不能为空')

    result, error = ArticleService.search_articles(keyword, search_type, page, page_size)

    if error:
        return Result.server_error(error)

    return Result.success(result)
