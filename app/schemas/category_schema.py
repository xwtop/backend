from marshmallow import Schema, fields, validate
from app.schemas.base_page_query import BasePageQuery


class CategoryFormSchema(Schema):
    id = fields.Str(allow_none=True)
    parent_id = fields.Str(allow_none=True)
    name = fields.Str(required=True, error_messages={'required': '分类名称不能为空'})
    code = fields.Str(required=True, error_messages={'required': '分类编码不能为空'})
    sort = fields.Integer(missing=0, allow_none=True)
    status = fields.Integer(missing=1, allow_none=True)
    remark = fields.Str(allow_none=True)


class CategoryPageQuerySchema(BasePageQuery):
    name = fields.Str(allow_none=True)
    code = fields.Str(allow_none=True)
    status = fields.Integer(allow_none=True)
