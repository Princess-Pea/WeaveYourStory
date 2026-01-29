from flask import Blueprint, request, jsonify, g
from flask_cors import CORS
from datetime import datetime
import json
import os
from middleware.auth_middleware import token_required
import secrets
from database.projects_db import (
    projects_db,
    get_project,
    set_project,
    delete_project,
    project_exists,
    get_all_projects,
    get_user_projects
)
from utils.project_storage import ProjectStorage

# 创建项目管理蓝图
projects_bp = Blueprint('projects', __name__)
CORS(projects_bp)

@projects_bp.route('/api/v1/projects', methods=['GET'])
def get_projects():
    """获取用户项目列表"""
    try:
        # 从g对象获取用户信息
        token_data = getattr(g, 'user', {})
        username = token_data.get('user', 'guest') if isinstance(token_data, dict) else 'guest'
        
        # 获取用户的所有项目
        user_projects = []
        for proj_id, project in get_user_projects(username):
            user_projects.append({
                'id': proj_id,
                'title': project['title'],
                'status': project['status'],
                'updated_at': project['updated_at'],
                'created_at': project['created_at']
            })
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'requestId': generate_request_id(),
            'data': {
                'projects': user_projects
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取项目列表失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

@projects_bp.route('/api/v1/projects', methods=['POST'])
def create_project():
    """创建新项目"""
    try:
        # 从g对象获取用户信息
        token_data = getattr(g, 'user', {})
        username = token_data.get('user', 'guest') if isinstance(token_data, dict) else 'guest'
        
        data = request.json
        title = data.get('title', '未命名项目')
        description = data.get('description', '')
        
        if not title:
            return jsonify({
                'code': 400,
                'msg': '项目标题不能为空',
                'requestId': generate_request_id()
            }), 400
        
        # 生成项目ID
        project_id = f"proj_{secrets.token_hex(8)}"
        
        # 创建项目
        project_data = {
            'id': project_id,
            'title': title,
            'description': description,
            'owner': username,
            'status': 'draft',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'manuscript_data': {}
        }
        set_project(project_id, project_data)
        
        return jsonify({
            'code': 200,
            'msg': '项目创建成功',
            'requestId': generate_request_id(),
            'data': {
                'project': {
                    'id': project_id,
                    'title': title,
                    'description': description,
                    'status': 'draft',
                    'created_at': project_data['created_at']
                }
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'创建项目失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

@projects_bp.route('/api/v1/projects/<project_id>', methods=['GET'])
def get_project_by_id(project_id):
    """获取特定项目"""
    try:
        # 从g对象获取用户信息
        token_data = getattr(g, 'user', {})
        username = token_data.get('user', 'guest') if isinstance(token_data, dict) else 'guest'
        
        # 检查项目是否存在且属于当前用户
        project = get_project(project_id)
        if not project or project['owner'] != username:
            return jsonify({
                'code': 404,
                'msg': '项目不存在或无权访问',
                'requestId': generate_request_id()
            }), 404
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'requestId': generate_request_id(),
            'data': {
                'project': {
                    'id': project['id'],
                    'title': project['title'],
                    'description': project['description'],
                    'status': project['status'],
                    'created_at': project['created_at'],
                    'updated_at': project['updated_at'],
                    'manuscript_data': project['manuscript_data']
                }
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取项目失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

@projects_bp.route('/api/v1/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    """更新项目"""
    try:
        # 从g对象获取用户信息
        token_data = getattr(g, 'user', {})
        username = token_data.get('user', 'guest') if isinstance(token_data, dict) else 'guest'
        
        # 检查项目是否存在且属于当前用户
        project = get_project(project_id)
        if not project or project['owner'] != username:
            return jsonify({
                'code': 404,
                'msg': '项目不存在或无权访问',
                'requestId': generate_request_id()
            }), 404
        
        data = request.json
        title = data.get('title')
        description = data.get('description')
        status = data.get('status')
        manuscript_data = data.get('manuscript_data')
        
        # 更新项目信息
        updated_project = project.copy()
        if title is not None:
            updated_project['title'] = title
        if description is not None:
            updated_project['description'] = description
        if status is not None:
            updated_project['status'] = status
        if manuscript_data is not None:
            updated_project['manuscript_data'] = manuscript_data
        
        updated_project['updated_at'] = datetime.now().isoformat()
        
        set_project(project_id, updated_project)
        
        return jsonify({
            'code': 200,
            'msg': '项目更新成功',
            'requestId': generate_request_id(),
            'data': {
                'project': {
                    'id': updated_project['id'],
                    'title': updated_project['title'],
                    'description': updated_project['description'],
                    'status': updated_project['status'],
                    'updated_at': updated_project['updated_at']
                }
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'更新项目失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

@projects_bp.route('/api/v1/projects/<project_id>', methods=['DELETE'])
def delete_project_route(project_id):
    """删除项目"""
    try:
        # 从g对象获取用户信息
        token_data = getattr(g, 'user', {})
        username = token_data.get('user', 'guest') if isinstance(token_data, dict) else 'guest'
        
        # 检查项目是否存在且属于当前用户
        project = get_project(project_id)
        if not project or project['owner'] != username:
            return jsonify({
                'code': 404,
                'msg': '项目不存在或无权访问',
                'requestId': generate_request_id()
            }), 404
        
        delete_project(project_id)
        
        return jsonify({
            'code': 200,
            'msg': '项目删除成功',
            'requestId': generate_request_id()
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'删除项目失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

# ==================== 草稿管理API ====================

# 初始化项目存储实例
project_storage = ProjectStorage()

@projects_bp.route('/api/v1/projects/drafts', methods=['POST'])
def save_draft():
    """保存草稿（新建或更新）"""
    try:
        # 从g对象获取用户信息
        token_data = getattr(g, 'user', {})
        username = token_data.get('user', 'guest') if isinstance(token_data, dict) else 'guest'
        
        data = request.json
        draft_id = data.get('draft_id')
        title = data.get('title', '未命名草稿')
        manuscript = data.get('manuscript', {})
        
        # 保存草稿
        draft = project_storage.save_draft(
            user_id=username,
            draft_id=draft_id,
            title=title,
            manuscript=manuscript
        )
        
        if not draft:
            return jsonify({
                'code': 500,
                'msg': '保存草稿失败',
                'requestId': generate_request_id()
            }), 500
        
        return jsonify({
            'code': 200,
            'msg': '草稿保存成功',
            'requestId': generate_request_id(),
            'data': {
                'draft': draft
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'保存草稿失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500


@projects_bp.route('/api/v1/projects/drafts', methods=['GET'])
def get_drafts_list():
    """获取草稿列表"""
    try:
        # 从g对象获取用户信息
        token_data = getattr(g, 'user', {})
        username = token_data.get('user', 'guest') if isinstance(token_data, dict) else 'guest'
        
        # 获取草稿列表
        drafts = project_storage.list_drafts(user_id=username)
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'requestId': generate_request_id(),
            'data': {
                'drafts': drafts
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取草稿列表失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500


@projects_bp.route('/api/v1/projects/drafts/<draft_id>', methods=['GET'])
def get_draft_by_id(draft_id):
    """获取草稿详情"""
    try:
        # 从g对象获取用户信息
        token_data = getattr(g, 'user', {})
        username = token_data.get('user', 'guest') if isinstance(token_data, dict) else 'guest'
        
        # 获取草稿详情
        draft = project_storage.get_draft(user_id=username, draft_id=draft_id)
        
        if not draft:
            return jsonify({
                'code': 404,
                'msg': '草稿不存在',
                'requestId': generate_request_id()
            }), 404
        
        return jsonify({
            'code': 200,
            'msg': 'success',
            'requestId': generate_request_id(),
            'data': {
                'draft': draft
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取草稿详情失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500


@projects_bp.route('/api/v1/projects/drafts/<draft_id>', methods=['DELETE'])
def delete_draft_by_id(draft_id):
    """删除草稿"""
    try:
        # 从g对象获取用户信息
        token_data = getattr(g, 'user', {})
        username = token_data.get('user', 'guest') if isinstance(token_data, dict) else 'guest'
        
        # 删除草稿
        success = project_storage.delete_draft(user_id=username, draft_id=draft_id)
        
        if not success:
            return jsonify({
                'code': 404,
                'msg': '草稿不存在或删除失败',
                'requestId': generate_request_id()
            }), 404
        
        return jsonify({
            'code': 200,
            'msg': '草稿删除成功',
            'requestId': generate_request_id()
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'删除草稿失败: {str(e)}',
            'requestId': generate_request_id()
        }), 500

def generate_request_id():
    """生成请求ID"""
    return secrets.token_hex(8)