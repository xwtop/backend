from marshmallow import Schema, fields, validate
from app.schemas.base_page_query import BasePageQuery


class SysRoleFormSchema(Schema):
    id = fields.Str(allow_none=True)
    code = fields.Str(required=True, error_messages={'required': '角色编码不能为空'})
    name = fields.Str(required=True, error_messages={'required': '角色名称不能为空'})
    sort = fields.Integer(allow_none=True)
    remark = fields.Str(allow_none=True)
    status = fields.Integer(allow_none=True)
    permission_ids = fields.List(fields.Str(), allow_none=True)


class SysRolePageQuerySchema(BasePageQuery):
    code = fields.Str(allow_none=True)
    name = fields.Str(allow_none=True)
    status = fields.Integer(allow_none=True)

