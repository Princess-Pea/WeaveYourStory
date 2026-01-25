from flask import Blueprint, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from config.settings import Config
from middleware.auth_middleware import token_required
import hashlib
import secrets

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__)
CORS(auth_bp)

from database.users_db import (
    users_db,
    get_user,
    set_user,
    user_exists,
    delete_user,
    get_all_users
)

@auth_bp.route('/api/v1/auth/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'code': 400, 
                'msg': '用户名和密码不能为空',
                'requestId': generate_request_id()
            }), 400
        
        # 检查用户是否已存在
        if user_exists(username):
            return jsonify({
                'code': 409, 
                'msg': '用户已存在',
                'requestId': generate_request_id()
            }), 409
        
        # 存储用户（密码应该加密，这里简化处理）
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        set_user(username, {
            'email': email,
            'password': hashed_password,
            'created_at': datetime.now().isoformat()
        })
        
        # 生成token
        token = jwt.encode({
            'user': username,
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow() - timedelta(seconds=10)  # 添加10秒的容差，防止时钟偏移
        }, Config.JWT_SECRET, algorithm="HS256")
        
        return jsonify({
            'code': 200,
            'msg': '注册成功',
            'requestId': generate_request_id(),
            'data': {
                'token': token,
                'user': {
                    'username': username,
                    'email': email
                }
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'注册失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'code': 400, 
                'msg': '用户名和密码不能为空',
                'requestId': generate_request_id()
            }), 400
        
        # 检查用户是否存在
        if not user_exists(username):
            return jsonify({
                'code': 401, 
                'msg': '用户名或密码错误',
                'requestId': generate_request_id()
            }), 401
        
        # 验证密码
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if users_db[username]['password'] != hashed_password:
            return jsonify({
                'code': 401, 
                'msg': '用户名或密码错误',
                'requestId': generate_request_id()
            }), 401
        
        # 生成token
        token = jwt.encode({
            'user': username,
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow() - timedelta(seconds=10)  # 添加10秒的容差，防止时钟偏移
        }, Config.JWT_SECRET, algorithm="HS256")
        
        return jsonify({
            'code': 200,
            'msg': '登录成功',
            'requestId': generate_request_id(),
            'data': {
                'token': token,
                'user': {
                    'username': username,
                    'email': get_user(username).get('email', '') if get_user(username) else ''
                }
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'登录失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

@auth_bp.route('/api/v1/auth/guest', methods=['POST'])
def guest_login():
    """游客登录 - 生成临时访客令牌"""
    try:
        import uuid
        
        # 生成唯一的访客ID
        guest_id = f"guest_{uuid.uuid4().hex[:8]}"
        guest_username = f"游客_{uuid.uuid4().hex[:6]}"
        
        # 生成游客token（有效期较短，例如1小时）
        token = jwt.encode({
            'user': guest_username,
            'guest_id': guest_id,
            'exp': datetime.utcnow() + timedelta(hours=1),  # 1小时后过期
            'iat': datetime.utcnow() - timedelta(seconds=10),  # 添加10秒的容差，防止时钟偏移
            'is_guest': True
        }, Config.JWT_SECRET, algorithm="HS256")
        
        return jsonify({
            'code': 200,
            'msg': '游客登录成功',
            'requestId': generate_request_id(),
            'data': {
                'token': token,
                'user': {
                    'username': guest_username,
                    'guest_id': guest_id,
                    'is_guest': True
                }
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'游客登录失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

@auth_bp.route('/api/v1/auth/profile', methods=['GET'])
@token_required
def get_profile():
    """获取用户资料"""
    try:
        # 从全局变量获取用户信息
        username = request.environ.get('FLASK_USER', 'guest')
        user_info = get_user(username) or {}
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'requestId': generate_request_id(),
            'data': {
                'user': {
                    'username': username,
                    'email': user_info.get('email', ''),
                    'created_at': user_info.get('created_at', '')
                }
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取用户资料失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

@auth_bp.route('/api/v1/auth/user', methods=['GET'])
@token_required
def get_current_user():
    """获取当前用户信息"""
    try:
        # 从token获取用户信息
        from flask import g
        token_payload = getattr(g, 'user', {})
        username = token_payload.get('user', 'unknown')
        is_guest = token_payload.get('is_guest', False)
        guest_id = token_payload.get('guest_id')
        
        # 获取用户详细信息
        user_detail = get_user(username) or {}
        
        user_info = {
            'username': username,
            'email': user_detail.get('email', ''),
            'is_guest': is_guest,
            'guest_id': guest_id,
            'created_at': user_detail.get('created_at', '')
        }
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'requestId': generate_request_id(),
            'data': {
                'user': user_info
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取用户信息失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

@auth_bp.route('/api/v1/auth/refresh', methods=['POST'])
def refresh_token():
    """刷新Token"""
    try:
        data = request.json
        old_token = data.get('token')
        
        if not old_token:
            return jsonify({
                'code': 400,
                'msg': '缺少旧的token',
                'requestId': generate_request_id()
            }), 400
        
        try:
            # 解码旧token获取用户信息
            payload = jwt.decode(old_token, Config.JWT_SECRET, algorithms=["HS256"])
            username = payload.get('user')
            is_guest = payload.get('is_guest', False)
            guest_id = payload.get('guest_id')
            
            # 生成新token
            new_token = jwt.encode({
                'user': username,
                'exp': datetime.utcnow() + timedelta(days=30 if not is_guest else 1),  # 游客token有效期更短
                'iat': datetime.utcnow(),
                'is_guest': is_guest,
                'guest_id': guest_id
            }, Config.JWT_SECRET, algorithm="HS256")
            
            return jsonify({
                'code': 200,
                'msg': 'Token刷新成功',
                'requestId': generate_request_id(),
                'data': {
                    'token': new_token
                }
            })
        except jwt.InvalidTokenError:
            return jsonify({
                'code': 401,
                'msg': '无效的token',
                'requestId': generate_request_id()
            }), 401
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'Token刷新失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

def generate_request_id():
    """生成请求ID"""
    return secrets.token_hex(8)