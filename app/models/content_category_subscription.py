from app.models.base_model import BaseModel
from app.extensions import db


class ContentCategorySubscription(BaseModel):
    __tablename__ = 'content_category_subscription'
    
    user_id = db.Column(db.String(64), nullable=False, comment='用户ID')
    category_id = db.Column(db.String(64), nullable=False, comment='分类ID')
