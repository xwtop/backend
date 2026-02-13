from flask import Blueprint, request
from marshmallow import ValidationError
from datetime import datetime, timezone

from app.common.Results import Result, PageResult
from app.middleware.auth import token_required
from app.models import NotificationReminder
from app.extensions import db

notification_reminder_bp = Blueprint('notification_reminder', __name__)

@notification_reminder_bp.route('/add', methods=['POST'])
@token_required
def add_reminder():
    """添加定时提醒"""
    data = request.json
    try:
        # 转换时间格式
        remind_time_str = data['remindTime']
        # 解析本地时间
        remind_time = datetime.strptime(remind_time_str, '%Y-%m-%d %H:%M:%S')
        
        reminder = NotificationReminder(
            title=data['title'],
            content=data['content'],
            remind_time=remind_time,
            repeat=data.get('repeat', 0),
            status=data.get('status', 1),
            target_type=data.get('targetType', 0),
            target_role=data.get('targetRole'),
            create_by=request.headers.get('User-Id') or 'system',
            create_time=db.func.current_timestamp(),
            update_by=request.headers.get('User-Id') or 'system',
            update_time=db.func.current_timestamp()
        )
        db.session.add(reminder)
        db.session.commit()
        return Result.success(reminder.id)
    except Exception as e:
        db.session.rollback()
        return Result.server_error(str(e))


@notification_reminder_bp.route('/list', methods=['GET'])
@token_required
def list_reminders():
    """获取定时提醒列表"""
    try:
        reminders = db.session.query(NotificationReminder).filter_by(
            deleted=0
        ).order_by(
            NotificationReminder.create_time.desc()
        ).all()
        
        result = []
        for reminder in reminders:
            result.append({
                'id': reminder.id,
                'title': reminder.title,
                'content': reminder.content,
                'remindTime': reminder.remind_time.strftime('%Y-%m-%d %H:%M:%S') if reminder.remind_time else None,
                'repeat': reminder.repeat,
                'status': reminder.status,
                'targetType': reminder.target_type,
                'targetRole': reminder.target_role,
                'createBy': reminder.create_by,
                'createTime': reminder.create_time.strftime('%Y-%m-%d %H:%M:%S') if reminder.create_time else None,
                'updateBy': reminder.update_by,
                'updateTime': reminder.update_time.strftime('%Y-%m-%d %H:%M:%S') if reminder.update_time else None
            })
        
        return Result.success(result)
    except Exception as e:
        return Result.server_error(str(e))


@notification_reminder_bp.route('/<int:reminder_id>', methods=['GET'])
@token_required
def get_reminder(reminder_id):
    """获取定时提醒详情"""
    try:
        reminder = db.session.query(NotificationReminder).filter_by(
            id=reminder_id,
            deleted=0
        ).first()
        
        if not reminder:
            return Result.not_found('提醒不存在')
        
        result = {
            'id': reminder.id,
            'title': reminder.title,
            'content': reminder.content,
            'remindTime': reminder.remind_time.strftime('%Y-%m-%d %H:%M:%S') if reminder.remind_time else None,
            'repeat': reminder.repeat,
            'status': reminder.status,
            'targetType': reminder.target_type,
            'targetRole': reminder.target_role,
            'createBy': reminder.create_by,
            'createTime': reminder.create_time.strftime('%Y-%m-%d %H:%M:%S') if reminder.create_time else None,
            'updateBy': reminder.update_by,
            'updateTime': reminder.update_time.strftime('%Y-%m-%d %H:%M:%S') if reminder.update_time else None
        }
        
        return Result.success(result)
    except Exception as e:
        return Result.server_error(str(e))


@notification_reminder_bp.route('/<int:reminder_id>', methods=['PUT'])
@token_required
def update_reminder(reminder_id):
    """更新定时提醒"""
    data = request.json
    try:
        reminder = db.session.query(NotificationReminder).filter_by(
            id=reminder_id,
            deleted=0
        ).first()
        
        if not reminder:
            return Result.not_found('提醒不存在')
        
        reminder.title = data.get('title', reminder.title)
        reminder.content = data.get('content', reminder.content)
        
        # 转换时间格式
        remind_time_str = data.get('remindTime')
        if remind_time_str:
            # 解析本地时间
            remind_time = datetime.strptime(remind_time_str, '%Y-%m-%d %H:%M:%S')
            reminder.remind_time = remind_time
        
        reminder.repeat = data.get('repeat', reminder.repeat)
        reminder.status = data.get('status', reminder.status)
        reminder.target_type = data.get('targetType', reminder.target_type)
        reminder.target_role = data.get('targetRole', reminder.target_role)
        reminder.update_by = request.headers.get('User-Id') or 'system'
        reminder.update_time = db.func.current_timestamp()
        
        db.session.commit()
        return Result.success(True)
    except Exception as e:
        db.session.rollback()
        return Result.server_error(str(e))


@notification_reminder_bp.route('/<int:reminder_id>', methods=['DELETE'])
@token_required
def delete_reminder(reminder_id):
    """删除定时提醒（逻辑删除）"""
    try:
        reminder = db.session.query(NotificationReminder).filter_by(
            id=reminder_id,
            deleted=0
        ).first()
        
        if not reminder:
            return Result.not_found('提醒不存在')
        
        reminder.deleted = 1
        reminder.update_by = request.headers.get('User-Id') or 'system'
        reminder.update_time = db.func.current_timestamp()
        
        db.session.commit()
        return Result.success(True)
    except Exception as e:
        db.session.rollback()
        return Result.server_error(str(e))


@notification_reminder_bp.route('/toggle-status/<int:reminder_id>', methods=['PUT'])
@token_required
def toggle_reminder_status(reminder_id):
    """切换定时提醒状态"""
    try:
        reminder = db.session.query(NotificationReminder).filter_by(
            id=reminder_id,
            deleted=0
        ).first()
        
        if not reminder:
            return Result.not_found('提醒不存在')
        
        reminder.status = 1 if reminder.status == 0 else 0
        reminder.update_by = request.headers.get('User-Id') or 'system'
        reminder.update_time = db.func.current_timestamp()
        
        db.session.commit()
        return Result.success({'status': reminder.status})
    except Exception as e:
        db.session.rollback()
        return Result.server_error(str(e))
