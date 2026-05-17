from app.extensions import db
from app.models import SysUser, SysRole, SysUserRole
from app.common.utils.jwt_utils import generate_token
from app.common.utils.password_utils import hash_password, verify_password


class AuthService:
    @staticmethod
    def login(username, password):
        # 用户登录：验证用户名密码并生成JWT令牌
        user = db.session.query(SysUser).filter_by(username=username, deleted=0).first()

        if not user:
            return None, '账号或密码错误'

        if user.status == 0:
            return None, '账号已被禁用'

        if not verify_password(password, user.password):
            return None, '账号或密码错误'

        roles = user.roles.all()

        token = generate_token(user.id, user.real_name, roles)

        return {
            'accessToken': token,
            'userId': user.id,
            'realName': user.real_name,
            'role': [role.code for role in roles],
            'roleName': [role.name for role in roles]
        }, None

    @staticmethod
    def register(username, password, real_name):
        existing_user = db.session.query(SysUser).filter_by(username=username, deleted=0).first()
        if existing_user:
            return False, '学号已存在'

        hashed_password = hash_password(password)

        user = SysUser(
            username=username,
            password=hashed_password,
            real_name=real_name,
            status=1
        )
        db.session.add(user)
        db.session.flush()

        student_role = db.session.query(SysRole).filter_by(code='STUDENT', deleted=0).first()
        if student_role:
            user_role = SysUserRole(
                user_id=user.id,
                role_id=student_role.id
            )
            db.session.add(user_role)

        db.session.commit()
        return True, None

    @staticmethod
    def logout(token):
        # 用户登出：处理登出逻辑

        # TODO: 在实际部署中，可能需要实现token黑名单功能

        return True, None

    @staticmethod
    def change_password(user_id, old_password, new_password):
        # 修改密码：验证原密码并更新为新密码
        user = db.session.query(SysUser).filter_by(id=user_id, deleted=0).first()
        
        if not user:
            return False, '用户不存在'
        
        if not verify_password(old_password, user.password):
            return False, '原密码错误'
        
        hashed_password = hash_password(new_password)
        user.password = hashed_password
        db.session.commit()
        
        return True, None
