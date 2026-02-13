from app.models.content_article import ContentArticle
from app.models.content_article_like import ContentArticleLike
from app.models.content_article_comment import ContentArticleComment
from app.models.content_category_subscription import ContentCategorySubscription
from app.extensions import db
import math
from collections import defaultdict


class RecommendationService:
    @staticmethod
    def get_personalized_recommendations(user_id, limit=20):
        """
        获取个性化推荐
        基于用户的点赞、评论、订阅和浏览行为
        """
        try:
            # 1. 获取用户的历史行为数据
            user_behavior = RecommendationService._get_user_behavior(user_id)
            
            if not user_behavior:
                # 如果用户没有历史行为，返回热门文章
                return RecommendationService._get_hot_articles(limit), None
            
            # 2. 基于用户的协同过滤
            user_based_recommendations = RecommendationService._user_based_collaborative_filtering(user_id, limit)
            
            # 3. 基于物品的协同过滤
            item_based_recommendations = RecommendationService._item_based_collaborative_filtering(user_id, limit)
            
            # 4. 结合两种推荐结果
            recommendations = RecommendationService._combine_recommendations(
                user_based_recommendations, item_based_recommendations, limit
            )
            
            return recommendations, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def _get_user_behavior(user_id):
        """
        获取用户的历史行为数据
        """
        behavior = {
            'liked_articles': [],
            'commented_articles': [],
            'subscribed_categories': [],
            'viewed_articles': []
        }
        
        # 获取用户点赞的文章
        liked_articles = db.session.query(ContentArticleLike.article_id).filter(
            ContentArticleLike.user_id == user_id
        ).all()
        behavior['liked_articles'] = [item[0] for item in liked_articles]
        
        # 获取用户评论的文章
        commented_articles = db.session.query(ContentArticleComment.article_id).filter(
            ContentArticleComment.user_id == user_id
        ).distinct().all()
        behavior['commented_articles'] = [item[0] for item in commented_articles]
        
        # 获取用户订阅的分类
        subscribed_categories = db.session.query(ContentCategorySubscription.category_id).filter(
            ContentCategorySubscription.user_id == user_id
        ).all()
        behavior['subscribed_categories'] = [item[0] for item in subscribed_categories]
        
        # 获取用户浏览的文章（这里简化处理，实际应该有浏览记录）
        # 暂时使用点赞和评论的文章作为浏览记录
        behavior['viewed_articles'] = list(set(behavior['liked_articles'] + behavior['commented_articles']))
        
        return behavior
    
    @staticmethod
    def _user_based_collaborative_filtering(user_id, limit):
        """
        基于用户的协同过滤
        """
        # 获取用户的历史行为
        user_behavior = RecommendationService._get_user_behavior(user_id)
        user_articles = list(set(user_behavior['liked_articles'] + user_behavior['commented_articles']))
        
        if not user_articles:
            return []
        
        # 1. 找到有相似行为的用户
        similar_users = RecommendationService._find_similar_users(user_id, user_articles)
        
        if not similar_users:
            return []
        
        # 2. 获取相似用户喜欢的文章
        recommended_articles = []
        for similar_user, similarity in similar_users:
            # 获取相似用户点赞的文章
            similar_user_likes = db.session.query(ContentArticleLike.article_id).filter(
                ContentArticleLike.user_id == similar_user
            ).all()
            similar_user_articles = [item[0] for item in similar_user_likes]
            
            # 排除用户已经看过的文章
            for article_id in similar_user_articles:
                if article_id not in user_articles:
                    recommended_articles.append((article_id, similarity))
        
        # 3. 按相似度排序并去重
        recommended_articles = sorted(recommended_articles, key=lambda x: x[1], reverse=True)
        unique_articles = []
        seen_articles = set()
        
        for article_id, similarity in recommended_articles:
            if article_id not in seen_articles:
                unique_articles.append(article_id)
                seen_articles.add(article_id)
                if len(unique_articles) >= limit:
                    break
        
        # 4. 获取文章详情
        return RecommendationService._get_articles_by_ids(unique_articles)
    
    @staticmethod
    def _item_based_collaborative_filtering(user_id, limit):
        """
        基于物品的协同过滤
        """
        # 获取用户的历史行为
        user_behavior = RecommendationService._get_user_behavior(user_id)
        user_articles = list(set(user_behavior['liked_articles'] + user_behavior['commented_articles']))
        
        if not user_articles:
            return []
        
        # 1. 计算文章相似度
        article_similarities = defaultdict(float)
        
        for article_id in user_articles:
            similar_articles = RecommendationService._find_similar_articles(article_id)
            for similar_article, similarity in similar_articles:
                if similar_article not in user_articles:
                    article_similarities[similar_article] += similarity
        
        # 2. 按相似度排序
        sorted_articles = sorted(article_similarities.items(), key=lambda x: x[1], reverse=True)
        
        # 3. 获取推荐文章ID
        recommended_article_ids = [article_id for article_id, _ in sorted_articles[:limit]]
        
        # 4. 获取文章详情
        return RecommendationService._get_articles_by_ids(recommended_article_ids)
    
    @staticmethod
    def _find_similar_users(user_id, user_articles, top_n=10):
        """
        找到与目标用户相似的用户
        """
        # 获取所有与目标用户有共同文章行为的用户
        similar_users = defaultdict(int)
        
        # 通过点赞行为查找相似用户
        for article_id in user_articles:
            users_who_liked = db.session.query(ContentArticleLike.user_id).filter(
                ContentArticleLike.article_id == article_id, 
                ContentArticleLike.user_id != user_id
            ).all()
            
            for user in users_who_liked:
                similar_users[user[0]] += 1
        
        # 通过评论行为查找相似用户
        for article_id in user_articles:
            users_who_commented = db.session.query(ContentArticleComment.user_id).filter(
                ContentArticleComment.article_id == article_id, 
                ContentArticleComment.user_id != user_id
            ).distinct().all()
            
            for user in users_who_commented:
                similar_users[user[0]] += 1
        
        # 计算相似度并排序
        user_similarities = []
        for user, common_count in similar_users.items():
            # 计算Jaccard相似度
            user_articles_set = set(user_articles)
            other_user_articles = RecommendationService._get_user_article_ids(user)
            other_user_articles_set = set(other_user_articles)
            
            union_size = len(user_articles_set.union(other_user_articles_set))
            if union_size > 0:
                similarity = common_count / union_size
                user_similarities.append((user, similarity))
        
        # 按相似度排序并返回前N个
        user_similarities.sort(key=lambda x: x[1], reverse=True)
        return user_similarities[:top_n]
    
    @staticmethod
    def _find_similar_articles(article_id, top_n=10):
        """
        找到与目标文章相似的文章
        """
        # 获取喜欢目标文章的用户
        users_who_liked = db.session.query(ContentArticleLike.user_id).filter(
            ContentArticleLike.article_id == article_id
        ).all()
        user_ids = [user[0] for user in users_who_liked]
        
        if not user_ids:
            return []
        
        # 找到这些用户喜欢的其他文章
        similar_articles = defaultdict(int)
        
        other_articles = db.session.query(ContentArticleLike.article_id, db.func.count(ContentArticleLike.user_id)).filter(
            ContentArticleLike.user_id.in_(user_ids),
            ContentArticleLike.article_id != article_id
        ).group_by(ContentArticleLike.article_id).all()
        
        for article, count in other_articles:
            similar_articles[article] = count
        
        # 计算相似度并排序
        article_similarities = []
        for article, common_count in similar_articles.items():
            # 计算Jaccard相似度
            total_users = len(user_ids)
            similarity = common_count / total_users
            article_similarities.append((article, similarity))
        
        # 按相似度排序并返回前N个
        article_similarities.sort(key=lambda x: x[1], reverse=True)
        return article_similarities[:top_n]
    
    @staticmethod
    def _get_user_article_ids(user_id):
        """
        获取用户的所有文章ID
        """
        # 获取用户点赞的文章
        liked_articles = db.session.query(ContentArticleLike.article_id).filter(
            ContentArticleLike.user_id == user_id
        ).all()
        
        # 获取用户评论的文章
        commented_articles = db.session.query(ContentArticleComment.article_id).filter(
            ContentArticleComment.user_id == user_id
        ).distinct().all()
        
        # 合并去重
        article_ids = set()
        for article in liked_articles:
            article_ids.add(article[0])
        for article in commented_articles:
            article_ids.add(article[0])
        
        return list(article_ids)
    
    @staticmethod
    def _get_articles_by_ids(article_ids):
        """
        根据文章ID列表获取文章详情
        """
        if not article_ids:
            return []
        
        articles = db.session.query(ContentArticle).filter(
            ContentArticle.id.in_(article_ids),
            ContentArticle.status == 1  # 只返回已发布的文章
        ).all()
        
        # 转换为字典列表
        article_list = []
        for article in articles:
            article_list.append({
                'id': article.id,
                'title': article.title,
                'sub_title': article.sub_title,
                'cover_image': article.cover_image,
                'author_name': article.author_name,
                'view_count': article.view_count,
                'like_count': article.like_count,
                'comment_count': article.comment_count,
                'publish_time': article.publish_time.strftime('%Y-%m-%d %H:%M:%S') if article.publish_time else None
            })
        
        return article_list
    
    @staticmethod
    def _get_hot_articles(limit):
        """
        获取热门文章
        """
        articles = db.session.query(ContentArticle).filter(
            ContentArticle.status == 1
        ).order_by(
            ContentArticle.view_count.desc(),
            ContentArticle.like_count.desc()
        ).limit(limit).all()
        
        # 转换为字典列表
        article_list = []
        for article in articles:
            article_list.append({
                'id': article.id,
                'title': article.title,
                'sub_title': article.sub_title,
                'cover_image': article.cover_image,
                'author_name': article.author_name,
                'view_count': article.view_count,
                'like_count': article.like_count,
                'comment_count': article.comment_count,
                'publish_time': article.publish_time.strftime('%Y-%m-%d %H:%M:%S') if article.publish_time else None
            })
        
        return article_list
    
    @staticmethod
    def _combine_recommendations(list1, list2, limit):
        """
        结合两种推荐结果
        """
        # 使用字典去重，保留先出现的文章
        combined = {}
        
        # 先添加list1的文章
        for article in list1:
            combined[article['id']] = article
        
        # 再添加list2的文章，填补空缺
        for article in list2:
            if article['id'] not in combined:
                combined[article['id']] = article
        
        # 转换为列表并返回前limit个
        result = list(combined.values())
        return result[:limit]
