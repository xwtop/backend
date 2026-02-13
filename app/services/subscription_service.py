from app.models import ContentCategorySubscription
from app.extensions import db


class SubscriptionService:
    @staticmethod
    def subscribe(user_id, category_id):
        from app.models.content_category import ContentCategory
        
        category = db.session.query(ContentCategory).filter_by(id=category_id, deleted=0).first()
        if not category:
            return False, '分类不存在'
        
        existing = db.session.query(ContentCategorySubscription).filter_by(
            user_id=user_id,
            category_id=category_id,
            deleted=0
        ).first()
        
        if existing:
            return False, '已订阅该分类'
        
        subscription = ContentCategorySubscription(
            user_id=user_id,
            category_id=category_id,
            create_by=user_id
        )
        db.session.add(subscription)
        db.session.commit()
        
        return True, None

    @staticmethod
    def unsubscribe(user_id, category_id):
        subscription = db.session.query(ContentCategorySubscription).filter_by(
            user_id=user_id,
            category_id=category_id,
            deleted=0
        ).first()
        
        if not subscription:
            return False, '未订阅该分类'
        
        subscription.deleted = 1
        subscription.update_by = user_id
        db.session.commit()
        
        return True, None

    @staticmethod
    def get_user_subscriptions(user_id):
        subscriptions = db.session.query(ContentCategorySubscription).filter_by(
            user_id=user_id,
            deleted=0
        ).all()
        
        items = []
        for subscription in subscriptions:
            items.append({
                'id': subscription.id,
                'categoryId': subscription.category_id,
                'subscribeTime': subscription.create_time.isoformat() if subscription.create_time else None
            })
        
        return items, None

    @staticmethod
    def is_subscribed(user_id, category_id):
        subscription = db.session.query(ContentCategorySubscription).filter_by(
            user_id=user_id,
            category_id=category_id,
            deleted=0
        ).first()
        
        return subscription is not None

    @staticmethod
    def batch_is_subscribed(user_id, category_ids):
        subscriptions = db.session.query(ContentCategorySubscription).filter(
            ContentCategorySubscription.user_id == user_id,
            ContentCategorySubscription.category_id.in_(category_ids),
            ContentCategorySubscription.deleted == 0
        ).all()
        
        subscribed_ids = {sub.category_id for sub in subscriptions}
        result = {}
        for category_id in category_ids:
            result[str(category_id)] = category_id in subscribed_ids
        
        return result

    @staticmethod
    def get_category_subscribers(category_id):
        subscriptions = db.session.query(ContentCategorySubscription).filter_by(
            category_id=category_id,
            deleted=0
        ).all()
        
        return [sub.user_id for sub in subscriptions]
