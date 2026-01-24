"""
JWT工具类
负责JWT Token的生成、验证和解析
"""
import jwt
import datetime
from config.settings import Config

class JWTUtil:
    """
    JWT工具类
    提供token生成、验证、解析功能
    """
    
    @staticmethod
    def generate_token(user_id, username, expires_in=None):
        """
        生成JWT Token
        
        参数:
            user_id (str): 用户ID
            username (str): 用户名
            expires_in (int): 过期时间（秒），默认使用配置中的JWT_EXPIRATION
            
        返回:
            str: JWT Token字符串
        """
        if expires_in is None:
            expires_in = Config.JWT_EXPIRATION
        
        # 计算过期时间
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        
        # 构造payload
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': exp_time,
            'iat': datetime.datetime.utcnow()  # 签发时间
        }
        
        # 生成token
        token = jwt.encode(payload, Config.JWT_SECRET, algorithm='HS256')
        
        return token
    
    @staticmethod
    def verify_token(token):
        """
        验证JWT Token是否有效
        
        参数:
            token (str): JWT Token字符串
            
        返回:
            dict: 验证成功返回payload字典，失败返回None
        """
        try:
            # 解码并验证token
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            # Token已过期
            return None
        except jwt.InvalidTokenError:
            # Token无效
            return None
    
    @staticmethod
    def parse_user_id(token):
        """
        从Token中解析用户ID
        
        参数:
            token (str): JWT Token字符串
            
        返回:
            str: 用户ID，解析失败返回None
        """
        payload = JWTUtil.verify_token(token)
        if payload:
            return payload.get('user_id')
        return None
    
    @staticmethod
    def refresh_token(old_token):
        """
        刷新Token（生成新的Token）
        
        参数:
            old_token (str): 旧的JWT Token
            
        返回:
            str: 新的JWT Token，验证失败返回None
        """
        payload = JWTUtil.verify_token(old_token)
        if not payload:
            return None
        
        # 使用旧token中的用户信息生成新token
        user_id = payload.get('user_id')
        username = payload.get('username')
        
        return JWTUtil.generate_token(user_id, username)
