from flask_socketio import emit, join_room, leave_room, disconnect
from flask import request
from app.extensions import socketio
from app.common.utils.jwt_utils import decode_token


@socketio.on('connect')
def handle_connect():
    token = request.args.get('token')
    if not token:
        print('[WebSocket] 连接失败：没有 token')
        disconnect()
        return
    
    try:
        decoded = decode_token(token)
        if not decoded:
            print('[WebSocket] 连接失败：token 无效')
            disconnect()
            return
        
        user_id = decoded.get('user_id')
        if not user_id:
            print('[WebSocket] 连接失败：token 中没有 user_id')
            disconnect()
            return
        
        request.user_id = user_id
        
        room = f'user_{user_id}'
        join_room(room)
        
        print(f'[WebSocket] 用户 {user_id} 连接成功，加入房间 {room}')
        emit('connected', {'userId': user_id, 'message': '连接成功'})
    except Exception as e:
        print(f'[WebSocket] 连接失败：{e}')
        disconnect()


@socketio.on('disconnect')
def handle_disconnect():
    user_id = getattr(request, 'user_id', None)
    if user_id:
        room = f'user_{user_id}'
        leave_room(room)


def send_notification_to_user(user_id, notification_data):
    room = f'user_{user_id}'
    print(f'[WebSocket] 发送通知给用户 {user_id}，房间 {room}，通知内容：{notification_data}')
    socketio.emit('new_notification', notification_data, room=room)
    print(f'[WebSocket] 通知已发送')
