from marshmallow import Schema, fields, validate
from app.schemas.base_page_query import BasePageQuery


class SysUserFormSchema(Schema):
    id = fields.Str(allow_none=True)
    username = fields.Str(required=True, error_messages={'required': '学号不能为空'})
    password = fields.Str(allow_none=True)
    real_name = fields.Str(required=True, error_messages={'required': '真实姓名不能为空'})
    role_ids = fields.List(fields.Str(), allow_none=True)
    email = fields.Email(required=True, error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式不正确'})
    phone = fields.Str(allow_none=True)
    avatar = fields.Url(allow_none=True)
    gender = fields.Integer(allow_none=True)
    birthday = fields.Date(allow_none=True)
    introduction = fields.Str(allow_none=True)
    status = fields.Integer(allow_none=True)


class SysUserPageQuerySchema(BasePageQuery):
    username = fields.Str(allow_none=True)
    real_name = fields.Str(allow_none=True)
    email = fields.Email(allow_none=True)
    status = fields.Integer(allow_none=True)
