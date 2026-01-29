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
    
    # =============== JWT配置 ===============
    JWT_SECRET = os.environ.get('JWT_SECRET', os.environ.get('JWT_SECRET_KEY', 'pixelforge_default_secret_key_change_in_production'))
    JWT_EXPIRATION = int(os.environ.get('JWT_EXPIRATION', 86400))  # 默认24小时
    
    # =============== 服务配置 ===============
    SERVER_PORT = int(os.environ.get('SERVER_PORT', 8888))
    
    # =============== AI服务配置 ===============
    # AI适配器类型: openai / wenxin / qianwen / modelscope
    AI_ADAPTER_TYPE = os.environ.get('AI_ADAPTER_TYPE', 'modelscope')
    AI_REQUEST_TIMEOUT = int(os.environ.get('AI_REQUEST_TIMEOUT', 60))
    AI_MAX_RETRIES = int(os.environ.get('AI_MAX_RETRIES', 3))
    
    # 魔搭社区配置（DashScope API）
    MODELSCOPE_KEY = os.environ.get('MODELSCOPE_KEY', '')
    MODELSCOPE_MODEL = os.environ.get('MODELSCOPE_MODEL', 'qwen-turbo')
    
    # OpenAI配置
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    OPENAI_API_BASE = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # 百度文心一言配置
    WENXIN_API_KEY = os.environ.get('WENXIN_API_KEY', '')
    WENXIN_SECRET_KEY = os.environ.get('WENXIN_SECRET_KEY', '')
    WENXIN_MODEL = os.environ.get('WENXIN_MODEL', 'ernie-bot-4')
    
    # 阿里通义千问配置
    QIANWEN_API_KEY = os.environ.get('QIANWEN_API_KEY', '')
    QIANWEN_MODEL = os.environ.get('QIANWEN_MODEL', 'qwen-turbo')
    
    # =============== 数据存储配置 ===============
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    USERS_DIR = os.path.join(DATA_DIR, 'users')
    USERS_FILE = os.path.join(USERS_DIR, 'users.json')
    PROJECTS_DIR = os.path.join(DATA_DIR, 'projects')
    DRAFTS_DIR = os.path.join(DATA_DIR, 'drafts')
    
    # =============== Flask配置 ===============
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
