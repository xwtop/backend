from app.models.base_model import BaseModel
from app.extensions import db


class Notification(BaseModel):
    __tablename__ = 'notification'
    
    user_id = db.Column(db.String(64), nullable=False, comment='用户ID')
    type = db.Column(db.String(32), nullable=False, comment='通知类型（article_new-新文章，comment_reply-评论回复）')
    title = db.Column(db.String(255), nullable=False, comment='通知标题')
    content = db.Column(db.Text, nullable=True, comment='通知内容')
    related_id = db.Column(db.String(64), nullable=True, comment='关联ID（文章ID、评论ID等）')
    is_read = db.Column(db.Integer, default=0, nullable=False, comment='是否已读（0未读，1已读）')
