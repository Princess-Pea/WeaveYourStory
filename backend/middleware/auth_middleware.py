"""
认证中间件
负责拦截请求并验证JWT Token
"""
from flask import request, jsonify, g
from functools import wraps
from utils.jwt_util import JWTUtil
import uuid

def generate_request_id():
    """生成请求ID"""
    return f"req_{uuid.uuid4().hex[:16]}"

def auth_required(f):
    """
    认证装饰器
    用于需要鉴权的接口
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取token
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header:
            return jsonify({
                "code": 401,
                "msg": "缺少Authorization请求头",
                "requestId": generate_request_id()
            }), 401
        
        # 解析token（支持 "Bearer token" 和 "token" 两种格式）
        token = auth_header
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
        
        # 验证token
        payload = JWTUtil.verify_token(token)
        
        if not payload:
            return jsonify({
                "code": 401,
                "msg": "token无效或已过期",
                "requestId": generate_request_id()
            }), 401
        
        # 将用户ID存入请求上下文
        g.user_id = payload.get('user_id')
        g.username = payload.get('username')
        
        return f(*args, **kwargs)
    
    return decorated_function

def init_auth_middleware(app):
    """
    初始化认证中间件
    【魔搭适配点】配置请求拦截规则
    
    参数:
        app: Flask应用实例
    """
    
    # 无需鉴权的路径列表
    PUBLIC_PATHS = [
        '/api/v1/auth/register',
        '/api/v1/auth/login',
        '/api/v1/auth/refresh',
        '/swagger',
        '/api/v1/game/preview/'  # 预览接口无需鉴权
    ]
    
    @app.before_request
    def check_auth():
        """
        请求前置拦截器
        对需要鉴权的接口进行token验证
        """
        # 获取请求路径
        path = request.path
        
        # 检查是否为公开路径
        for public_path in PUBLIC_PATHS:
            if path.startswith(public_path):
                return None  # 不拦截
        
        # 静态资源不拦截
        if path.startswith('/static/'):
            return None
        
        # 其他路径需要鉴权（如果以/api开头）
        if path.startswith('/api/'):
            # 从请求头获取token
            auth_header = request.headers.get('Authorization', '')
            
            if not auth_header:
                return jsonify({
                    "code": 401,
                    "msg": "缺少Authorization请求头",
                    "requestId": generate_request_id()
                }), 401
            
            # 解析token
            token = auth_header
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
            
            # 验证token
            payload = JWTUtil.verify_token(token)
            
            if not payload:
                return jsonify({
                    "code": 401,
                    "msg": "token无效或已过期",
                    "requestId": generate_request_id()
                }), 401
            
            # 将用户信息存入请求上下文
            g.user_id = payload.get('user_id')
            g.username = payload.get('username')
            g.is_guest = payload.get('is_guest', False)  # 游客标记
        
        return None  # 放行
