from datetime import datetime

from app.models import ContentArticle, ContentArticleLike
from app.extensions import db


class ArticleService:
    @staticmethod
    def save_article(form_data):
        article = ContentArticle(
            category_id=form_data.get('category_id'),
            title=form_data.get('title'),
            sub_title=form_data.get('sub_title'),
            content=form_data.get('content'),
            cover_image=form_data.get('cover_image'),
            author_id=form_data.get('author_id'),
            author_name=form_data.get('author_name'),
            is_top=form_data.get('is_top', 0),
            is_hot=form_data.get('is_hot', 0),
            status=form_data.get('status', 0),
            publish_time=form_data.get('publish_time')
        )

        db.session.add(article)
        db.session.commit()

        return article.id, None

    @staticmethod
    def update_article(article_id, form_data):
        article = db.session.query(ContentArticle).filter_by(id=article_id, deleted=0).first()
        if not article:
            return False, '文章不存在'

        if 'category_id' in form_data:
            article.category_id = form_data['category_id']
        if 'title' in form_data:
            article.title = form_data['title']
        if 'sub_title' in form_data:
            article.sub_title = form_data['sub_title']
        if 'content' in form_data:
            article.content = form_data['content']
        if 'cover_image' in form_data:
            article.cover_image = form_data['cover_image']
        if 'author_id' in form_data:
            article.author_id = form_data['author_id']
        if 'author_name' in form_data:
            article.author_name = form_data['author_name']
        if 'is_top' in form_data:
            article.is_top = form_data['is_top']
        if 'is_hot' in form_data:
            article.is_hot = form_data['is_hot']
        if 'status' in form_data:
            article.status = form_data['status']
            if form_data['status'] == 1 and not article.publish_time:
                article.publish_time = datetime.utcnow()
        if 'publish_time' in form_data:
            article.publish_time = form_data['publish_time']

        db.session.commit()

        return True, None

    @staticmethod
    def delete_article(ids_str):
        ids = [id_str.strip() for id_str in ids_str.split(',') if id_str.strip()]

        db.session.query(ContentArticle).filter(
            ContentArticle.id.in_(ids)
        ).update({
            'deleted': 1
        }, synchronize_session=False)

        db.session.commit()

        return True, None

    @staticmethod
    def get_article_vo(article_id):
        article = db.session.query(ContentArticle).filter_by(id=article_id, deleted=0).first()
        if not article:
            return None, '文章不存在'

        return {
            'id': article.id,
            'categoryId': article.category_id,
            'title': article.title,
            'subTitle': article.sub_title,
            'content': article.content,
            'coverImage': article.cover_image,
            'authorId': article.author_id,
            'authorName': article.author_name,
            'viewCount': article.view_count,
            'likeCount': article.like_count,
            'commentCount': article.comment_count,
            'isTop': article.is_top,
            'isHot': article.is_hot,
            'status': article.status,
            'publishTime': article.publish_time.isoformat() if article.publish_time else None,
            'createTime': article.create_time.isoformat() if article.create_time else None,
            'updateTime': article.update_time.isoformat() if article.update_time else None
        }, None

    @staticmethod
    def increment_view_count(article_id):
        article = db.session.query(ContentArticle).filter_by(id=article_id, deleted=0).first()
        if not article:
            return False, '文章不存在'

        article.view_count += 1
        db.session.commit()

        return True, None

    @staticmethod
    def page_article(query_params):
        page = query_params.get('page', 1)
        page_size = query_params.get('page_size', 10)
        category_id = query_params.get('category_id')
        title = query_params.get('title')
        status = query_params.get('status')
        is_top = query_params.get('is_top')
        is_hot = query_params.get('is_hot')

        query = db.session.query(ContentArticle).filter_by(deleted=0)

        if category_id:
            query = query.filter(ContentArticle.category_id == category_id)
        if title:
            query = query.filter(ContentArticle.title.like(f'%{title}%'))
        if status is not None:
            query = query.filter(ContentArticle.status == status)
        if is_top is not None:
            query = query.filter(ContentArticle.is_top == is_top)
        if is_hot is not None:
            query = query.filter(ContentArticle.is_hot == is_hot)

        query = query.order_by(ContentArticle.is_top.desc(), ContentArticle.publish_time.desc())

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        items = []
        for article in pagination.items:
            items.append({
                'id': article.id,
                'categoryId': article.category_id,
                'title': article.title,
                'subTitle': article.sub_title,
                'coverImage': article.cover_image,
                'authorId': article.author_id,
                'authorName': article.author_name,
                'viewCount': article.view_count,
                'likeCount': article.like_count,
                'commentCount': article.comment_count,
                'isTop': article.is_top,
                'isHot': article.is_hot,
                'status': article.status,
                'publishTime': article.publish_time.isoformat() if article.publish_time else None,
                'createTime': article.create_time.isoformat() if article.create_time else None,
                'updateTime': article.update_time.isoformat() if article.update_time else None
            })

        return {
            'total': pagination.total,
            'items': items,
            'page': page,
            'page_size': page_size
        }, None

    @staticmethod
    def publish_article(article_id):
        article = db.session.query(ContentArticle).filter_by(id=article_id, deleted=0).first()
        if not article:
            return False, '文章不存在'

        article.status = 1
        if not article.publish_time:
            article.publish_time = datetime.utcnow()

        db.session.commit()

        return True, None

    @staticmethod
    def unpublish_article(article_id):
        article = db.session.query(ContentArticle).filter_by(id=article_id, deleted=0).first()
        if not article:
            return False, '文章不存在'

        article.status = 2

        db.session.commit()

        return True, None

    @staticmethod
    def set_top(article_id, is_top):
        article = db.session.query(ContentArticle).filter_by(id=article_id, deleted=0).first()
        if not article:
            return False, '文章不存在'

        article.is_top = is_top

        db.session.commit()

        return True, None

    @staticmethod
    def set_hot(article_id, is_hot):
        article = db.session.query(ContentArticle).filter_by(id=article_id, deleted=0).first()
        if not article:
            return False, '文章不存在'

        article.is_hot = is_hot

        db.session.commit()

        return True, None

    @staticmethod
    def get_hot_articles(limit=10):
        articles = db.session.query(ContentArticle).filter_by(
            deleted=0, status=1, is_hot=1
        ).order_by(
            ContentArticle.view_count.desc()
        ).limit(limit).all()

        items = []
        for article in articles:
            items.append({
                'id': article.id,
                'categoryId': article.category_id,
                'title': article.title,
                'subTitle': article.sub_title,
                'coverImage': article.cover_image,
                'authorId': article.author_id,
                'authorName': article.author_name,
                'viewCount': article.view_count,
                'likeCount': article.like_count,
                'commentCount': article.comment_count,
                'isTop': article.is_top,
                'isHot': article.is_hot,
                'status': article.status,
                'publishTime': article.publish_time.isoformat() if article.publish_time else None
            })

        return items, None

    @staticmethod
    def get_top_articles(limit=10):
        articles = db.session.query(ContentArticle).filter_by(
            deleted=0, status=1, is_top=1
        ).order_by(
            ContentArticle.publish_time.desc()
        ).limit(limit).all()

        items = []
        for article in articles:
            items.append({
                'id': article.id,
                'categoryId': article.category_id,
                'title': article.title,
                'subTitle': article.sub_title,
                'coverImage': article.cover_image,
                'authorId': article.author_id,
                'authorName': article.author_name,
                'viewCount': article.view_count,
                'likeCount': article.like_count,
                'commentCount': article.comment_count,
                'isTop': article.is_top,
                'isHot': article.is_hot,
                'status': article.status,
                'publishTime': article.publish_time.isoformat() if article.publish_time else None
            })

        return items, None
