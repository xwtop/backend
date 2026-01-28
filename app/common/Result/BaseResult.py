import json
from datetime import datetime, date

from flask import Response


def json_serializer(obj):
    """自定义JSON序列化器，处理datetime和date对象"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} not serializable')


class BaseResult(Response):
    def __init__(self, body: dict, status: int):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        super().__init__(
            response=json.dumps(body, ensure_ascii=False, default=json_serializer).encode('utf-8'),
            status=status,
            headers=headers,
            mimetype='application/json'
        )
