from marshmallow import Schema, fields, validate
from app.schemas.base_page_query import BasePageQuery


class ArticleFormSchema(Schema):
    id = fields.Str(allow_none=True)
    category_id = fields.Str(required=True, error_messages={'required': '分类ID不能为空'})
    title = fields.Str(required=True, error_messages={'required': '文章标题不能为空'})
    sub_title = fields.Str(allow_none=True)
    content = fields.Str(required=True, error_messages={'required': '文章内容不能为空'})
    cover_image = fields.Str(allow_none=True)
    author_id = fields.Str(required=True, error_messages={'required': '作者ID不能为空'})
    author_name = fields.Str(allow_none=True)
    is_top = fields.Integer(missing=0, allow_none=True)
    is_hot = fields.Integer(missing=0, allow_none=True)
    status = fields.Integer(missing=1, allow_none=True)
    publish_time = fields.DateTime(allow_none=True)


class ArticlePageQuerySchema(BasePageQuery):
    author_id = fields.Str(allow_none=True)
    category_id = fields.Str(allow_none=True)
    title = fields.Str(allow_none=True)
    status = fields.Integer(allow_none=True)
    is_top = fields.Integer(allow_none=True)
    is_hot = fields.Integer(allow_none=True)


class ArticlePublishSchema(Schema):
    id = fields.Str(required=True, error_messages={'required': '文章ID不能为空'})
