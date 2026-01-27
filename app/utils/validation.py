from marshmallow import validate
import re


def validate_username(value):
    """验证用户名格式（学号），只允许字母、数字和下划线，长度6-32位"""
    if not re.match(r'^[a-zA-Z0-9_]{6,32}$', value):
        raise ValueError('用户名必须为6-32位字母、数字或下划线')


def validate_password(value):
    """验证密码强度，至少8位，包含大小写字母、数字和特殊字符"""
    if value is None:
        return  # 允许密码为空（更新时可能不更改密码）
    if len(value) < 8:
        raise ValueError('密码长度至少8位')
    if not re.search(r'[a-z]', value):
        raise ValueError('密码必须包含小写字母')
    if not re.search(r'[A-Z]', value):
        raise ValueError('密码必须包含大写字母')
    if not re.search(r'\d', value):
        raise ValueError('密码必须包含数字')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValueError('密码必须包含特殊字符')


def validate_phone(value):
    """验证手机号格式"""
    if value and not re.match(r'^1[3-9]\d{9}$', value):
        raise ValueError('手机号格式不正确')


def validate_real_name(value):
    """验证真实姓名"""
    if not value or len(value.strip()) == 0:
        raise ValueError('真实姓名不能为空')
    if len(value.strip()) > 50:
        raise ValueError('真实姓名不能超过50个字符')


def validate_code(value):
    """验证编码格式，只允许字母、数字、冒号、连字符和下划线"""
    if not re.match(r'^[a-zA-Z0-9:_\-]+$', value):
        raise ValueError('编码只能包含字母、数字、冒号、连字符和下划线')


def validate_name(value):
    """验证名称格式"""
    if not value or len(value.strip()) == 0:
        raise ValueError('名称不能为空')
    if len(value.strip()) > 64:
        raise ValueError('名称不能超过64个字符')


def validate_email(value):
    """验证邮箱格式"""
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        raise ValueError('邮箱格式不正确')