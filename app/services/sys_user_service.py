from app.models import SysUser, SysUserRole
from app.extensions import db


class SysUserService:
    @staticmethod
    def save_sys_user(form_data):
        # 添加用户：创建新用户并分配角色

        
        existing_user = db.session.query(SysUser).filter_by(username=form_data['username'], deleted=0).first()
        if existing_user:
    
            return None, '学号已存在'
        
        if form_data.get('email'):
            existing_email = db.session.query(SysUser).filter_by(email=form_data['email'], deleted=0).first()
            if existing_email:
        
                return None, '邮箱已被注册'
        
        # 密码是必需的，如果未提供则返回错误
        password = form_data.get('password')
        if not password:
    
            return None, '密码不能为空'
        
        from app.common.utils.password_utils import hash_password
        hashed_password = hash_password(password)
        
        user = SysUser(
            username=form_data['username'],
            password=hashed_password,
            real_name=form_data.get('real_name'),
            email=form_data.get('email'),
            phone=form_data.get('phone'),
            avatar=form_data.get('avatar'),
            gender=form_data.get('gender', 0),
            birthday=form_data.get('birthday'),
            introduction=form_data.get('introduction'),
            status=form_data.get('status', 1)
        )
        
        db.session.add(user)
        db.session.commit()
        
        role_ids = form_data.get('role_ids', [])
        for role_id in role_ids:
            user_role = SysUserRole(user_id=user.id, role_id=role_id)
            db.session.add(user_role)
        
        db.session.commit()

        return user.id, None
    
    @staticmethod
    def update_sys_user(user_id, form_data):
        # 更新用户：修改用户信息及角色分配

        
        user = db.session.query(SysUser).filter_by(id=user_id, deleted=0).first()
        if not user:
    
            return False, '用户不存在'
        
        if form_data.get('username') and form_data['username'] != user.username:
            existing_user = db.session.query(SysUser).filter(
                SysUser.username == form_data['username'],
                SysUser.id != user_id,
                SysUser.deleted == 0
            ).first()
            if existing_user:
        
                return False, '学号已存在'
            user.username = form_data['username']
        
        if form_data.get('email') and form_data['email'] != user.email:
            existing_email = db.session.query(SysUser).filter(
                SysUser.email == form_data['email'],
                SysUser.id != user_id,
                SysUser.deleted == 0
            ).first()
            if existing_email:
        
                return False, '邮箱已被注册'
            user.email = form_data['email']
        
        if form_data.get('password'):
            from app.common.utils.password_utils import hash_password
            user.password = hash_password(form_data['password'])
        
        if 'real_name' in form_data:
            user.real_name = form_data['real_name']
        if 'phone' in form_data:
            user.phone = form_data['phone']
        if 'avatar' in form_data:
            user.avatar = form_data['avatar']
        if 'gender' in form_data:
            user.gender = form_data['gender']
        if 'birthday' in form_data:
            user.birthday = form_data['birthday']
        if 'introduction' in form_data:
            user.introduction = form_data['introduction']
        if 'status' in form_data:
            user.status = form_data['status']
        
        db.session.query(SysUserRole).filter_by(user_id=user_id).delete()
        
        role_ids = form_data.get('role_ids', [])
        for role_id in role_ids:
            user_role = SysUserRole(user_id=user_id, role_id=role_id)
            db.session.add(user_role)
        
        db.session.commit()

        return True, None
    
    @staticmethod
    def delete_sys_user(ids_str):
        # 删除用户：逻辑删除用户记录

        
        ids = [int(id_str) for id_str in ids_str.split(',') if id_str.strip()]
        
        db.session.query(SysUserRole).filter(SysUserRole.user_id.in_(ids)).delete(synchronize_session=False)
        
        db.session.query(SysUser).filter(SysUser.id.in_(ids)).update({
            'deleted': 1
        }, synchronize_session=False)
        
        db.session.commit()

        return True, None
    
    @staticmethod
    def get_sys_user_vo(user_id):
        # 获取用户详情：根据ID获取用户详细信息

        
        user = db.session.query(SysUser).filter_by(id=user_id, deleted=0).first()
        if not user:
    
            return None, '用户不存在'
        

        return {
            'id': user.id,
            'username': user.username,
            'realName': user.real_name,
            'email': user.email,
            'phone': user.phone,
            'avatar': user.avatar,
            'gender': user.gender,
            'birthday': user.birthday,
            'introduction': user.introduction,
            'status': user.status,
            'roles': [{'id': r.id, 'code': r.code, 'name': r.name, 'sort': r.sort, 'remark': r.remark, 'status': r.status} for r in user.roles.all()]
        }, None
    
    @staticmethod
    def page_sys_user(query_params):
        # 分页查询用户：根据条件分页获取用户列表

        
        page = query_params.get('page', 1)
        page_size = query_params.get('page_size', 10)
        username = query_params.get('username')
        real_name = query_params.get('real_name')
        email = query_params.get('email')
        status = query_params.get('status')
        
        query = db.session.query(SysUser).filter_by(deleted=0)
        
        if username:
            query = query.filter(SysUser.username.like(f'%{username}%'))
        if real_name:
            query = query.filter(SysUser.real_name.like(f'%{real_name}%'))
        if email:
            query = query.filter(SysUser.email.like(f'%{email}%'))
        if status is not None:
            query = query.filter(SysUser.status == status)
        
        query = query.order_by(SysUser.create_time.desc())
        
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        
        items = []
        for user in pagination.items:
            items.append({
                'id': user.id,
                'username': user.username,
                'realName': user.real_name,
                'email': user.email,
                'phone': user.phone,
                'avatar': user.avatar,
                'gender': user.gender,
                'birthday': user.birthday,
                'introduction': user.introduction,
                'status': user.status,
                'roles': [{'id': r.id, 'code': r.code, 'name': r.name, 'sort': r.sort, 'remark': r.remark, 'status': r.status} for r in user.roles.all()]
            })
        

        return {
            'total': pagination.total,
            'items': items,
            'page': page,
            'page_size': page_size
        }, None

    @staticmethod
    def assign_user_role(user_id, role_ids):
        user = db.session.query(SysUser).filter_by(id=user_id, deleted=0).first()
        if not user:
            return None, '用户不存在'
        
        db.session.query(SysUserRole).filter_by(user_id=user_id).delete()
        
        for role_id in role_ids:
            user_role = SysUserRole(user_id=user_id, role_id=role_id)
            db.session.add(user_role)
        
        db.session.commit()
        
        return True, None

    @staticmethod
    def reset_password(user_id, new_password):
        user = db.session.query(SysUser).filter_by(id=user_id, deleted=0).first()
        if not user:
            return False, '用户不存在'
        
        if not new_password:
            return False, '密码不能为空'
        
        from app.common.utils.password_utils import hash_password
        user.password = hash_password(new_password)
        db.session.commit()
        
        return True, None