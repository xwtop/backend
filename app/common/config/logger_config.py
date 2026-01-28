import logging
import os
from logging.handlers import RotatingFileHandler


def init_logging(app):
    """
    配置应用程序日志
    """
    # 如果处于调试或测试模式，则不添加文件处理器
    if app.debug or app.testing:
        return

    # 创建日志目录
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 设置日志级别
    app.logger.setLevel(logging.INFO)

    # 创建轮转日志处理器
    file_handler = RotatingFileHandler(
        'logs/campus_portal.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )

    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 添加处理器到应用日志器
    app.logger.addHandler(file_handler)


def get_logger(name):
    """
    获取指定名称的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 避免重复添加处理器
    if not logger.handlers:
        # 创建日志目录
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 创建轮转日志处理器
        file_handler = RotatingFileHandler(
            f'logs/{name}.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )

        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        # 添加处理器到日志器
        logger.addHandler(file_handler)

    return logger
