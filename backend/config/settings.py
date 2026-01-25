"""
魔搭创空间环境配置读取模块
负责读取和管理所有环境变量配置
"""
import os
from dotenv import load_dotenv
import warnings

# 加载.env文件（如果存在）
try:
    load_dotenv()
except Exception as e:
    warnings.warn(f"无法加载.env文件: {e}")


class Config:
    """
    配置类 - 从魔搭创空间环境变量读取配置
    """
    
    # 【魔搭适配点】JWT秘钥配置（必填）
    # 魔搭创空间需在环境变量中配置 JWT_SECRET 或 JWT_SECRET_KEY
    JWT_SECRET = os.environ.get('JWT_SECRET', os.environ.get('JWT_SECRET_KEY', 'pixelforge_default_secret_key_change_in_production'))
    
    # 【魔搭适配点】服务端口配置
    # 魔搭创空间默认使用8888端口
    SERVER_PORT = int(os.environ.get('SERVER_PORT', 8888))
    
    # JWT Token过期时间（秒）
    JWT_EXPIRATION = int(os.environ.get('JWT_EXPIRATION', 86400))  # 默认24小时
    
    # 【魔搭适配点】数据存储路径
    # 魔搭创空间本地文件存储路径
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    USERS_DIR = os.path.join(DATA_DIR, 'users')
    USERS_FILE = os.path.join(USERS_DIR, 'users.json')
    
    # 项目和草稿存储路径
    PROJECTS_DIR = os.path.join(DATA_DIR, 'projects')
    DRAFTS_DIR = os.path.join(DATA_DIR, 'drafts')
    
    # Flask配置
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', JWT_SECRET)
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    @classmethod
    def init_directories(cls):
        """
        初始化必要的目录结构
        【魔搭适配点】确保数据目录存在
        """
        try:
            os.makedirs(cls.DATA_DIR, exist_ok=True)
            os.makedirs(cls.USERS_DIR, exist_ok=True)
            os.makedirs(cls.PROJECTS_DIR, exist_ok=True)
            os.makedirs(cls.DRAFTS_DIR, exist_ok=True)
            
            # 如果users.json不存在，创建空文件
            if not os.path.exists(cls.USERS_FILE):
                import json
                with open(cls.USERS_FILE, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"初始化目录失败: {e}")
            # 如果无法创建目录，尝试使用临时目录
            cls.USERS_FILE = os.path.join("/tmp", "users.json")
            if not os.path.exists(cls.USERS_FILE):
                import json
                with open(cls.USERS_FILE, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
