"""
项目数据存储工具类
【魔搭适配点】使用JSON文件存储项目和草稿数据，按用户ID分层
【TODO】后续需要迁移到MySQL/MongoDB等数据库
"""
import json
import os
import uuid
import datetime
from config.settings import Config
import threading

class ProjectStorage:
    """
    项目数据存储类
    支持草稿和正式项目的存储管理
    当前使用JSON文件存储，预留数据库迁移接口
    """
    
    def __init__(self):
        """初始化存储类，确保数据目录存在"""
        self.projects_dir = Config.PROJECTS_DIR
        self.drafts_dir = Config.DRAFTS_DIR
        self._lock = threading.Lock()  # 并发访问控制
        
        # 确保目录存在
        os.makedirs(self.projects_dir, exist_ok=True)
        os.makedirs(self.drafts_dir, exist_ok=True)
    
    def _get_user_dir(self, user_id, is_draft=False):
        """
        获取用户专属数据目录
        【魔搭适配点】按用户ID分层存储，确保数据隔离
        
        参数:
            user_id (str): 用户ID
            is_draft (bool): 是否为草稿目录
            
        返回:
            str: 用户数据目录路径
        """
        base_dir = self.drafts_dir if is_draft else self.projects_dir
        user_dir = os.path.join(base_dir, user_id)
        os.makedirs(user_dir, exist_ok=True)
        return user_dir
    
    def _read_project_file(self, file_path):
        """
        读取项目文件
        
        参数:
            file_path (str): 文件路径
            
        返回:
            dict: 项目数据，不存在返回None
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            with self._lock:  # 并发控制
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"读取项目文件失败: {file_path}, 错误: {str(e)}")
            return None
    
    def _write_project_file(self, file_path, data):
        """
        写入项目文件
        
        参数:
            file_path (str): 文件路径
            data (dict): 项目数据
        """
        with self._lock:  # 并发控制
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ==================== 草稿管理 ====================
    
    def save_draft(self, user_id, draft_id=None, title="", manuscript=None):
        """
        保存草稿（新建或更新）
        【TODO】数据库迁移时，改为INSERT或UPDATE语句
        
        参数:
            user_id (str): 用户ID
            draft_id (str): 草稿ID（None表示新建）
            title (str): 草稿标题
            manuscript (dict): 原稿数据
            
        返回:
            dict: 草稿信息，失败返回None
        """
        user_dir = self._get_user_dir(user_id, is_draft=True)
        
        # 如果是新建草稿，生成ID
        if not draft_id:
            draft_id = f"draft_{uuid.uuid4().hex[:16]}"
        
        # 构造草稿对象
        draft = {
            'draft_id': draft_id,
            'user_id': user_id,
            'title': title or '未命名草稿',
            'manuscript': manuscript or {},
            'status': 'draft',
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        
        # 如果是更新已有草稿，保留创建时间
        file_path = os.path.join(user_dir, f"{draft_id}.json")
        if os.path.exists(file_path):
            old_draft = self._read_project_file(file_path)
            if old_draft:
                draft['created_at'] = old_draft.get('created_at', draft['created_at'])
        
        # 写入文件
        self._write_project_file(file_path, draft)
        
        return draft
    
    def get_draft(self, user_id, draft_id):
        """
        获取草稿详情
        【TODO】数据库迁移时，改为SELECT语句
        
        参数:
            user_id (str): 用户ID
            draft_id (str): 草稿ID
            
        返回:
            dict: 草稿信息，不存在返回None
        """
        user_dir = self._get_user_dir(user_id, is_draft=True)
        file_path = os.path.join(user_dir, f"{draft_id}.json")
        return self._read_project_file(file_path)
    
    def list_drafts(self, user_id):
        """
        获取用户的草稿列表
        【TODO】数据库迁移时，改为SELECT语句
        
        参数:
            user_id (str): 用户ID
            
        返回:
            list: 草稿列表
        """
        user_dir = self._get_user_dir(user_id, is_draft=True)
        drafts = []
        
        try:
            for filename in os.listdir(user_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(user_dir, filename)
                    draft = self._read_project_file(file_path)
                    if draft:
                        drafts.append(draft)
        except Exception as e:
            print(f"读取草稿列表失败: {str(e)}")
        
        # 按更新时间倒序排序
        drafts.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        return drafts
    
    def delete_draft(self, user_id, draft_id):
        """
        删除草稿
        【TODO】数据库迁移时，改为DELETE语句
        
        参数:
            user_id (str): 用户ID
            draft_id (str): 草稿ID
            
        返回:
            bool: 删除成功返回True，否则返回False
        """
        user_dir = self._get_user_dir(user_id, is_draft=True)
        file_path = os.path.join(user_dir, f"{draft_id}.json")
        
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"删除草稿失败: {str(e)}")
            return False
    
    # ==================== 项目管理 ====================
    
    def save_project(self, user_id, project_id=None, title="", game_data=None, status="draft"):
        """
        保存项目（新建或更新）
        【TODO】数据库迁移时，改为INSERT或UPDATE语句
        
        参数:
            user_id (str): 用户ID
            project_id (str): 项目ID（None表示新建）
            title (str): 项目标题
            game_data (dict): 游戏数据
            status (str): 项目状态（draft/editing/published）
            
        返回:
            dict: 项目信息，失败返回None
        """
        user_dir = self._get_user_dir(user_id, is_draft=False)
        
        # 如果是新建项目，生成ID
        if not project_id:
            project_id = f"proj_{uuid.uuid4().hex[:16]}"
        
        # 构造项目对象
        project = {
            'project_id': project_id,
            'user_id': user_id,
            'title': title or '未命名项目',
            'game_data': game_data or {},
            'status': status,
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        
        # 如果是更新已有项目，保留创建时间
        file_path = os.path.join(user_dir, f"{project_id}.json")
        if os.path.exists(file_path):
            old_project = self._read_project_file(file_path)
            if old_project:
                project['created_at'] = old_project.get('created_at', project['created_at'])
        
        # 写入文件
        self._write_project_file(file_path, project)
        
        return project
    
    def get_project(self, user_id, project_id):
        """
        获取项目详情
        【TODO】数据库迁移时，改为SELECT语句
        
        参数:
            user_id (str): 用户ID
            project_id (str): 项目ID
            
        返回:
            dict: 项目信息，不存在返回None
        """
        user_dir = self._get_user_dir(user_id, is_draft=False)
        file_path = os.path.join(user_dir, f"{project_id}.json")
        return self._read_project_file(file_path)
    
    def list_projects(self, user_id, status=None):
        """
        获取用户的项目列表
        【TODO】数据库迁移时，改为SELECT语句
        
        参数:
            user_id (str): 用户ID
            status (str): 状态过滤（None表示全部）
            
        返回:
            list: 项目列表
        """
        user_dir = self._get_user_dir(user_id, is_draft=False)
        projects = []
        
        try:
            for filename in os.listdir(user_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(user_dir, filename)
                    project = self._read_project_file(file_path)
                    if project:
                        # 状态过滤
                        if status is None or project.get('status') == status:
                            projects.append(project)
        except Exception as e:
            print(f"读取项目列表失败: {str(e)}")
        
        # 按更新时间倒序排序
        projects.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        return projects
    
    def delete_project(self, user_id, project_id):
        """
        删除项目
        【TODO】数据库迁移时，改为DELETE语句
        
        参数:
            user_id (str): 用户ID
            project_id (str): 项目ID
            
        返回:
            bool: 删除成功返回True，否则返回False
        """
        user_dir = self._get_user_dir(user_id, is_draft=False)
        file_path = os.path.join(user_dir, f"{project_id}.json")
        
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"删除项目失败: {str(e)}")
            return False
    
    def update_project_status(self, user_id, project_id, status):
        """
        更新项目状态
        
        参数:
            user_id (str): 用户ID
            project_id (str): 项目ID
            status (str): 新状态
            
        返回:
            bool: 更新成功返回True，否则返回False
        """
        project = self.get_project(user_id, project_id)
        if not project:
            return False
        
        project['status'] = status
        project['updated_at'] = datetime.datetime.now().isoformat()
        
        user_dir = self._get_user_dir(user_id, is_draft=False)
        file_path = os.path.join(user_dir, f"{project_id}.json")
        self._write_project_file(file_path, project)
        
        return True
