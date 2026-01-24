"""
项目和草稿管理接口模块
提供草稿保存、项目管理等接口
"""
from flask import Blueprint, request, jsonify, g
from utils.project_storage import ProjectStorage
import uuid

# 创建项目管理蓝图
projects_bp = Blueprint('projects', __name__, url_prefix='/api/v1/projects')

# 初始化项目存储
project_storage = ProjectStorage()

def generate_request_id():
    """生成请求ID"""
    return f"req_{uuid.uuid4().hex[:16]}"

# ==================== 草稿管理接口 ====================

@projects_bp.route('/drafts', methods=['POST'])
def save_draft():
    """
    保存草稿接口（新建或更新）
    
    请求体:
        {
            "draft_id": "草稿ID（更新时传入，新建时不传）",
            "title": "草稿标题",
            "manuscript": {
                "story": "剧情描述",
                "characters": [...],
                "tasks": [...]
            }
        }
    
    响应体:
        {
            "code": 200,
            "msg": "保存成功",
            "requestId": "req_xxx",
            "data": {
                "draft_id": "xxx",
                "title": "xxx",
                "updated_at": "2026-01-24T12:00:00"
            }
        }
    """
    request_id = generate_request_id()
    
    try:
        # 从请求上下文获取用户ID
        user_id = g.get('user_id')
        is_guest = g.get('is_guest', False)
        
        if not user_id:
            return jsonify({
                "code": 401,
                "msg": "未登录或token无效",
                "requestId": request_id
            }), 401
        
        # 检查是否为游客
        if is_guest:
            return jsonify({
                "code": 403,
                "msg": "游客模式不支持保存功能，请注册登录后使用",
                "requestId": request_id,
                "data": {
                    "guest_mode": True
                }
            }), 403
        
        data = request.json
        draft_id = data.get('draft_id')
        title = data.get('title', '')
        manuscript = data.get('manuscript', {})
        
        # 保存草稿
        draft = project_storage.save_draft(user_id, draft_id, title, manuscript)
        
        if not draft:
            return jsonify({
                "code": 500,
                "msg": "保存草稿失败",
                "requestId": request_id
            }), 500
        
        # 返回成功响应
        return jsonify({
            "code": 200,
            "msg": "保存成功",
            "requestId": request_id,
            "data": {
                "draft_id": draft['draft_id'],
                "title": draft['title'],
                "updated_at": draft['updated_at']
            }
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"保存草稿失败: {str(e)}",
            "requestId": request_id
        }), 500

@projects_bp.route('/drafts', methods=['GET'])
def list_drafts():
    """
    获取草稿列表接口
    
    响应体:
        {
            "code": 200,
            "msg": "success",
            "requestId": "req_xxx",
            "data": {
                "drafts": [
                    {
                        "draft_id": "xxx",
                        "title": "xxx",
                        "status": "draft",
                        "created_at": "2026-01-24T12:00:00",
                        "updated_at": "2026-01-24T12:00:00"
                    }
                ],
                "total": 10
            }
        }
    """
    request_id = generate_request_id()
    
    try:
        # 从请求上下文获取用户ID
        user_id = g.get('user_id')
        
        if not user_id:
            return jsonify({
                "code": 401,
                "msg": "未登录或token无效",
                "requestId": request_id
            }), 401
        
        # 获取草稿列表
        drafts = project_storage.list_drafts(user_id)
        
        # 返回成功响应（不包含完整manuscript数据，只返回元信息）
        draft_list = [
            {
                "draft_id": draft['draft_id'],
                "title": draft['title'],
                "status": draft['status'],
                "created_at": draft['created_at'],
                "updated_at": draft['updated_at']
            }
            for draft in drafts
        ]
        
        return jsonify({
            "code": 200,
            "msg": "success",
            "requestId": request_id,
            "data": {
                "drafts": draft_list,
                "total": len(draft_list)
            }
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"获取草稿列表失败: {str(e)}",
            "requestId": request_id
        }), 500

@projects_bp.route('/drafts/<draft_id>', methods=['GET'])
def get_draft(draft_id):
    """
    获取草稿详情接口
    
    响应体:
        {
            "code": 200,
            "msg": "success",
            "requestId": "req_xxx",
            "data": {
                "draft_id": "xxx",
                "title": "xxx",
                "manuscript": {...},
                "status": "draft",
                "created_at": "2026-01-24T12:00:00",
                "updated_at": "2026-01-24T12:00:00"
            }
        }
    """
    request_id = generate_request_id()
    
    try:
        # 从请求上下文获取用户ID
        user_id = g.get('user_id')
        
        if not user_id:
            return jsonify({
                "code": 401,
                "msg": "未登录或token无效",
                "requestId": request_id
            }), 401
        
        # 获取草稿详情
        draft = project_storage.get_draft(user_id, draft_id)
        
        if not draft:
            return jsonify({
                "code": 404,
                "msg": "草稿不存在",
                "requestId": request_id
            }), 404
        
        # 返回完整草稿数据
        return jsonify({
            "code": 200,
            "msg": "success",
            "requestId": request_id,
            "data": draft
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"获取草稿详情失败: {str(e)}",
            "requestId": request_id
        }), 500

@projects_bp.route('/drafts/<draft_id>', methods=['DELETE'])
def delete_draft(draft_id):
    """
    删除草稿接口
    
    响应体:
        {
            "code": 200,
            "msg": "删除成功",
            "requestId": "req_xxx"
        }
    """
    request_id = generate_request_id()
    
    try:
        # 从请求上下文获取用户ID
        user_id = g.get('user_id')
        
        if not user_id:
            return jsonify({
                "code": 401,
                "msg": "未登录或token无效",
                "requestId": request_id
            }), 401
        
        # 删除草稿
        success = project_storage.delete_draft(user_id, draft_id)
        
        if not success:
            return jsonify({
                "code": 404,
                "msg": "草稿不存在",
                "requestId": request_id
            }), 404
        
        # 返回成功响应
        return jsonify({
            "code": 200,
            "msg": "删除成功",
            "requestId": request_id
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"删除草稿失败: {str(e)}",
            "requestId": request_id
        }), 500

# ==================== 项目管理接口 ====================

@projects_bp.route('/', methods=['POST'])
def save_project():
    """
    保存项目接口（新建或更新）
    
    请求体:
        {
            "project_id": "项目ID（更新时传入，新建时不传）",
            "title": "项目标题",
            "game_data": {
                "scenes": [...],
                "characters": [...],
                "tasks": [...]
            },
            "status": "draft/editing/published"
        }
    
    响应体:
        {
            "code": 200,
            "msg": "保存成功",
            "requestId": "req_xxx",
            "data": {
                "project_id": "xxx",
                "title": "xxx",
                "status": "xxx",
                "updated_at": "2026-01-24T12:00:00"
            }
        }
    """
    request_id = generate_request_id()
    
    try:
        # 从请求上下文获取用户ID
        user_id = g.get('user_id')
        is_guest = g.get('is_guest', False)
        
        if not user_id:
            return jsonify({
                "code": 401,
                "msg": "未登录或token无效",
                "requestId": request_id
            }), 401
        
        # 检查是否为游客
        if is_guest:
            return jsonify({
                "code": 403,
                "msg": "游客模式不支持保存功能，请注册登录后使用",
                "requestId": request_id,
                "data": {
                    "guest_mode": True
                }
            }), 403
        
        data = request.json
        project_id = data.get('project_id')
        title = data.get('title', '')
        game_data = data.get('game_data', {})
        status = data.get('status', 'draft')
        
        # 保存项目
        project = project_storage.save_project(user_id, project_id, title, game_data, status)
        
        if not project:
            return jsonify({
                "code": 500,
                "msg": "保存项目失败",
                "requestId": request_id
            }), 500
        
        # 返回成功响应
        return jsonify({
            "code": 200,
            "msg": "保存成功",
            "requestId": request_id,
            "data": {
                "project_id": project['project_id'],
                "title": project['title'],
                "status": project['status'],
                "updated_at": project['updated_at']
            }
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"保存项目失败: {str(e)}",
            "requestId": request_id
        }), 500

@projects_bp.route('/', methods=['GET'])
def list_projects():
    """
    获取项目列表接口
    
    查询参数:
        status: 状态过滤（可选，draft/editing/published）
    
    响应体:
        {
            "code": 200,
            "msg": "success",
            "requestId": "req_xxx",
            "data": {
                "projects": [
                    {
                        "project_id": "xxx",
                        "title": "xxx",
                        "status": "xxx",
                        "created_at": "2026-01-24T12:00:00",
                        "updated_at": "2026-01-24T12:00:00"
                    }
                ],
                "total": 10
            }
        }
    """
    request_id = generate_request_id()
    
    try:
        # 从请求上下文获取用户ID
        user_id = g.get('user_id')
        
        if not user_id:
            return jsonify({
                "code": 401,
                "msg": "未登录或token无效",
                "requestId": request_id
            }), 401
        
        # 获取状态过滤参数
        status = request.args.get('status')
        
        # 获取项目列表
        projects = project_storage.list_projects(user_id, status)
        
        # 返回成功响应（不包含完整game_data，只返回元信息）
        project_list = [
            {
                "project_id": project['project_id'],
                "title": project['title'],
                "status": project['status'],
                "created_at": project['created_at'],
                "updated_at": project['updated_at']
            }
            for project in projects
        ]
        
        return jsonify({
            "code": 200,
            "msg": "success",
            "requestId": request_id,
            "data": {
                "projects": project_list,
                "total": len(project_list)
            }
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"获取项目列表失败: {str(e)}",
            "requestId": request_id
        }), 500

@projects_bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    """
    获取项目详情接口
    
    响应体:
        {
            "code": 200,
            "msg": "success",
            "requestId": "req_xxx",
            "data": {
                "project_id": "xxx",
                "title": "xxx",
                "game_data": {...},
                "status": "xxx",
                "created_at": "2026-01-24T12:00:00",
                "updated_at": "2026-01-24T12:00:00"
            }
        }
    """
    request_id = generate_request_id()
    
    try:
        # 从请求上下文获取用户ID
        user_id = g.get('user_id')
        
        if not user_id:
            return jsonify({
                "code": 401,
                "msg": "未登录或token无效",
                "requestId": request_id
            }), 401
        
        # 获取项目详情
        project = project_storage.get_project(user_id, project_id)
        
        if not project:
            return jsonify({
                "code": 404,
                "msg": "项目不存在",
                "requestId": request_id
            }), 404
        
        # 返回完整项目数据
        return jsonify({
            "code": 200,
            "msg": "success",
            "requestId": request_id,
            "data": project
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"获取项目详情失败: {str(e)}",
            "requestId": request_id
        }), 500

@projects_bp.route('/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """
    删除项目接口
    
    响应体:
        {
            "code": 200,
            "msg": "删除成功",
            "requestId": "req_xxx"
        }
    """
    request_id = generate_request_id()
    
    try:
        # 从请求上下文获取用户ID
        user_id = g.get('user_id')
        
        if not user_id:
            return jsonify({
                "code": 401,
                "msg": "未登录或token无效",
                "requestId": request_id
            }), 401
        
        # 删除项目
        success = project_storage.delete_project(user_id, project_id)
        
        if not success:
            return jsonify({
                "code": 404,
                "msg": "项目不存在",
                "requestId": request_id
            }), 404
        
        # 返回成功响应
        return jsonify({
            "code": 200,
            "msg": "删除成功",
            "requestId": request_id
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"删除项目失败: {str(e)}",
            "requestId": request_id
        }), 500

@projects_bp.route('/<project_id>/status', methods=['PUT'])
def update_project_status(project_id):
    """
    更新项目状态接口
    
    请求体:
        {
            "status": "draft/editing/published"
        }
    
    响应体:
        {
            "code": 200,
            "msg": "更新成功",
            "requestId": "req_xxx"
        }
    """
    request_id = generate_request_id()
    
    try:
        # 从请求上下文获取用户ID
        user_id = g.get('user_id')
        
        if not user_id:
            return jsonify({
                "code": 401,
                "msg": "未登录或token无效",
                "requestId": request_id
            }), 401
        
        data = request.json
        status = data.get('status')
        
        if not status:
            return jsonify({
                "code": 400,
                "msg": "状态参数不能为空",
                "requestId": request_id
            }), 400
        
        # 更新项目状态
        success = project_storage.update_project_status(user_id, project_id, status)
        
        if not success:
            return jsonify({
                "code": 404,
                "msg": "项目不存在",
                "requestId": request_id
            }), 404
        
        # 返回成功响应
        return jsonify({
            "code": 200,
            "msg": "更新成功",
            "requestId": request_id
        })
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"更新项目状态失败: {str(e)}",
            "requestId": request_id
        }), 500
