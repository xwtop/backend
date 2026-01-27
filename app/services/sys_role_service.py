from app.models import SysRole, SysPermission, SysRolePermission
from app.extensions import db
from sqlalchemy import or_
from flask import current_app


class SysRoleService:
    @staticmethod
    def save_sys_role(form_data):
        # 添加角色：创建新角色并分配权限

        
        existing_role = db.session.query(SysRole).filter_by(code=form_data['code'], deleted=0).first()
        if existing_role:
    
            return None, '角色编码已存在'
        
        role = SysRole(
            code=form_data['code'],
            name=form_data['name'],
            sort=form_data.get('sort', 0),
            remark=form_data.get('remark'),
            status=form_data.get('status', 1)
        )
        
        db.session.add(role)
        db.session.commit()
        
        permission_ids = form_data.get('permission_ids', [])
        for permission_id in permission_ids:
            role_permission = SysRolePermission(role_id=role.id, permission_id=permission_id)
            db.session.add(role_permission)
        
        db.session.commit()

        return role.id, None
    
    @staticmethod
    def update_sys_role(role_id, form_data):
        # 更新角色：修改角色信息及权限分配

        
        role = db.session.query(SysRole).filter_by(id=role_id, deleted=0).first()
        if not role:
    
            return False, '角色不存在'
        
        if form_data.get('code') and form_data['code'] != role.code:
            existing_role = db.session.query(SysRole).filter(
                SysRole.code == form_data['code'],
                SysRole.id != role_id,
                SysRole.deleted == 0
            ).first()
            if existing_role:
        
                return False, '角色编码已存在'
            role.code = form_data['code']
        
        if 'name' in form_data:
            role.name = form_data['name']
        if 'sort' in form_data:
            role.sort = form_data['sort']
        if 'remark' in form_data:
            role.remark = form_data['remark']
        if 'status' in form_data:
            role.status = form_data['status']
        
        db.session.query(SysRolePermission).filter_by(role_id=role_id).delete()
        
        permission_ids = form_data.get('permission_ids', [])
        for permission_id in permission_ids:
            role_permission = SysRolePermission(role_id=role_id, permission_id=permission_id)
            db.session.add(role_permission)
        
        db.session.commit()

        return True, None
    
    @staticmethod
    def delete_sys_role(ids_str):
        # 删除角色：逻辑删除角色记录

        
        ids = [int(id_str) for id_str in ids_str.split(',') if id_str.strip()]
        
        db.session.query(SysRolePermission).filter(SysRolePermission.role_id.in_(ids)).delete(synchronize_session=False)
        
        db.session.query(SysRole).filter(SysRole.id.in_(ids)).update({
            'deleted': 1
        }, synchronize_session=False)
        
        db.session.commit()

        return True, None
    
    @staticmethod
    def get_sys_role_vo(role_id):
        # 获取角色详情：根据ID获取角色详细信息

        
        role = db.session.query(SysRole).filter_by(id=role_id, deleted=0).first()
        if not role:
    
            return None, '角色不存在'
        

        return {
            'id': role.id,
            'code': role.code,
            'name': role.name,
            'sort': role.sort,
            'remark': role.remark,
            'status': role.status,
            'permissions': [{'id': p.id, 'code': p.code, 'name': p.name, 'resource': p.resource, 'action': p.action, 'type': p.type, 'remark': p.remark, 'status': p.status} for p in role.permissions.all()]
        }, None
    
    @staticmethod
    def page_sys_role(query_params):
        # 分页查询角色：根据条件分页获取角色列表

        
        page = query_params.get('page', 1)
        page_size = query_params.get('page_size', 10)
        code = query_params.get('code')
        name = query_params.get('name')
        status = query_params.get('status')
        
        query = db.session.query(SysRole).filter_by(deleted=0)
        
        if code:
            query = query.filter(SysRole.code.like(f'%{code}%'))
        if name:
            query = query.filter(SysRole.name.like(f'%{name}%'))
        if status is not None:
            query = query.filter(SysRole.status == status)
        
        query = query.order_by(SysRole.sort.asc(), SysRole.create_time.desc())
        
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        
        items = []
        for role in pagination.items:
            items.append({
                'id': role.id,
                'code': role.code,
                'name': role.name,
                'sort': role.sort,
                'remark': role.remark,
                'status': role.status,
                'permissions': [{'id': p.id, 'code': p.code, 'name': p.name, 'resource': p.resource, 'action': p.action, 'type': p.type, 'remark': p.remark, 'status': p.status} for p in role.permissions.all()]
            })
        

        return {
            'total': pagination.total,
            'items': items,
            'page': page,
            'page_size': page_size
        }, None

    @staticmethod
    def assign_role_permission(role_id, permission_ids):
        role = db.session.query(SysRole).filter_by(id=role_id, deleted=0).first()
        if not role:
            return None, '角色不存在'
        
        db.session.query(SysRolePermission).filter_by(role_id=role_id).delete()
        
        for permission_id in permission_ids:
            role_permission = SysRolePermission(role_id=role_id, permission_id=permission_id)
            db.session.add(role_permission)
        
        db.session.commit()
        
        return True, None

    @staticmethod
    def get_role_permissions(role_id):
        role = db.session.query(SysRole).filter_by(id=role_id, deleted=0).first()
        if not role:
            return None, '角色不存在'
        
        permissions = role.permissions.all()
        
        return [
            {
                'id': p.id,
                'code': p.code,
                'name': p.name,
                'type': p.type
            }
            for p in permissions
        ], None

    @staticmethod
    def list_all_roles():
        roles = db.session.query(SysRole).filter_by(deleted=0, status=1).order_by(SysRole.sort.asc()).all()
        
        return [
            {
                'id': role.id,
                'code': role.code,
                'name': role.name,
                'sort': role.sort,
                'remark': role.remark,
                'status': role.status
            }
            for role in roles
        ], None