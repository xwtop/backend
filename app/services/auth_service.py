from app.extensions import db
from app.models import SysUser
from app.common.utils.jwt_utils import generate_token
from app.common.utils.password_utils import hash_password, verify_password


class AuthService:
    @staticmethod
    def login(username, password):
        # 用户登录：验证用户名密码并生成JWT令牌
        user = db.session.query(SysUser).filter_by(username=username, deleted=0).first()

        if not user:
            return None, '用户不存在'

        if user.status == 0:
            return None, '用户已被禁用'

        if not verify_password(password, user.password):
            return None, '密码错误'

        roles = user.roles.all()

        token = generate_token(user.id, user.real_name, roles)

        return {
            'accessToken': token,
            'userId': user.id,
            'realName': user.real_name,
            'role': [role.code for role in roles]
        }, None

    @staticmethod
    def register(username, password, real_name, email, email_code):
        # 用户注册：创建新用户并分配默认角色
        existing_user = db.session.query(SysUser).filter_by(username=username, deleted=0).first()
        if existing_user:
            return False, '学号已存在'

        existing_email = db.session.query(SysUser).filter_by(email=email, deleted=0).first()
        if existing_email:
            return False, '邮箱已被注册'

        hashed_password = hash_password(password)

        user = SysUser(
            username=username,
            password=hashed_password,
            real_name=real_name,
            email=email,
            status=1
        )
        db.session.add(user)
        db.session.commit()
        return True, None

    @staticmethod
    def logout(token):
        # 用户登出：处理登出逻辑

        # TODO: 在实际部署中，可能需要实现token黑名单功能

        return True, None
