from flask import Blueprint, request
from app.common.Results import Result
from app.middleware.auth import token_required
from app.services.recommendation_service import RecommendationService

recommendation_bp = Blueprint('recommendation', __name__)


@recommendation_bp.route('/personalized', methods=['GET'])
@token_required
def get_personalized_recommendations():
    """
    获取个性化推荐
    """
    try:
        # 从请求中获取用户ID（通过token解析）
        from flask import g
        user_id = g.user_id
        
        result, error = RecommendationService.get_personalized_recommendations(user_id)
        
        if error:
            return Result.server_error(error)
        
        return Result.success(result)
    except Exception as e:
        return Result.server_error(str(e))
