from app.common.Enum.HttpStatusCode import HttpStatusCode
from app.common.Results.BaseResult import BaseResult


class PageResult(BaseResult):
    """分页返回结果"""

    def __init__(self, status: int, statusText: str, data: dict):
        body = {
            'status': status,
            'statusText': statusText,
            'data': data
        }
        super().__init__(body, status)

    @classmethod
    def success(cls, page, statusText: str = HttpStatusCode.OK.status_message, status: int = HttpStatusCode.OK.status_code):
        """分页成功返回，page应包含records和total属性"""
        data = {
            'list': page.get('records', page.get('items', [])),  # 兼容不同的数据结构
            'total': page.get('total', 0)
        }
        return cls(status=status, statusText=statusText, data=data)
