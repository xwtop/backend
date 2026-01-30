from marshmallow import Schema, fields, validate


class BasePageQuery(Schema):
    """分页查询参数基类"""
    page = fields.Integer(missing=1, validate=validate.Range(min=1, max=10000))
    page_size = fields.Integer(missing=10, validate=validate.Range(min=1, max=100))