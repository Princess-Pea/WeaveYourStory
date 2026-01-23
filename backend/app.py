import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import jwt
import json
import time
from utils.ai_wrapper import start_async_ai_task, get_task_status, generate_id
from utils.ai_adapter import ai_adapter

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
@app.route('/api/v1/ai/game/submit', methods=['POST'])
@token_required
def ai_submit_game():
    """
    异步提交游戏原稿，生成游戏雏形
    请求体规范：{content: str, context: dict, params: dict}
    """
    data = request.json
    content = data.get('content', '')
    context = data.get('context', {})
    params = data.get('params', {})
    
    # 解析结构化的原稿内容
    try:
        manuscript_data = json.loads(content)
    except json.JSONDecodeError:
        return jsonify({"code": 400, "msg": "content格式错误，应为JSON字符串", "requestId": generate_id()}), 400
    
    # 生成任务ID和游戏ID
    task_id = generate_id("task")
    game_id = generate_id("game")
    
    # 存储原稿数据到本地文件（模拟数据库存储）
    import os
    
    # 确保数据目录存在
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 保存原稿到JSON文件
    manuscript_file_path = os.path.join(data_dir, f"manuscript_{game_id}.json")
    with open(manuscript_file_path, 'w', encoding='utf-8') as f:
        json.dump({
            "gameId": game_id,
            "manuscript": manuscript_data,
            "context": context,
            "params": params,
            "createdAt": datetime.datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)
    
    # 开始异步AI生成任务
    req_id = generate_id("req")
    start_async_ai_task(content, context, params, task_id)  # 传递task_id给后台任务
    
    return jsonify({
        "code": 200,
        "msg": "task_submitted",
        "requestId": req_id,
        "data": {
            "taskId": task_id,
            "gameId": game_id
        }
    })

@app.route('/api/v1/ai/task/<task_id>', methods=['GET'])
@token_required
def get_task_status_api(task_id):
    """
    查询异步任务状态
    响应体规范：{code:200, msg:"success", data: {taskId:"xxx", status:"completed/failed/pending", progress:80, result:{...}, errorMsg:""}}
    """
    task_data = get_task_status(task_id)
    
    # 根据内部状态映射到规范状态
    status_mapping = {
        "not_found": "pending",
        "processing": "pending",
        "completed": "completed",
        "failed": "failed"
    }
    
    normalized_status = status_mapping.get(task_data.get("status", "not_found"), "pending")
    
    response_data = {
        "code": 200,
        "msg": "success",
        "requestId": generate_id(),
        "data": {
            "taskId": task_id,
            "status": normalized_status,
            "progress": task_data.get("progress", 0),
            "result": task_data.get("result", None),
            "errorMsg": task_data.get("errorMsg", "")
        }
    }
    
    return jsonify(response_data)

# --- AI辅助接口 ---
@app.route('/api/v1/ai/assist/scene', methods=['POST'])
@token_required
def ai_assist_scene():
    """
    AI辅助生成场景
    请求体规范：{content: str, context: dict, params: dict}
    响应体规范：{code:200, msg:"success", requestId:"xxx", cost:0.5, data: {result: "AI生成的内容"}}
    """
    start_time = time.time()
    data = request.json
    content = data.get('content', '')
    context = data.get('context', {})
    params = data.get('params', {})
    
    try:
        result = ai_adapter.assist_with_scene(content, context, params)
        
        response_data = {
            "code": 200,
            "msg": "success",
            "requestId": generate_id(),
            "cost": round(time.time() - start_time, 2),
            "data": {
                "result": result
            }
        }
        return jsonify(response_data)
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"AI辅助生成场景失败: {str(e)}",
            "requestId": generate_id(),
            "cost": round(time.time() - start_time, 2),
            "data": {
                "result": ""
            }
        }), 500

@app.route('/api/v1/ai/assist/dialog', methods=['POST'])
@token_required
def ai_assist_dialog():
    """
    AI辅助生成对话
    请求体规范：{content: str, context: dict, params: dict}
    响应体规范：{code:200, msg:"success", requestId:"xxx", cost:0.5, data: {result: "AI生成的内容"}}
    """
    start_time = time.time()
    data = request.json
    content = data.get('content', '')
    context = data.get('context', {})
    params = data.get('params', {})
    
    try:
        result = ai_adapter.assist_with_dialog(content, context, params)
        
        response_data = {
            "code": 200,
            "msg": "success",
            "requestId": generate_id(),
            "cost": round(time.time() - start_time, 2),
            "data": {
                "result": result
            }
        }
        return jsonify(response_data)
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"AI辅助生成对话失败: {str(e)}",
            "requestId": generate_id(),
            "cost": round(time.time() - start_time, 2),
            "data": {
                "result": ""
            }
        }), 500

@app.route('/api/v1/ai/assist/task', methods=['POST'])
@token_required
def ai_assist_task():
    """
    AI辅助设计任务
    请求体规范：{content: str, context: dict, params: dict}
    响应体规范：{code:200, msg:"success", requestId:"xxx", cost:0.5, data: {result: "AI生成的内容"}}
    """
    start_time = time.time()
    data = request.json
    content = data.get('content', '')
    context = data.get('context', {})
    params = data.get('params', {})
    
    try:
        result = ai_adapter.assist_with_task(content, context, params)
        
        response_data = {
            "code": 200,
            "msg": "success",
            "requestId": generate_id(),
            "cost": round(time.time() - start_time, 2),
            "data": {
                "result": result
            }
        }
        return jsonify(response_data)
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"AI辅助设计任务失败: {str(e)}",
            "requestId": generate_id(),
            "cost": round(time.time() - start_time, 2),
            "data": {
                "result": ""
            }
        }), 500

@app.route('/api/v1/game/save', methods=['POST'])
@token_required
def save_game():
    """
    保存编辑后的游戏数据
    """
    data = request.json
    game_id = data.get('gameId', '')
    game_data = data.get('gameData', {})
    
    if not game_id or not game_data:
        return jsonify({"code": 400, "msg": "缺少必要参数", "requestId": generate_id()}), 400
    
    # 保存到本地文件
    import os
    import json
    
    # 确保数据目录存在
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 保存游戏数据到JSON文件
    game_file_path = os.path.join(data_dir, f"game_{game_id}.json")
    with open(game_file_path, 'w', encoding='utf-8') as f:
        json.dump(game_data, f, ensure_ascii=False, indent=2)
    
    return jsonify({
        "code": 200,
        "msg": "保存成功",
        "requestId": generate_id(),
        "data": {"gameId": game_id}
    })

# --- 预览数据接口 ---
@app.route('/api/v1/game/preview/<game_id>', methods=['GET'])
@token_required
def get_game_preview(game_id):
    """
    根据gameId返回最新的游戏结构化数据
    """
    import os
    import json
    
    # 构造游戏数据文件路径
    game_file_path = os.path.join("data", f"game_{game_id}.json")
    
    if not os.path.exists(game_file_path):
        return jsonify({"code": 404, "msg": "游戏数据不存在", "requestId": generate_id()}), 404
    
    try:
        with open(game_file_path, 'r', encoding='utf-8') as f:
            game_data = json.load(f)
        
        return jsonify({
            "code": 200,
            "msg": "success",
            "requestId": generate_id(),
            "data": game_data
        })
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"读取游戏数据失败: {str(e)}",
            "requestId": generate_id()
        }), 500

@app.route('/api/v1/asset/pixel', methods=['GET'])
@token_required
def get_pixel_assets():
    """
    返回像素风素材信息（预留接口）
    """
    # 这里返回可用的像素风素材列表
    assets = {
        "characters": [
            {"id": "player", "name": "玩家", "url": "/assets/pixel/player.png"},
            {"id": "npc1", "name": "村民", "url": "/assets/pixel/npc1.png"},
            {"id": "npc2", "name": "商人", "url": "/assets/pixel/npc2.png"}
        ],
        "objects": [
            {"id": "chest", "name": "宝箱", "url": "/assets/pixel/chest.png"},
            {"id": "door", "name": "门", "url": "/assets/pixel/door.png"},
            {"id": "tree", "name": "树", "url": "/assets/pixel/tree.png"}
        ],
        "backgrounds": [
            {"id": "grassland", "name": "草地", "url": "/assets/pixel/grassland.png"},
            {"id": "forest", "name": "森林", "url": "/assets/pixel/forest.png"},
            {"id": "village", "name": "村庄", "url": "/assets/pixel/village.png"}
        ]
    }
    
    return jsonify({
        "code": 200,
        "msg": "success",
        "requestId": generate_id(),
        "data": assets
    })

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
