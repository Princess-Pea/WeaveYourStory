"""
密码加密工具类
使用bcrypt进行密码加密和验证
"""
import bcrypt

class PasswordUtil:
    """
    密码工具类
    提供密码加密和验证功能
    """
    
    @staticmethod
    def hash_password(password):
        """
        加密密码
        
        参数:
            password (str): 明文密码
            
        返回:
            str: 加密后的密码哈希值
        """
        # 将密码转换为bytes
        password_bytes = password.encode('utf-8')
        
        # 生成盐值并加密
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # 返回字符串格式
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed_password):
        """
        验证密码是否正确
        
        参数:
            password (str): 用户输入的明文密码
            hashed_password (str): 数据库中存储的加密密码
            
        返回:
            bool: 密码正确返回True，否则返回False
        """
        try:
            # 将字符串转换为bytes
            password_bytes = password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            
            # 验证密码
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception as e:
            # 验证失败（可能是格式错误）
            print(f"密码验证异常: {str(e)}")
            return False
