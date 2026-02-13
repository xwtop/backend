from datetime import datetime, timedelta
from sqlalchemy import func, and_
from app.models.sys_user import SysUser
from app.models.content_article import ContentArticle
from app.models.content_article_comment import ContentArticleComment
from app.models.content_article_like import ContentArticleLike
from app.models.content_category import ContentCategory
from app.extensions import db


class DashboardService:
    @staticmethod
    def get_basic_stats():
        total_users = db.session.query(func.count(SysUser.id)).filter(SysUser.deleted == 0).scalar() or 0
        
        today = datetime.now().date()
        today_new_users = db.session.query(func.count(SysUser.id)).filter(
            and_(
                func.date(SysUser.create_time) == today,
                SysUser.deleted == 0
            )
        ).scalar() or 0
        
        total_articles = db.session.query(func.count(ContentArticle.id)).filter(ContentArticle.deleted == 0).scalar() or 0
        
        today_new_articles = db.session.query(func.count(ContentArticle.id)).filter(
            and_(
                func.date(ContentArticle.create_time) == today,
                ContentArticle.deleted == 0
            )
        ).scalar() or 0
        
        total_comments = db.session.query(func.count(ContentArticleComment.id)).filter(ContentArticleComment.deleted == 0).scalar() or 0
        
        total_likes = db.session.query(func.count(ContentArticleLike.id)).filter(ContentArticleLike.deleted == 0).scalar() or 0
        
        total_views = db.session.query(func.sum(ContentArticle.view_count)).filter(ContentArticle.deleted == 0).scalar() or 0
        
        return {
            'totalUsers': total_users,
            'todayNewUsers': today_new_users,
            'totalArticles': total_articles,
            'todayNewArticles': today_new_articles,
            'totalComments': total_comments,
            'totalLikes': total_likes,
            'totalViews': total_views
        }

    @staticmethod
    def get_user_trend(days=7):
        result = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=days - 1 - i)).date()
            count = db.session.query(func.count(SysUser.id)).filter(
                and_(
                    func.date(SysUser.create_time) == date,
                    SysUser.deleted == 0
                )
            ).scalar() or 0
            result.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })
        return result

    @staticmethod
    def get_article_trend(days=7):
        result = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=days - 1 - i)).date()
            count = db.session.query(func.count(ContentArticle.id)).filter(
                and_(
                    func.date(ContentArticle.create_time) == date,
                    ContentArticle.deleted == 0
                )
            ).scalar() or 0
            result.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })
        return result

    @staticmethod
    def get_view_trend(days=7):
        result = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=days - 1 - i)).date()
            total = db.session.query(func.sum(ContentArticle.view_count)).filter(
                and_(
                    func.date(ContentArticle.create_time) == date,
                    ContentArticle.deleted == 0
                )
            ).scalar() or 0
            result.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': total
            })
        return result

    @staticmethod
    def get_category_stats(limit=10):
        categories = db.session.query(
            ContentCategory.id,
            ContentCategory.name,
            func.count(ContentArticle.id).label('article_count')
        ).outerjoin(
            ContentArticle,
            and_(
                ContentArticle.category_id == ContentCategory.id,
                ContentArticle.deleted == 0
            )
        ).filter(
            ContentCategory.deleted == 0
        ).group_by(
            ContentCategory.id,
            ContentCategory.name
        ).order_by(
            func.count(ContentArticle.id).desc()
        ).limit(limit).all()
        
        return [
            {
                'categoryId': cat.id,
                'categoryName': cat.name,
                'articleCount': cat.article_count
            }
            for cat in categories
        ]

    @staticmethod
    def get_hot_articles(limit=10):
        articles = db.session.query(
            ContentArticle.id,
            ContentArticle.title,
            ContentArticle.view_count,
            ContentArticle.like_count,
            ContentArticle.comment_count,
            ContentCategory.name.label('category_name')
        ).join(
            ContentCategory,
            ContentArticle.category_id == ContentCategory.id
        ).filter(
            and_(
                ContentArticle.deleted == 0,
                ContentArticle.status == 1
            )
        ).order_by(
            ContentArticle.view_count.desc()
        ).limit(limit).all()
        
        return [
            {
                'id': article.id,
                'title': article.title,
                'viewCount': article.view_count,
                'likeCount': article.like_count,
                'commentCount': article.comment_count,
                'categoryName': article.category_name
            }
            for article in articles
        ]

    @staticmethod
    def get_active_users(limit=10):
        users = db.session.query(
            SysUser.id,
            SysUser.username,
            SysUser.real_name,
            func.count(ContentArticle.id).label('article_count'),
            func.sum(ContentArticle.like_count).label('total_likes'),
            func.sum(ContentArticle.comment_count).label('total_comments'),
            func.sum(ContentArticle.view_count).label('total_views')
        ).outerjoin(
            ContentArticle,
            and_(
                ContentArticle.author_id == SysUser.id,
                ContentArticle.deleted == 0
            )
        ).filter(
            SysUser.deleted == 0
        ).group_by(
            SysUser.id,
            SysUser.username,
            SysUser.real_name
        ).order_by(
            func.count(ContentArticle.id).desc()
        ).limit(limit).all()
        
        return [
            {
                'id': user.id,
                'username': user.username,
                'realName': user.real_name,
                'articleCount': user.article_count,
                'totalLikes': user.total_likes or 0,
                'totalComments': user.total_comments or 0,
                'totalViews': user.total_views or 0
            }
            for user in users
        ]

    @staticmethod
    def get_hourly_activity(date=None):
        if date is None:
            date = datetime.now().date()
        
        result = []
        for hour in range(24):
            start_time = datetime.combine(date, datetime.min.time()).replace(hour=hour)
            end_time = start_time + timedelta(hours=1)
            
            article_count = db.session.query(func.count(ContentArticle.id)).filter(
                and_(
                    ContentArticle.create_time >= start_time,
                    ContentArticle.create_time < end_time,
                    ContentArticle.deleted == 0
                )
            ).scalar() or 0
            
            comment_count = db.session.query(func.count(ContentArticleComment.id)).filter(
                and_(
                    ContentArticleComment.create_time >= start_time,
                    ContentArticleComment.create_time < end_time,
                    ContentArticleComment.deleted == 0
                )
            ).scalar() or 0
            
            result.append({
                'hour': f'{hour:02d}:00',
                'articleCount': article_count,
                'commentCount': comment_count
            })
        
        return result
