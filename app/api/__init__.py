from flask import Blueprint, request, jsonify, g
from app.schemas import LoginSchema, RegisterSchema, TokenVOSchema, SysUserFormSchema, SysUserPageQuerySchema, SysRoleFormSchema, SysRolePageQuerySchema, SysPermissionFormSchema, SysPermissionPageQuerySchema, CategoryFormSchema, CategoryPageQuerySchema, ArticleFormSchema, ArticlePageQuerySchema, ArticlePublishSchema, ArticleLikeFormSchema, ArticleCommentFormSchema, ArticleCommentPageQuerySchema, SubscriptionSchema, NotificationQuerySchema
from app.middleware.auth import token_required


# 从子模块导入蓝图
from .auth_api import auth_bp
from .user_api import user_bp
from .role_api import role_bp
from .permission_api import permission_bp
from .category_api import category_bp
from .article_api import article_bp
from .article_like_api import article_like_bp
from .article_comment_api import article_comment_bp
from .upload_api import upload_bp
from .subscription_api import subscription_bp
from .notification_api import notification_bp
from .notification_reminder_api import notification_reminder_bp
from .recommendation_api import recommendation_bp
from .dashboard_api import dashboard_bp

__all__ = ['auth_bp', 'user_bp', 'role_bp', 'permission_bp', 'category_bp', 'article_bp', 'article_like_bp', 'article_comment_bp', 'upload_bp', 'subscription_bp', 'notification_bp', 'notification_reminder_bp', 'recommendation_bp', 'dashboard_bp']
