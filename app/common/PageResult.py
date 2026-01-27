import json
from datetime import datetime, date

from flask import Response

from .HttpStatusCode import HttpStatusCode


def json_serializer(obj):
    """自定义JSON序列化器，处理datetime和date对象"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} not serializable')


class PageResult(Response):
    """分页返回结果"""

    def __init__(self, status: int, statusText: str, data: dict):
        body = {
            'status': status,
            'statusText': statusText,
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
    def success(cls, page, statusText: str = "OK", status: int = HttpStatusCode.OK):
        """分页成功返回，page应包含records和total属性"""
        data = {
            'list': page.get('records', page.get('items', [])),  # 兼容不同的数据结构
            'total': page.get('total', 0)
        }
        return cls(status=status, statusText=statusText, data=data)
