from datetime import datetime
from app.models import ContentCategorySubscription, Notification
from app.extensions import db
from app.socketio_handlers import send_notification_to_user


class NotificationService:
    @staticmethod
    def create_notification(user_id, title, content, related_id, notification_type='article_new'):
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            content=content,
            related_id=related_id,
            create_by='system',
            create_time=datetime.now()
        )
        db.session.add(notification)
        db.session.commit()
        
        send_notification_to_user(user_id, {
            'id': notification.id,
            'type': notification_type,
            'title': title,
            'content': content,
            'relatedId': related_id,
            'isRead': 0,
            'createTime': notification.create_time.isoformat()
        })
        
        return notification.id

    @staticmethod
    def notify_category_subscribers(category_id, article_title, article_id):
        from app.models.content_category import ContentCategory
        
        print(f'[Notification] 开始通知分类 {category_id} 的订阅者，文章标题：{article_title}')
        
        category = db.session.query(ContentCategory).filter_by(id=category_id, deleted=0).first()
        if not category:
            print(f'[Notification] 分类 {category_id} 不存在')
            return
        
        category_name = category.name
        
        subscriptions = db.session.query(ContentCategorySubscription).filter_by(
            category_id=category_id,
            deleted=0
        ).all()
        
        print(f'[Notification] 找到 {len(subscriptions)} 个订阅者')
        
        for subscription in subscriptions:
            print(f'[Notification] 发送通知给用户 {subscription.user_id}')
            NotificationService.create_notification(
                user_id=subscription.user_id,
                title=f'【{category_name}】新文章发布',
                content=article_title,
                related_id=article_id,
                notification_type='article_new'
            )
        
        print(f'[Notification] 通知发送完成')
        return len(subscriptions)

    @staticmethod
    def get_user_notifications(user_id, unread_only=False):
        query = db.session.query(Notification).filter_by(
            user_id=user_id,
            deleted=0
        )
        
        if unread_only:
            query = query.filter(Notification.is_read == 0)
        
        notifications = query.order_by(Notification.create_time.desc()).all()
        
        items = []
        for notification in notifications:
            items.append({
                'id': notification.id,
                'type': notification.type,
                'title': notification.title,
                'content': notification.content,
                'relatedId': notification.related_id,
                'isRead': notification.is_read,
                'createTime': notification.create_time.isoformat() if notification.create_time else None
            })
        
        return items, None

    @staticmethod
    def mark_as_read(notification_id, user_id):
        notification = db.session.query(Notification).filter_by(
            id=notification_id,
            user_id=user_id,
            deleted=0
        ).first()
        
        if notification:
            notification.is_read = 1
            notification.update_time = datetime.now()
            db.session.commit()
            return True, None
        
        return False, '通知不存在'

    @staticmethod
    def mark_all_as_read(user_id):
        db.session.query(Notification).filter_by(
            user_id=user_id,
            is_read=0,
            deleted=0
        ).update({
            'is_read': 1,
            'update_time': datetime.now()
        }, synchronize_session=False)
        
        db.session.commit()
        return True, None

    @staticmethod
    def get_unread_count(user_id):
        count = db.session.query(Notification).filter_by(
            user_id=user_id,
            is_read=0,
            deleted=0
        ).count()
        
        return count
