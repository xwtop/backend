from marshmallow import Schema, fields, validate
from app.schemas.base_page_query import BasePageQuery


class ArticleCommentFormSchema(Schema):
    article_id = fields.Str(required=True, error_messages={'required': '文章ID不能为空'})
    parent_id = fields.Str(allow_none=True)
    user_id = fields.Str(required=True, error_messages={'required': '用户ID不能为空'})
    user_name = fields.Str(allow_none=True)
    user_avatar = fields.Str(allow_none=True)
    content = fields.Str(required=True, error_messages={'required': '评论内容不能为空'})


class ArticleCommentPageQuerySchema(BasePageQuery):
    article_id = fields.Str(required=True, error_messages={'required': '文章ID不能为空'})
