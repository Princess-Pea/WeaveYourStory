"""
用户认证接口模块
提供注册、登录、token刷新、用户信息查询等接口
"""
from flask import Blueprint, request, jsonify, g
from utils.jwt_util import JWTUtil
from utils.password_util import PasswordUtil
from utils.user_storage import UserStorage
from config.settings import Config
import uuid

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# 初始化用户存储
user_storage = UserStorage()

def generate_request_id():
    """生成请求ID"""
    return f"req_{uuid.uuid4().hex[:16]}"

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册接口
    
    请求体:
        {
            "username": "用户名",
            "password": "密码",
            "email": "邮箱（可选）"
        }
    
    响应体:
        {
            "code": 200,
            "msg": "注册成功",
            "requestId": "req_xxx",
            "data": {
                "user_id": "xxx",
                "username": "xxx"
            }
        }
    """
    request_id = generate_request_id()
    
    try:
        data = request.json
        
        # 验证必填字段
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()
        
        if not username:
            return jsonify({
                "code": 400,
                "msg": "用户名不能为空",
                "requestId": request_id
            }), 400
        
        if not password:
            return jsonify({
                "code": 400,
                "msg": "密码不能为空",
                "requestId": request_id
            }), 400
        
        if len(password) < 6:
            return jsonify({
                "code": 400,
                "msg": "密码长度至少为6位",
                "requestId": request_id
            }), 400
        
        # 加密密码
        hashed_password = PasswordUtil.hash_password(password)
        
        # 创建用户
        user = user_storage.create_user(username, hashed_password, email)
        
        if not user:
            return jsonify({
                "code": 400,
                "msg": "用户名已存在",
                "requestId": request_id
            }), 400
        
        # 返回成功响应
        return jsonify({
            "code": 200,
            "msg": "注册成功",
            "requestId": request_id,
            "data": {
                "user_id": user['user_id'],
                "username": user['username']
            }
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"注册失败: {str(e)}",
            "requestId": request_id
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录接口
    
    请求体:
        {
            "username": "用户名",
            "password": "密码"
        }
    
    响应体:
        {
            "code": 200,
            "msg": "登录成功",
            "requestId": "req_xxx",
            "data": {
                "token": "jwt_token_string",
                "expires_in": 86400,
                "user_id": "xxx",
                "username": "xxx"
            }
        }
    """
    request_id = generate_request_id()
    
    try:
        data = request.json
        
        # 验证必填字段
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({
                "code": 400,
                "msg": "用户名和密码不能为空",
                "requestId": request_id
            }), 400
        
        # 查询用户
        user = user_storage.find_user_by_username(username)
        
        if not user:
            return jsonify({
                "code": 401,
                "msg": "用户名或密码错误",
                "requestId": request_id
            }), 401
        
        # 验证密码
        if not PasswordUtil.verify_password(password, user['password']):
            return jsonify({
                "code": 401,
                "msg": "用户名或密码错误",
                "requestId": request_id
            }), 401
        
        # 生成JWT Token
        token = JWTUtil.generate_token(user['user_id'], user['username'])
        
        # 返回成功响应
        return jsonify({
            "code": 200,
            "msg": "登录成功",
            "requestId": request_id,
            "data": {
                "token": token,
                "expires_in": Config.JWT_EXPIRATION,
                "user_id": user['user_id'],
                "username": user['username']
            }
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"登录失败: {str(e)}",
            "requestId": request_id
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """
    刷新Token接口
    
    请求体:
        {
            "token": "旧的JWT Token"
        }
    
    响应体:
        {
            "code": 200,
            "msg": "刷新成功",
            "requestId": "req_xxx",
            "data": {
                "token": "新的JWT Token",
                "expires_in": 86400
            }
        }
    """
    request_id = generate_request_id()
    
    try:
        data = request.json
        old_token = data.get('token', '')
        
        if not old_token:
            return jsonify({
                "code": 400,
                "msg": "Token不能为空",
                "requestId": request_id
            }), 400
        
        # 刷新Token
        new_token = JWTUtil.refresh_token(old_token)
        
        if not new_token:
            return jsonify({
                "code": 401,
                "msg": "Token无效或已过期",
                "requestId": request_id
            }), 401
        
        # 返回新Token
        return jsonify({
            "code": 200,
            "msg": "刷新成功",
            "requestId": request_id,
            "data": {
                "token": new_token,
                "expires_in": Config.JWT_EXPIRATION
            }
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"Token刷新失败: {str(e)}",
            "requestId": request_id
        }), 500

@auth_bp.route('/info', methods=['GET'])
def get_user_info():
    """
    获取当前登录用户信息接口（需要鉴权）
    
    响应体:
        {
            "code": 200,
            "msg": "success",
            "requestId": "req_xxx",
            "data": {
                "user_id": "xxx",
                "username": "xxx",
                "email": "xxx",
                "created_at": "2026-01-23T12:00:00"
            }
        }
    """
    request_id = generate_request_id()
    
    try:
        # 从请求上下文获取用户ID（由中间件注入）
        user_id = g.get('user_id')
        
        if not user_id:
            return jsonify({
                "code": 401,
                "msg": "未登录或token无效",
                "requestId": request_id
            }), 401
        
        # 查询用户信息
        user_info = user_storage.get_user_safe(user_id)
        
        if not user_info:
            return jsonify({
                "code": 404,
                "msg": "用户不存在",
                "requestId": request_id
            }), 404
        
        # 返回用户信息
        return jsonify({
            "code": 200,
            "msg": "success",
            "requestId": request_id,
            "data": user_info
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"获取用户信息失败: {str(e)}",
            "requestId": request_id
        }), 500

@auth_bp.route('/guest', methods=['POST'])
def guest_login():
    """
    游客登录接口
    无需注册，生成临时游客Token
    
    响应体:
        {
            "code": 200,
            "msg": "游客登录成功",
            "requestId": "req_xxx",
            "data": {
                "token": "xxx",
                "expires_in": 86400,
                "user_id": "guest_xxx",
                "username": "游客",
                "is_guest": true
            }
        }
    """
    request_id = generate_request_id()
    
    try:
        # 生成游客ID
        guest_id = f"guest_{uuid.uuid4().hex[:12]}"
        guest_name = "游客"
        
        # 生成游客Token（标记为游客身份）
        token = JWTUtil.generate_token(guest_id, guest_name, is_guest=True)
        
        return jsonify({
            "code": 200,
            "msg": "游客登录成功",
            "requestId": request_id,
            "data": {
                "token": token,
                "expires_in": Config.JWT_EXPIRATION,
                "user_id": guest_id,
                "username": guest_name,
                "is_guest": True
            }
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"游客登录失败: {str(e)}",
            "requestId": request_id
        }), 500
