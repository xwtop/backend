import bcrypt


def hash_password(password):
    # 密码加密：使用bcrypt算法对密码进行哈希处理
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, hashed_password):
    # 密码验证：验证明文密码与哈希值是否匹配
    # 确保hashed_password是字节串
    if isinstance(hashed_password, str):
        hashed_bytes = hashed_password.encode('utf-8')
    else:
        hashed_bytes = hashed_password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_bytes)
