from app.models.base_model import BaseModel
from app.extensions import db


class ContentArticleLike(BaseModel):
    __tablename__ = 'content_article_like'

    article_id = db.Column(db.String(64), nullable=False, comment='文章ID')
    user_id = db.Column(db.String(64), nullable=False, comment='用户ID')
