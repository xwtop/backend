from app.api import auth_bp, user_bp, role_bp, permission_bp


# 注册蓝图
def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(user_bp, url_prefix='/api/v1/sysUser')
    app.register_blueprint(role_bp, url_prefix='/api/v1/sysRole')
    app.register_blueprint(permission_bp, url_prefix='/api/v1/sysPermission')
