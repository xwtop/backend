from enum import Enum


class HttpStatusCode(Enum):
    """HTTP状态码枚举"""
    OK = (200, "OK")
    BAD_REQUEST = (400, "Bad Request")
    UNAUTHORIZED = (401, "Unauthorized")
    FORBIDDEN = (403, "Forbidden")
    NOT_FOUND = (404, "Not Found")
    METHOD_NOT_ALLOWED = (405, "Method Not Allowed")
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"{self.code} {self.message}"

    @property
    def status_code(self):
        return self.code

    @property
    def status_message(self):
        return self.message
