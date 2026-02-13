from flask import Blueprint, request
from app.common.Results import Result
from app.middleware.auth import token_required
from app.services.dashboard_service import DashboardService

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/stats', methods=['GET'])
@token_required
def get_stats():
    result = DashboardService.get_basic_stats()
    return Result.success(result)


@dashboard_bp.route('/user-trend', methods=['GET'])
@token_required
def get_user_trend():
    days = request.args.get('days', 7, type=int)
    result = DashboardService.get_user_trend(days)
    return Result.success(result)


@dashboard_bp.route('/article-trend', methods=['GET'])
@token_required
def get_article_trend():
    days = request.args.get('days', 7, type=int)
    result = DashboardService.get_article_trend(days)
    return Result.success(result)


@dashboard_bp.route('/view-trend', methods=['GET'])
@token_required
def get_view_trend():
    days = request.args.get('days', 7, type=int)
    result = DashboardService.get_view_trend(days)
    return Result.success(result)


@dashboard_bp.route('/category-stats', methods=['GET'])
@token_required
def get_category_stats():
    limit = request.args.get('limit', 10, type=int)
    result = DashboardService.get_category_stats(limit)
    return Result.success(result)


@dashboard_bp.route('/hot-articles', methods=['GET'])
@token_required
def get_hot_articles():
    limit = request.args.get('limit', 10, type=int)
    result = DashboardService.get_hot_articles(limit)
    return Result.success(result)


@dashboard_bp.route('/active-users', methods=['GET'])
@token_required
def get_active_users():
    limit = request.args.get('limit', 10, type=int)
    result = DashboardService.get_active_users(limit)
    return Result.success(result)


@dashboard_bp.route('/hourly-activity', methods=['GET'])
@token_required
def get_hourly_activity():
    result = DashboardService.get_hourly_activity()
    return Result.success(result)
