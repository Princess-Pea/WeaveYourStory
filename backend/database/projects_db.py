"""
项目数据库模块
用于在多个蓝图之间共享项目数据
"""

# 模拟项目数据库 - 使用字典作为内存存储
projects_db = {}


def get_project(project_id):
    """获取项目信息"""
    return projects_db.get(project_id)


def set_project(project_id, project_data):
    """设置项目信息"""
    projects_db[project_id] = project_data


def delete_project(project_id):
    """删除项目"""
    if project_id in projects_db:
        del projects_db[project_id]


def project_exists(project_id):
    """检查项目是否存在"""
    return project_id in projects_db


def get_all_projects():
    """获取所有项目"""
    return projects_db.copy()


def get_user_projects(username):
    """获取特定用户的所有项目"""
    user_projects = []
    for proj_id, project in projects_db.items():
        if project.get('owner') == username:
            user_projects.append((proj_id, project))
    return user_projects