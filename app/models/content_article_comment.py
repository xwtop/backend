from app.models.base_model import BaseModel
from app.extensions import db


class ContentArticleComment(BaseModel):
    __tablename__ = 'content_article_comment'

    article_id = db.Column(db.String(64), nullable=False, comment='文章ID')
    parent_id = db.Column(db.String(64), nullable=True, comment='父评论ID（NULL表示一级评论）')
    user_id = db.Column(db.String(64), nullable=False, comment='评论用户ID')
    user_name = db.Column(db.String(64), nullable=True, comment='评论用户姓名（冗余字段）')
    user_avatar = db.Column(db.String(500), nullable=True, comment='评论用户头像（冗余字段）')
    content = db.Column(db.Text, nullable=False, comment='评论内容')
