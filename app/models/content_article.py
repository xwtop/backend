from app.models.base_model import BaseModel
from app.extensions import db


class ContentArticle(BaseModel):
    __tablename__ = 'content_article'

    category_id = db.Column(db.String(64), nullable=False, comment='分类ID')
    title = db.Column(db.String(255), nullable=False, comment='文章标题')
    sub_title = db.Column(db.String(255), nullable=True, comment='文章副标题')
    content = db.Column(db.Text, nullable=False, comment='文章内容')
    cover_image = db.Column(db.String(500), nullable=True, comment='封面图片URL')
    author_id = db.Column(db.String(64), nullable=False, comment='作者ID（关联用户表）')
    author_name = db.Column(db.String(64), nullable=True, comment='作者姓名（冗余字段，方便查询）')
    view_count = db.Column(db.Integer, default=0, nullable=False, comment='浏览次数')
    like_count = db.Column(db.Integer, default=0, nullable=False, comment='点赞次数（冗余字段，方便查询）')
    comment_count = db.Column(db.Integer, default=0, nullable=False, comment='评论次数（冗余字段，方便查询）')
    is_top = db.Column(db.Integer, default=0, nullable=False, comment='是否置顶（0否，1是）')
    is_hot = db.Column(db.Integer, default=0, nullable=False, comment='是否热门（0否，1是）')
    status = db.Column(db.Integer, default=1, nullable=False, comment='状态（0草稿，1已发布，2已下架）')
    publish_time = db.Column(db.DateTime, nullable=True, comment='发布时间')
