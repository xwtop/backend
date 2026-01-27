import json
from datetime import datetime, date
from typing import Any

from flask import Response

from .HttpStatusCode import HttpStatusCode


def json_serializer(obj):
    """自定义JSON序列化器，处理datetime和date对象"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} not serializable')


class Result(Response):
    """统一返回结果"""

    def __init__(self, status: int, status_text: str, data: Any = None):
        body = {
            'status': status,
            'statusText': status_text,
            'data': data
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        super().__init__(
            response=json.dumps(body, ensure_ascii=False, default=json_serializer).encode('utf-8'),
            status=status,
            headers=headers,
            mimetype='application/json'
        )

    @classmethod
    def success(cls, data: Any = None, message: str = "success", status_code: int = HttpStatusCode.OK):
        """成功返回"""
        return cls(status=status_code, status_text=message, data=data)

    @classmethod
    def success_with_message(cls, message: str, data: Any = None):
        """成功返回带消息"""
        return cls(status=HttpStatusCode.OK, status_text=message, data=data)

    @classmethod
    def bad_request(cls, message: str = "Bad Request"):
        """400错误返回"""
        return cls(status=HttpStatusCode.BAD_REQUEST, status_text=message, data=None)

    @classmethod
    def unauthorized(cls, message: str = "Unauthorized"):
        """401错误返回"""
        return cls(status=HttpStatusCode.UNAUTHORIZED, status_text=message, data=None)

    @classmethod
    def forbidden(cls, message: str = "Forbidden"):
        """403错误返回"""
        return cls(status=HttpStatusCode.FORBIDDEN, status_text=message, data=None)

    @classmethod
    def not_found(cls, message: str = "Not Found"):
        """404错误返回"""
        return cls(status=HttpStatusCode.NOT_FOUND, status_text=message, data=None)

    @classmethod
    def method_not_allowed(cls, message: str = "Method Not Allowed"):
        """405错误返回"""
        return cls(status=HttpStatusCode.METHOD_NOT_ALLOWED, status_text=message, data=None)

    @classmethod
    def server_error(cls, message: str = "Internal Server Error"):
        """500错误返回"""
        return cls(status=HttpStatusCode.INTERNAL_SERVER_ERROR, status_text=message, data=None)

    @classmethod
    def custom_error(cls, status_code: int, message: str):
        """自定义错误返回"""
        return cls(status=status_code, status_text=message, data=None)
