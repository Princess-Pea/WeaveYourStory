import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import jwt
from utils.ai_wrapper import start_async_ai_task, get_task_status, generate_id

app = Flask(__name__)
CORS(app) # 允许跨域请求
app.config['SECRET_KEY'] = os.environ.get("PIXELFORGE_SECRET_KEY", "pixelforge_secret_key")

# 模拟数据库存储
projects = [
    {"id": "1", "title": "我的第一个冒险", "status": "published", "updated_at": "2026-01-20"},
    {"id": "2", "title": "森林物语", "status": "editing", "updated_at": "2026-01-22"}
]

# --- 鉴权中间件 ---
def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # 去掉 Bearer 前缀
            token = token.split(" ")[1] if " " in token else token
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

# --- 核心接口：用户与鉴权 ---
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """模拟登录，返回Token"""
    data = request.json
    # 演示目的：任何用户名/密码均可登录
    token = jwt.encode({
        'user': data.get('username'),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'])
    return jsonify({'token': token, 'username': data.get('username')})

# --- 核心接口：项目管理 ---
@app.route('/api/v1/projects', methods=['GET'])
@token_required
def get_projects():
    """查询作品列表"""
    return jsonify({"projects": projects, "requestId": generate_id()})

@app.route('/api/v1/projects', methods=['POST'])
@token_required
def create_project():
    """新建游戏项目"""
    data = request.json
    new_project = {
        "id": generate_id("proj"),
        "title": data.get("title", "未命名游戏"),
        "status": "draft",
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    projects.append(new_project)
    return jsonify({"project": new_project, "requestId": generate_id()})

# --- 核心接口：AIGC 规范化接口 ---
@app.route('/api/v1/ai/generate-game', methods=['POST'])
@token_required
def ai_generate():
    """
    异步生成游戏雏形
    请求体规范：{content: str, context: dict, params: dict}
    """
    data = request.json
    content = data.get('content', '')
    context = data.get('context', {})
    params = data.get('params', {})
    
    req_id, task_id = start_async_ai_task(content, context, params)
    
    return jsonify({
        "requestId": req_id,
        "taskId": task_id,
        "message": "AI任务已启动，请轮询状态"
    }), 202

@app.route('/api/v1/ai/task/<task_id>', methods=['GET'])
@token_required
def check_ai_status(task_id):
    """查询异步任务状态"""
    status_data = get_task_status(task_id)
    return jsonify({
        "requestId": generate_id(),
        "taskId": task_id,
        **status_data
    })

# --- 可视化编辑与预览 ---
@app.route('/api/v1/projects/<proj_id>/data', methods=['GET'])
@token_required
def get_project_data(proj_id):
    """获取预览或编辑所需的项目详情数据"""
    # 模拟返回一个固定的游戏结构
    return jsonify({
        "game_data": {
            "title": "森林物语",
            "scenes": [
                {"id": "s1", "text": "欢迎来到像素世界！", "options": [{"text": "开始", "next": "s2"}]},
                {"id": "s2", "text": "你看到一只像素猫。", "options": [{"text": "摸它", "next": "s1"}]}
            ]
        },
        "requestId": generate_id()
    })

if __name__ == '__main__':
    # 启动后端，端口5000
    app.run(debug=True, host='0.0.0.0', port=5000)
