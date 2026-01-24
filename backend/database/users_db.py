"""
用户数据库模块
用于在多个蓝图之间共享用户数据
"""

# 模拟用户数据库 - 使用字典作为内存存储
users_db = {}


def get_user(username):
    """获取用户信息"""
    return users_db.get(username)


def set_user(username, user_data):
    """设置用户信息"""
    users_db[username] = user_data


def delete_user(username):
    """删除用户"""
    if username in users_db:
        del users_db[username]


def user_exists(username):
    """检查用户是否存在"""
    return username in users_db


def get_all_users():
    """获取所有用户"""
    return users_db.copy()