from marshmallow import Schema, fields, validate


class ArticleLikeFormSchema(Schema):
    article_id = fields.Str(required=True, error_messages={'required': '文章ID不能为空'})
    user_id = fields.Str(required=True, error_messages={'required': '用户ID不能为空'})
