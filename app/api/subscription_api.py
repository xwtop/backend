from flask import Blueprint, request
from marshmallow import ValidationError

from app.common.Results import Result
from app.middleware.auth import token_required
from app.schemas import SubscriptionSchema
from app.services.subscription_service import SubscriptionService

subscription_bp = Blueprint('subscription', __name__)


@subscription_bp.route('/subscribe', methods=['POST'])
@token_required
def subscribe():
    try:
        data = SubscriptionSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = SubscriptionService.subscribe(
        user_id=data.get('user_id'),
        category_id=data.get('category_id')
    )

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@subscription_bp.route('/unsubscribe', methods=['POST'])
@token_required
def unsubscribe():
    try:
        data = SubscriptionSchema().load(request.json)
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    result, error = SubscriptionService.unsubscribe(
        user_id=data.get('user_id'),
        category_id=data.get('category_id')
    )

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@subscription_bp.route('/list', methods=['GET'])
@token_required
def get_subscriptions():
    from flask import g
    user_id = g.user_id
    
    result, error = SubscriptionService.get_user_subscriptions(user_id)

    if error:
        return Result.server_error(error)

    return Result.success(result)


@subscription_bp.route('/is-subscribed/<string:category_id>', methods=['GET'])
@token_required
def is_subscribed(category_id):
    from flask import g
    user_id = g.user_id
    
    result = SubscriptionService.is_subscribed(user_id, category_id)
    
    return Result.success({'isSubscribed': result})


@subscription_bp.route('/batch-subscribed', methods=['POST'])
@token_required
def batch_subscribed():
    from flask import g
    user_id = g.user_id
    
    category_ids = request.json.get('category_ids', [])
    if not category_ids:
        return Result.success({})
    
    result = SubscriptionService.batch_is_subscribed(user_id, category_ids)
    
    return Result.success(result)
