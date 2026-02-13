from datetime import datetime

from app.models import ContentArticle, ContentArticleLike
from app.extensions import db
from app.services.notification_service import NotificationService


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
                article.publish_time = datetime.now()
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
        author_id = query_params.get('author_id')
        category_id = query_params.get('category_id')
        title = query_params.get('title')
        status = query_params.get('status')
        is_top = query_params.get('is_top')
        is_hot = query_params.get('is_hot')
        min_view_count = query_params.get('min_view_count')

        query = db.session.query(ContentArticle).filter_by(deleted=0)

        if author_id:
            query = query.filter(ContentArticle.author_id == author_id)
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
        if min_view_count is not None:
            query = query.filter(ContentArticle.view_count >= min_view_count)

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
            article.publish_time = datetime.now()

        db.session.commit()

        NotificationService.notify_category_subscribers(
            category_id=article.category_id,
            article_title=article.title,
            article_id=article.id
        )

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

    @staticmethod
    def get_rank_articles(time_range='daily', limit=10):
        from datetime import datetime, timedelta
        
        # 计算时间范围
        now = datetime.now()
        if time_range == 'daily':
            start_time = now - timedelta(days=1)
        elif time_range == 'weekly':
            start_time = now - timedelta(weeks=1)
        elif time_range == 'monthly':
            start_time = now - timedelta(days=30)
        else:
            start_time = now - timedelta(days=1)
        
        # 查询符合条件的文章
        articles = db.session.query(ContentArticle).filter(
            ContentArticle.deleted == 0,
            ContentArticle.status == 1,
            ContentArticle.publish_time >= start_time
        ).all()
        
        # 计算综合得分并排序
        # 得分计算公式：观看量*0.5 + 点赞数*0.3 + 评论数*0.2
        articles_with_score = []
        for article in articles:
            score = (article.view_count * 0.5) + (article.like_count * 0.3) + (article.comment_count * 0.2)
            articles_with_score.append((score, article))
        
        # 按照得分降序排序
        articles_with_score.sort(key=lambda x: x[0], reverse=True)
        
        # 取前limit个
        top_articles = [article for _, article in articles_with_score[:limit]]
        
        # 转换为前端需要的格式
        items = []
        for i, article in enumerate(top_articles, 1):
            items.append({
                'rank': i,
                'id': article.id,
                'categoryId': article.category_id,
                'title': article.title,
                'subTitle': article.sub_title,
                'coverImage': article.cover_image,
                'authorId': article.author_id,
                'authorName': article.author_name,
                'views': article.view_count,
                'likes': article.like_count,
                'comments': article.comment_count,
                'publishTime': article.publish_time.isoformat() if article.publish_time else None
            })
        
        return items, None

    @staticmethod
    def search_articles(keyword, search_type='all', page=1, page_size=10):
        query = db.session.query(ContentArticle).filter_by(deleted=0, status=1)
        
        # 根据搜索类型进行筛选
        if search_type == 'title':
            query = query.filter(ContentArticle.title.like(f'%{keyword}%'))
        elif search_type == 'content':
            query = query.filter(ContentArticle.content.like(f'%{keyword}%'))
        elif search_type == 'author':
            query = query.filter(ContentArticle.author_name.like(f'%{keyword}%'))
        else:  # all - 搜索标题和内容
            query = query.filter(
                db.or_(
                    ContentArticle.title.like(f'%{keyword}%'),
                    ContentArticle.content.like(f'%{keyword}%')
                )
            )
        
        # 排序：置顶优先，然后按发布时间倒序
        query = query.order_by(ContentArticle.is_top.desc(), ContentArticle.publish_time.desc())
        
        # 分页
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        
        items = []
        for article in pagination.items:
            # 获取分类名称
            category_name = ''
            if article.category_id:
                from app.models.content_category import ContentCategory
                category = db.session.query(ContentCategory).filter_by(id=article.category_id).first()
                if category:
                    category_name = category.name
            
            items.append({
                'id': article.id,
                'title': article.title,
                'summary': article.sub_title if article.sub_title else article.content[:100] + '...',
                'author': article.author_name,
                'publishTime': article.publish_time.strftime('%Y-%m-%d') if article.publish_time else '',
                'category': category_name
            })
        
        return {
            'total': pagination.total,
            'items': items,
            'page': page,
            'page_size': page_size
        }, None
