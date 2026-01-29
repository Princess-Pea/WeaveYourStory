from functools import wraps
from flask import request, jsonify, g
import jwt
import datetime
from config.settings import Config
import traceback


def init_auth_middleware(app):
    """初始化认证中间件"""
    @app.before_request
    def check_auth():
        # 不需要认证的路径
        public_paths = [
            '/api/v1/auth/login',
            '/api/v1/auth/register',
            '/api/v1/auth/guest',
            '/api/v1/health',
            '/',
            '/index.html'
        ]
        
        # 检查是否为公共路径
        for path in public_paths:
            if request.path.startswith(path):
                return None
        
        # 检查认证头部
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Missing authorization header', 'code': 401}), 401
            
        try:
            # 解析token
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header
            payload = jwt.decode(
                token, 
                Config.JWT_SECRET, 
                algorithms=["HS256"]
            )
            
            # 将用户信息存储到请求上下文中
            g.user = payload
            g.token = token
            
        except jwt.ExpiredSignatureError as e:
            print(f"[AUTH] Token已过期: {str(e)}")
            return jsonify({'error': 'Token has expired', 'code': 401}), 401
        except jwt.InvalidTokenError as e:
            print(f"[AUTH] Token无效: {str(e)}")
            return jsonify({'error': 'Invalid token', 'code': 401}), 401
        except Exception as e:
            print(f"[AUTH] 认证中间件错误: {str(e)}")
            traceback.print_exc()
            return jsonify({'error': 'Authentication error', 'code': 401}), 401
    
    return app


def token_required(f):
    """装饰器：需要认证的路由"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing!', 'code': 401}), 401
        
        try:
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header
            payload = jwt.decode(
                token, 
                Config.JWT_SECRET, 
                algorithms=["HS256"]
            )
            g.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!', 'code': 401}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!', 'code': 401}), 401
        
        return f(*args, **kwargs)
    return decorated