from flask import Blueprint, request, g
from marshmallow import ValidationError

from app.common.Results import Result
from app.middleware.auth import token_required
from app.schemas import NotificationQuerySchema
from app.services.notification_service import NotificationService

notification_bp = Blueprint('notification', __name__)


@notification_bp.route('/list', methods=['GET'])
@token_required
def get_notifications():
    try:
        data = NotificationQuerySchema().load(request.args.to_dict())
    except ValidationError as err:
        return Result.bad_request(str(err.messages))

    unread_only = data.get('unreadOnly', False)
    
    result, error = NotificationService.get_user_notifications(
        user_id=g.user_id,
        unread_only=unread_only
    )

    if error:
        return Result.server_error(error)

    return Result.success(result)


@notification_bp.route('/unread-count', methods=['GET'])
@token_required
def get_unread_count():
    result = NotificationService.get_unread_count(user_id=g.user_id)
    
    return Result.success({'count': result})


@notification_bp.route('/mark-read/<string:notification_id>', methods=['POST'])
@token_required
def mark_as_read(notification_id):
    result, error = NotificationService.mark_as_read(
        notification_id=notification_id,
        user_id=g.user_id
    )

    if error:
        return Result.bad_request(error)

    return Result.success(result)


@notification_bp.route('/mark-all-read', methods=['POST'])
@token_required
def mark_all_as_read():
    result, error = NotificationService.mark_all_as_read(user_id=g.user_id)

    if error:
        return Result.bad_request(error)

    return Result.success(result)
