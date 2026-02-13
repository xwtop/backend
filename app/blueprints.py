from app.api import *


# 注册蓝图
def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(user_bp, url_prefix='/api/v1/sysUser')
    app.register_blueprint(role_bp, url_prefix='/api/v1/sysRole')
    app.register_blueprint(permission_bp, url_prefix='/api/v1/sysPermission')
    app.register_blueprint(category_bp, url_prefix='/api/v1/category')
    app.register_blueprint(article_bp, url_prefix='/api/v1/article')
    app.register_blueprint(article_like_bp, url_prefix='/api/v1/articleLike')
    app.register_blueprint(article_comment_bp, url_prefix='/api/v1/articleComment')
    app.register_blueprint(upload_bp, url_prefix='/api/v1/upload')
    app.register_blueprint(subscription_bp, url_prefix='/api/v1/subscription')
    app.register_blueprint(notification_bp, url_prefix='/api/v1/notification')
    app.register_blueprint(notification_reminder_bp, url_prefix='/api/v1/notificationReminder')
    app.register_blueprint(recommendation_bp, url_prefix='/api/v1/recommendation')
    app.register_blueprint(dashboard_bp, url_prefix='/api/v1/dashboard')
