from datetime import datetime, timedelta
from app.models import NotificationReminder, SysUser, SysUserRole, SysRole
from app.extensions import db
from app.services.notification_service import NotificationService


def check_reminders(app):
    """检查并发送到期的定时提醒"""
    print(f"[{datetime.now()}] 开始检查定时提醒")
    
    with app.app_context():
        try:
            # 查找时间已到且状态为启用的提醒
            now = datetime.now()
            reminders = db.session.query(NotificationReminder).filter(
                NotificationReminder.remind_time <= now,
                NotificationReminder.status == 1,
                NotificationReminder.deleted == 0
            ).all()
            
            for reminder in reminders:
                try:
                    print(f"处理提醒: {reminder.title} (ID: {reminder.id})")
                    
                    # 确定目标用户
                    target_users = get_target_users(reminder.target_type, reminder.target_role)
                    
                    # 为每个目标用户创建通知
                    for user in target_users:
                        # 创建站内通知
                        NotificationService.create_notification(
                            user_id=user.id,
                            title=reminder.title,
                            content=reminder.content,
                            related_id=None,
                            notification_type='reminder'
                        )
                    
                    # 更新提醒状态或下次提醒时间
                    if reminder.repeat == 0:
                        # 一次性提醒，标记为已发送（禁用）
                        reminder.status = 0
                        print(f"一次性提醒已发送: {reminder.title}")
                    else:
                        # 重复提醒，计算下次提醒时间
                        reminder.remind_time = calculate_next_remind_time(reminder.remind_time, reminder.repeat)
                        print(f"重复提醒已发送，下次提醒时间: {reminder.remind_time}")
                    
                    db.session.commit()
                except Exception as e:
                    # 单个提醒处理失败，继续处理其他提醒
                    print(f"处理提醒 {reminder.id} 失败: {str(e)}")
                    db.session.rollback()
            
            print(f"[{datetime.now()}] 定时提醒检查完成，处理了 {len(reminders)} 个提醒")
        except Exception as e:
            print(f"检查定时提醒失败: {str(e)}")


def get_target_users(target_type, target_role):
    """根据目标类型获取目标用户"""
    if target_type == 0:
        # 全员
        return db.session.query(SysUser).filter_by(deleted=0).all()
    elif target_type == 1 and target_role:
        # 指定角色
        # 首先根据角色代码找到对应的角色
        role = db.session.query(SysRole).filter_by(code=target_role, deleted=0).first()
        if not role:
            return []
        # 然后根据角色ID找到对应的用户角色关联
        user_roles = db.session.query(SysUserRole).filter_by(
            role_id=role.id,
            deleted=0
        ).all()
        user_ids = [ur.user_id for ur in user_roles]
        return db.session.query(SysUser).filter(
            SysUser.id.in_(user_ids),
            SysUser.deleted == 0
        ).all()
    return []


def calculate_next_remind_time(current_time, repeat):
    """计算下次提醒时间"""
    if repeat == 1:
        # 每天
        return current_time + timedelta(days=1)
    elif repeat == 2:
        # 每周
        return current_time + timedelta(weeks=1)
    elif repeat == 3:
        # 每月（简化处理，按30天计算）
        return current_time + timedelta(days=30)
    return current_time
