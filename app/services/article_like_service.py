from app.models import ContentArticleLike, ContentArticle
from app.extensions import db


class ArticleLikeService:
    @staticmethod
    def toggle_like(form_data):
        article_id = form_data.get('article_id')
        user_id = form_data.get('user_id')

        article = db.session.query(ContentArticle).filter_by(id=article_id, deleted=0).first()
        if not article:
            return False, '文章不存在'

        existing_like = db.session.query(ContentArticleLike).filter_by(
            article_id=article_id, user_id=user_id, deleted=0
        ).first()

        if existing_like:
            existing_like.deleted = 1
            article.like_count = max(0, article.like_count - 1)
            db.session.commit()
            return False, None
        else:
            article_like = ContentArticleLike(
                article_id=article_id,
                user_id=user_id
            )
            db.session.add(article_like)
            article.like_count += 1
            db.session.commit()
            return True, None

    @staticmethod
    def check_like(article_id, user_id):
        like = db.session.query(ContentArticleLike).filter_by(
            article_id=article_id, user_id=user_id, deleted=0
        ).first()

        return bool(like), None

    @staticmethod
    def get_article_likes(article_id, page=1, page_size=10):
        query = db.session.query(ContentArticleLike).filter_by(
            article_id=article_id, deleted=0
        ).order_by(ContentArticleLike.create_time.desc())

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        items = []
        for like in pagination.items:
            items.append({
                'id': like.id,
                'articleId': like.article_id,
                'userId': like.user_id,
                'createTime': like.create_time.isoformat() if like.create_time else None
            })

        return {
            'total': pagination.total,
            'items': items,
            'page': page,
            'page_size': page_size
        }, None

    @staticmethod
    def get_user_likes(user_id, page=1, page_size=10):
        query = db.session.query(ContentArticleLike).filter_by(
            user_id=user_id, deleted=0
        ).order_by(ContentArticleLike.create_time.desc())

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        items = []
        for like in pagination.items:
            items.append({
                'id': like.id,
                'articleId': like.article_id,
                'userId': like.user_id,
                'createTime': like.create_time.isoformat() if like.create_time else None
            })

        return {
            'total': pagination.total,
            'items': items,
            'page': page,
            'page_size': page_size
        }, None
