from marshmallow import Schema, fields, validate
from app.schemas.base_page_query import BasePageQuery


class SysPermissionFormSchema(Schema):
    id = fields.Str(allow_none=True)
    code = fields.Str(required=True, error_messages={'required': '权限编码不能为空'})
    name = fields.Str(required=True, error_messages={'required': '权限名称不能为空'})
    resource = fields.Str(allow_none=True)
    action = fields.Str(allow_none=True)
    type = fields.Str(required=True, error_messages={'required': '权限类型不能为空'})
    remark = fields.Str(allow_none=True)
    status = fields.Integer(allow_none=True)


class SysPermissionPageQuerySchema(BasePageQuery):
    code = fields.Str(allow_none=True)
    name = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True)
    status = fields.Integer(allow_none=True)


