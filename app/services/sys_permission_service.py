from app.extensions import db
from app.models import SysPermission


class SysPermissionService:
    @staticmethod
    def get_permission_tree():
        permissions = db.session.query(SysPermission).filter_by(deleted=0).all()
        
        # 由于已移除parent_id字段，暂时返回扁平化的权限列表
        # 如果需要树形结构，需要重新设计数据库表结构来支持层级关系
        result = []
        for perm in permissions:
            node = {
                'id': perm.id,
                'name': perm.name,
                'code': perm.code,
                'type': perm.type,
                'status': perm.status,
                'resource': perm.resource,
                'action': perm.action,
                'remark': perm.remark
            }
            result.append(node)
        
        return result, None

    @staticmethod
    def save_sys_permission(form_data):
        # 添加权限：创建新的权限记录

        existing_permission = db.session.query(SysPermission).filter_by(code=form_data['code'], deleted=0).first()
        if existing_permission:
            return None, '权限编码已存在'

        permission = SysPermission(
            code=form_data['code'],
            name=form_data['name'],
            resource=form_data.get('resource'),
            action=form_data.get('action'),
            type=form_data['type'],
            remark=form_data.get('remark'),
            status=form_data.get('status', 1)
        )

        db.session.add(permission)
        db.session.commit()

        return permission.id, None

    @staticmethod
    def update_sys_permission(permission_id, form_data):
        # 更新权限：修改权限信息

        permission = db.session.query(SysPermission).filter_by(id=permission_id, deleted=0).first()
        if not permission:
            return False, '权限不存在'

        if form_data.get('code') and form_data['code'] != permission.code:
            existing_permission = db.session.query(SysPermission).filter(
                SysPermission.code == form_data['code'],
                SysPermission.id != permission_id,
                SysPermission.deleted == 0
            ).first()
            if existing_permission:
                return False, '权限编码已存在'
            permission.code = form_data['code']

        if 'name' in form_data:
            permission.name = form_data['name']
        if 'resource' in form_data:
            permission.resource = form_data['resource']
        if 'action' in form_data:
            permission.action = form_data['action']
        if 'type' in form_data:
            permission.type = form_data['type']
        if 'remark' in form_data:
            permission.remark = form_data['remark']
        if 'status' in form_data:
            permission.status = form_data['status']

        db.session.commit()

        return True, None

    @staticmethod
    def delete_sys_permission(ids_str):
        # 删除权限：逻辑删除权限记录

        ids = [int(id_str) for id_str in ids_str.split(',') if id_str.strip()]

        db.session.query(SysPermission).filter(SysPermission.id.in_(ids)).update({
            'deleted': 1
        }, synchronize_session=False)

        db.session.commit()

        return True, None

    @staticmethod
    def get_sys_permission_vo(permission_id):
        # 获取权限详情：根据ID获取权限详细信息

        permission = db.session.query(SysPermission).filter_by(id=permission_id, deleted=0).first()
        if not permission:
            return None, '权限不存在'

        return {
            'id': permission.id,
            'code': permission.code,
            'name': permission.name,
            'resource': permission.resource,
            'action': permission.action,
            'type': permission.type,
            'remark': permission.remark,
            'status': permission.status
        }, None

    @staticmethod
    def page_sys_permission(query_params):
        # 分页查询权限：根据条件分页获取权限列表

        page = query_params.get('page', 1)
        page_size = query_params.get('page_size', 10)
        code = query_params.get('code')
        name = query_params.get('name')
        type_ = query_params.get('type')
        status = query_params.get('status')

        query = db.session.query(SysPermission).filter_by(deleted=0)

        if code:
            query = query.filter(SysPermission.code.like(f'%{code}%'))
        if name:
            query = query.filter(SysPermission.name.like(f'%{name}%'))
        if type_:
            query = query.filter(SysPermission.type == type_)
        if status is not None:
            query = query.filter(SysPermission.status == status)

        query = query.order_by(SysPermission.create_time.desc())

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        items = []
        for permission in pagination.items:
            items.append({
                'id': permission.id,
                'code': permission.code,
                'name': permission.name,
                'resource': permission.resource,
                'action': permission.action,
                'type': permission.type,
                'remark': permission.remark,
                'status': permission.status
            })

        return {
            'total': pagination.total,
            'items': items,
            'page': page,
            'page_size': page_size
        }, None

    @staticmethod
    def list_all_permissions():
        # 获取所有未删除的权限列表
        permissions = db.session.query(SysPermission).filter_by(deleted=0).order_by(SysPermission.create_time.desc()).all()

        items = []
        for permission in permissions:
            items.append({
                'id': permission.id,
                'code': permission.code,
                'name': permission.name,
                'resource': permission.resource,
                'action': permission.action,
                'type': permission.type,
                'remark': permission.remark,
                'status': permission.status
            })

        return items, None
