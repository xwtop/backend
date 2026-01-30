from app.models import ContentCategory
from app.extensions import db


class CategoryService:
    @staticmethod
    def save_category(form_data):
        existing_category = db.session.query(ContentCategory).filter_by(
            code=form_data['code'], deleted=0
        ).first()
        if existing_category:
            return None, '分类编码已存在'

        category = ContentCategory(
            parent_id=form_data.get('parent_id'),
            name=form_data.get('name'),
            code=form_data.get('code'),
            sort=form_data.get('sort', 0),
            status=form_data.get('status', 1),
            remark=form_data.get('remark')
        )

        db.session.add(category)
        db.session.commit()

        return category.id, None

    @staticmethod
    def update_category(category_id, form_data):
        category = db.session.query(ContentCategory).filter_by(id=category_id, deleted=0).first()
        if not category:
            return False, '分类不存在'

        if form_data.get('code') and form_data['code'] != category.code:
            existing_category = db.session.query(ContentCategory).filter(
                ContentCategory.code == form_data['code'],
                ContentCategory.id != category_id,
                ContentCategory.deleted == 0
            ).first()
            if existing_category:
                return False, '分类编码已存在'
            category.code = form_data['code']

        if 'parent_id' in form_data:
            category.parent_id = form_data['parent_id']
        if 'name' in form_data:
            category.name = form_data['name']
        if 'sort' in form_data:
            category.sort = form_data['sort']
        if 'status' in form_data:
            category.status = form_data['status']
        if 'remark' in form_data:
            category.remark = form_data['remark']

        db.session.commit()

        return True, None

    @staticmethod
    def delete_category(ids_str):
        ids = [id_str.strip() for id_str in ids_str.split(',') if id_str.strip()]

        db.session.query(ContentCategory).filter(
            ContentCategory.id.in_(ids)
        ).update({
            'deleted': 1
        }, synchronize_session=False)

        db.session.commit()

        return True, None

    @staticmethod
    def get_category_vo(category_id):
        category = db.session.query(ContentCategory).filter_by(id=category_id, deleted=0).first()
        if not category:
            return None, '分类不存在'

        return {
            'id': category.id,
            'parentId': category.parent_id,
            'name': category.name,
            'code': category.code,
            'sort': category.sort,
            'status': category.status,
            'remark': category.remark
        }, None

    @staticmethod
    def get_category_tree():
        all_categories = db.session.query(ContentCategory).filter_by(deleted=0).order_by(
            ContentCategory.sort.asc()
        ).all()

        category_dict = {}
        for category in all_categories:
            category_dict[category.id] = {
                'id': category.id,
                'parentId': category.parent_id,
                'name': category.name,
                'code': category.code,
                'sort': category.sort,
                'status': category.status,
                'children': []
            }

        tree = []
        for category_id, category_data in category_dict.items():
            parent_id = category_data['parentId']
            if parent_id and parent_id in category_dict:
                category_dict[parent_id]['children'].append(category_data)
            else:
                tree.append(category_data)

        return tree, None

    @staticmethod
    def page_category(query_params):
        page = query_params.get('page', 1)
        page_size = query_params.get('page_size', 10)
        name = query_params.get('name')
        code = query_params.get('code')
        status = query_params.get('status')

        query = db.session.query(ContentCategory).filter_by(deleted=0)

        if name:
            query = query.filter(ContentCategory.name.like(f'%{name}%'))
        if code:
            query = query.filter(ContentCategory.code.like(f'%{code}%'))
        if status is not None:
            query = query.filter(ContentCategory.status == status)

        query = query.order_by(ContentCategory.sort.asc())

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        items = []
        for category in pagination.items:
            items.append({
                'id': category.id,
                'parentId': category.parent_id,
                'name': category.name,
                'code': category.code,
                'sort': category.sort,
                'status': category.status,
                'remark': category.remark
            })

        return {
            'total': pagination.total,
            'items': items,
            'page': page,
            'page_size': page_size
        }, None
