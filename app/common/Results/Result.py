from typing import Any

from app.common.Enum.HttpStatusCode import HttpStatusCode
from app.common.Results.BaseResult import BaseResult


class Result(BaseResult):
    """统一返回结果"""

    def __init__(self, status: int, status_text: str, data: Any = None):
        body = {
            'status': status,
            'statusText': status_text,
            'data': data
        }
        super().__init__(body, status)

    @classmethod
    def success(cls, data: Any = None, message: str = HttpStatusCode.OK.status_message,
                status_code: int = HttpStatusCode.OK.status_code):
        """成功返回"""
        return cls(status=status_code, status_text=message, data=data)

    @classmethod
    def success_with_message(cls, message: str, data: Any = None):
        """成功返回带消息"""
        return cls(status=HttpStatusCode.OK.status_code, status_text=message, data=data)

    @classmethod
    def bad_request(cls, message: str = HttpStatusCode.BAD_REQUEST.status_message):
        """400错误返回"""
        return cls(status=HttpStatusCode.BAD_REQUEST.status_code, status_text=message, data=None)

    @classmethod
    def unauthorized(cls, message: str = HttpStatusCode.UNAUTHORIZED.status_message):
        """401错误返回"""
        return cls(status=HttpStatusCode.UNAUTHORIZED.status_code, status_text=message, data=None)

    @classmethod
    def forbidden(cls, message: str = HttpStatusCode.FORBIDDEN.status_message):
        """403错误返回"""
        return cls(status=HttpStatusCode.FORBIDDEN.status_code, status_text=message, data=None)

    @classmethod
    def not_found(cls, message: str = HttpStatusCode.NOT_FOUND.status_message):
        """404错误返回"""
        return cls(status=HttpStatusCode.NOT_FOUND.status_code, status_text=message, data=None)

    @classmethod
    def method_not_allowed(cls, message: str = HttpStatusCode.METHOD_NOT_ALLOWED.status_message):
        """405错误返回"""
        return cls(status=HttpStatusCode.METHOD_NOT_ALLOWED.status_code, status_text=message, data=None)

    @classmethod
    def server_error(cls, message: str = HttpStatusCode.INTERNAL_SERVER_ERROR.status_message):
        """500错误返回"""
        return cls(status=HttpStatusCode.INTERNAL_SERVER_ERROR.status_code, status_text=message, data=None)

    @classmethod
    def custom_error(cls, status_code: int, message: str):
        """自定义错误返回"""
        return cls(status=status_code, status_text=message, data=None)
