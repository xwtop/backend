from marshmallow import Schema, fields, validate
from app.schemas.base_page_query import BasePageQuery


class SubscriptionSchema(Schema):
    user_id = fields.Str(required=True, error_messages={'required': '用户ID不能为空'})
    category_id = fields.Str(required=True, error_messages={'required': '分类ID不能为空'})


class NotificationQuerySchema(BasePageQuery):
    unreadOnly = fields.Boolean(missing=False, allow_none=True)
