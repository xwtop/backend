from app.models.base_model import BaseModel
from app.extensions import db


class ContentCategory(BaseModel):
    __tablename__ = 'content_category'
    
    parent_id = db.Column(db.String(64), nullable=True, comment='父分类ID（NULL表示顶级分类）')
    name = db.Column(db.String(64), nullable=False, comment='分类名称')
    code = db.Column(db.String(64), unique=True, nullable=False, comment='分类编码（唯一标识）')
    sort = db.Column(db.Integer, default=0, nullable=False, comment='排序（数字越小越靠前）')
    status = db.Column(db.Integer, default=1, nullable=False, comment='状态（0禁用，1启用）')
    remark = db.Column(db.String(255), nullable=True, comment='备注')
