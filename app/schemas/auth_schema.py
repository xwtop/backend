from marshmallow import Schema, fields


class LoginSchema(Schema):
    username = fields.Str(required=True, error_messages={'required': '学号不能为空'})
    password = fields.Str(required=True, error_messages={'required': '密码不能为空'})


class RegisterSchema(Schema):
    username = fields.Str(required=True, error_messages={'required': '学号不能为空'})
    password = fields.Str(required=True, error_messages={'required': '密码不能为空'})
    real_name = fields.Str(required=True, error_messages={'required': '真实姓名不能为空'})
    email = fields.Str(required=True, error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式不正确'})
    email_code = fields.Str(required=True, error_messages={'required': '邮箱验证码不能为空'})


class TokenVOSchema(Schema):
    access_token = fields.Str(data_key='accessToken')
    real_name = fields.Str(data_key='realName')
    role = fields.List(fields.Str(), data_key='role')
