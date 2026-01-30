from app.models import ContentArticleComment, ContentArticle
from app.extensions import db


class ArticleCommentService:
    @staticmethod
    def save_comment(form_data):
        article_id = form_data.get('article_id')

        article = db.session.query(ContentArticle).filter_by(id=article_id, deleted=0).first()
        if not article:
            return None, '文章不存在'

        comment = ContentArticleComment(
            article_id=article_id,
            parent_id=form_data.get('parent_id'),
            user_id=form_data.get('user_id'),
            user_name=form_data.get('user_name'),
            user_avatar=form_data.get('user_avatar'),
            content=form_data.get('content')
        )

        db.session.add(comment)
        article.comment_count += 1
        db.session.commit()

        return comment.id, None

    @staticmethod
    def delete_comment(comment_id):
        comment = db.session.query(ContentArticleComment).filter_by(id=comment_id, deleted=0).first()
        if not comment:
            return False, '评论不存在'

        article = db.session.query(ContentArticle).filter_by(id=comment.article_id, deleted=0).first()
        if article:
            article.comment_count = max(0, article.comment_count - 1)

        comment.deleted = 1
        db.session.commit()

        return True, None

    @staticmethod
    def get_comment_vo(comment_id):
        comment = db.session.query(ContentArticleComment).filter_by(id=comment_id, deleted=0).first()
        if not comment:
            return None, '评论不存在'

        return {
            'id': comment.id,
            'articleId': comment.article_id,
            'parentId': comment.parent_id,
            'userId': comment.user_id,
            'userName': comment.user_name,
            'userAvatar': comment.user_avatar,
            'content': comment.content,
            'createTime': comment.create_time.isoformat() if comment.create_time else None
        }, None

    @staticmethod
    def get_comment_tree(article_id):
        all_comments = db.session.query(ContentArticleComment).filter_by(
            article_id=article_id, deleted=0
        ).order_by(ContentArticleComment.create_time.asc()).all()

        comment_dict = {}
        for comment in all_comments:
            comment_dict[comment.id] = {
                'id': comment.id,
                'articleId': comment.article_id,
                'parentId': comment.parent_id,
                'userId': comment.user_id,
                'userName': comment.user_name,
                'userAvatar': comment.user_avatar,
                'content': comment.content,
                'createTime': comment.create_time.isoformat() if comment.create_time else None,
                'children': []
            }

        tree = []
        for comment_id, comment_data in comment_dict.items():
            parent_id = comment_data['parentId']
            if parent_id and parent_id in comment_dict:
                comment_dict[parent_id]['children'].append(comment_data)
            else:
                tree.append(comment_data)

        return tree, None

    @staticmethod
    def page_comment(query_params):
        page = query_params.get('page', 1)
        page_size = query_params.get('page_size', 10)
        article_id = query_params.get('article_id')

        query = db.session.query(ContentArticleComment).filter_by(
            article_id=article_id, deleted=0
        ).order_by(ContentArticleComment.create_time.desc())

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        items = []
        for comment in pagination.items:
            items.append({
                'id': comment.id,
                'articleId': comment.article_id,
                'parentId': comment.parent_id,
                'userId': comment.user_id,
                'userName': comment.user_name,
                'userAvatar': comment.user_avatar,
                'content': comment.content,
                'createTime': comment.create_time.isoformat() if comment.create_time else None
            })

        return {
            'total': pagination.total,
            'items': items,
            'page': page,
            'page_size': page_size
        }, None

    @staticmethod
    def get_user_comments(user_id, page=1, page_size=10):
        query = db.session.query(ContentArticleComment).filter_by(
            user_id=user_id, deleted=0
        ).order_by(ContentArticleComment.create_time.desc())

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        items = []
        for comment in pagination.items:
            items.append({
                'id': comment.id,
                'articleId': comment.article_id,
                'parentId': comment.parent_id,
                'userId': comment.user_id,
                'userName': comment.user_name,
                'userAvatar': comment.user_avatar,
                'content': comment.content,
                'createTime': comment.create_time.isoformat() if comment.create_time else None
            })

        return {
            'total': pagination.total,
            'items': items,
            'page': page,
            'page_size': page_size
        }, None
