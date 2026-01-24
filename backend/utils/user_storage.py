"""
用户数据存储工具类
【魔搭适配点】使用JSON文件存储用户数据
【TODO】后续需要迁移到MySQL/MongoDB等数据库
"""
import json
import os
import uuid
import datetime
from config.settings import Config

class UserStorage:
    """
    用户数据存储类
    当前使用JSON文件存储，预留数据库迁移接口
    """
    
    def __init__(self):
        """初始化存储类，确保数据文件存在"""
        Config.init_directories()
        self.users_file = Config.USERS_FILE
    
    def _read_users(self):
        """
        读取所有用户数据
        
        返回:
            list: 用户列表
        """
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('users', [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _write_users(self, users):
        """
        写入所有用户数据
        
        参数:
            users (list): 用户列表
        """
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump({"users": users}, f, ensure_ascii=False, indent=2)
    
    def create_user(self, username, hashed_password, email=None):
        """
        创建新用户
        【TODO】数据库迁移时，改为INSERT INTO users语句
        
        参数:
            username (str): 用户名
            hashed_password (str): 加密后的密码
            email (str): 邮箱（可选）
            
        返回:
            dict: 创建成功返回用户信息，失败返回None
        """
        users = self._read_users()
        
        # 检查用户名是否已存在
        if any(u['username'] == username for u in users):
            return None
        
        # 生成用户ID
        user_id = str(uuid.uuid4())
        
        # 构造用户对象
        user = {
            'user_id': user_id,
            'username': username,
            'password': hashed_password,
            'email': email or '',
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        
        # 添加到用户列表
        users.append(user)
        
        # 写入文件
        self._write_users(users)
        
        return user
    
    def find_user_by_username(self, username):
        """
        根据用户名查询用户
        【TODO】数据库迁移时，改为SELECT * FROM users WHERE username=? 语句
        
        参数:
            username (str): 用户名
            
        返回:
            dict: 用户信息，不存在返回None
        """
        users = self._read_users()
        
        for user in users:
            if user['username'] == username:
                return user
        
        return None
    
    def find_user_by_id(self, user_id):
        """
        根据用户ID查询用户
        【TODO】数据库迁移时，改为SELECT * FROM users WHERE user_id=? 语句
        
        参数:
            user_id (str): 用户ID
            
        返回:
            dict: 用户信息，不存在返回None
        """
        users = self._read_users()
        
        for user in users:
            if user['user_id'] == user_id:
                return user
        
        return None
    
    def update_user(self, user_id, **kwargs):
        """
        更新用户信息
        【TODO】数据库迁移时，改为UPDATE users SET ... WHERE user_id=? 语句
        
        参数:
            user_id (str): 用户ID
            **kwargs: 要更新的字段（如email='new@email.com'）
            
        返回:
            bool: 更新成功返回True，否则返回False
        """
        users = self._read_users()
        
        for user in users:
            if user['user_id'] == user_id:
                # 更新字段
                for key, value in kwargs.items():
                    if key in user:
                        user[key] = value
                
                # 更新时间戳
                user['updated_at'] = datetime.datetime.now().isoformat()
                
                # 写入文件
                self._write_users(users)
                return True
        
        return False
    
    def get_user_safe(self, user_id):
        """
        获取用户安全信息（不包含密码）
        
        参数:
            user_id (str): 用户ID
            
        返回:
            dict: 用户信息（不包含password字段），不存在返回None
        """
        user = self.find_user_by_id(user_id)
        
        if not user:
            return None
        
        # 复制用户信息并移除密码字段
        safe_user = user.copy()
        safe_user.pop('password', None)
        
        return safe_user
