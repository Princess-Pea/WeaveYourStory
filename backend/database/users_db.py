"""
用户数据库模块
支持内存存储与文件持久化同步
"""
import json
import os
import threading
from config.settings import Config

# 模拟用户数据库 - 使用字典作为内存存储
users_db = {}
# 文件操作锁，确保并发安全
db_lock = threading.Lock()

def _load_db():
    """从文件加载数据库"""
    global users_db
    try:
        if os.path.exists(Config.USERS_FILE):
            with open(Config.USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 兼容旧格式（如果是列表转为字典）
                if isinstance(data, dict) and "users" in data:
                    if isinstance(data["users"], list):
                        # 如果是旧的列表格式，转为以 username 为键的字典
                        new_db = {}
                        for user in data["users"]:
                            if "username" in user:
                                uname = user.pop("username")
                                new_db[uname] = user
                        users_db = new_db
                    else:
                        users_db = data["users"]
                else:
                    users_db = data
    except Exception as e:
        print(f"加载用户数据库失败: {e}")
        users_db = {}

def _save_db():
    """保存数据库到文件"""
    try:
        # 确保目录存在
        os.makedirs(Config.USERS_DIR, exist_ok=True)
        with open(Config.USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_db, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存用户数据库失败: {e}")

# 初始化加载
_load_db()

def get_user(username):
    """获取用户信息"""
    with db_lock:
        return users_db.get(username)

def set_user(username, user_data):
    """设置用户信息并持久化"""
    with db_lock:
        users_db[username] = user_data
        _save_db()

def delete_user(username):
    """删除用户并持久化"""
    with db_lock:
        if username in users_db:
            del users_db[username]
            _save_db()

def user_exists(username):
    """检查用户是否存在"""
    with db_lock:
        return username in users_db

def get_all_users():
    """获取所有用户"""
    with db_lock:
        return users_db.copy()