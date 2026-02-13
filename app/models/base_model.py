from datetime import datetime

from app.extensions import db
from app.common.utils.snowflake import generate_snowflake_id


class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.String(64), primary_key=True, comment='主键ID')
    create_by = db.Column(db.String(64), nullable=True, comment='创建人')
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False, comment='创建时间')
    update_by = db.Column(db.String(64), nullable=True, comment='更新人')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment='更新时间')
    deleted = db.Column(db.Integer, default=0, nullable=False, comment='逻辑删除（0未删除，1已删除）')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.id is None:
            self.id = generate_snowflake_id()
