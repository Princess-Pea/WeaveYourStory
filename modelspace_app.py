"""
魔搭创空间部署入口文件
此文件用于适配魔搭创空间的部署要求
"""
import os
import sys
import importlib.util
from flask import Flask, send_from_directory, abort
from werkzeug.exceptions import NotFound
from flask_cors import CORS

# 动态添加backend目录到Python路径
project_root = os.path.dirname(__file__)  # 当前文件的目录
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)

# 尝试添加项目根目录到路径（有时需要这个）
sys.path.insert(0, project_root)

# 创建Flask应用
app = Flask(__name__, static_folder='frontend/dist')

# 配置CORS，允许前端的所有请求
CORS(app, 
     origins="*",
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

# 手动注册API蓝图（避免与backend.app的潜在冲突）
try:
    # 尝试多种方法导入后端模块
    import importlib.util
    
    # 首先尝试常规导入
    try:
        from backend.api.auth import auth_bp
        from backend.api.projects import projects_bp
    except ImportError:
        # 如果常规导入失败，尝试动态导入
        auth_module_path = os.path.join(backend_path, 'api', 'auth.py')
        if os.path.exists(auth_module_path):
            spec = importlib.util.spec_from_file_location("auth", auth_module_path)
            auth_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(auth_module)
            auth_bp = auth_module.auth_bp
            
            projects_module_path = os.path.join(backend_path, 'api', 'projects.py')
            spec = importlib.util.spec_from_file_location("projects", projects_module_path)
            projects_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(projects_module)
            projects_bp = projects_module.projects_bp
        else:
            raise ImportError("无法找到后端API模块")
    
    # 尝试导入配置，如果失败则使用默认值
    try:
        from backend.config.settings import Config
    except ImportError:
        # 如果导入失败，尝试动态导入
        config_path = os.path.join(backend_path, 'config', 'settings.py')
        if os.path.exists(config_path):
            spec = importlib.util.spec_from_file_location("settings", config_path)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            Config = config_module.Config
        else:
            # 如果动态导入也失败，创建一个基本的配置对象
            class Config:
                JWT_SECRET = os.environ.get('JWT_SECRET', 'pixelforge_default_secret_key_change_in_production')
                DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
                USERS_DIR = os.path.join(DATA_DIR, 'users')
                USERS_FILE = os.path.join(USERS_DIR, 'users.json')
                PROJECTS_DIR = os.path.join(DATA_DIR, 'projects')
                DRAFTS_DIR = os.path.join(DATA_DIR, 'drafts')
                
                @classmethod
                def init_directories(cls):
                    os.makedirs(cls.DATA_DIR, exist_ok=True)
                    os.makedirs(cls.USERS_DIR, exist_ok=True)
                    if not os.path.exists(cls.USERS_FILE):
                        import json
                        with open(cls.USERS_FILE, 'w', encoding='utf-8') as f:
                            json.dump({}, f, ensure_ascii=False, indent=2)
    
    # 尝试导入认证中间件，如果失败则跳过
    try:
        from backend.middleware.auth_middleware import init_auth_middleware
        middleware_available = True
    except ImportError:
        # 尝试动态导入中间件
        try:
            middleware_path = os.path.join(backend_path, 'middleware', 'auth_middleware.py')
            if os.path.exists(middleware_path):
                spec = importlib.util.spec_from_file_location("auth_middleware", middleware_path)
                middleware_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(middleware_module)
                init_auth_middleware = middleware_module.init_auth_middleware
                middleware_available = True
            else:
                print("认证中间件文件不存在，将跳过中间件初始化")
                middleware_available = False
        except Exception as e:
            print(f"认证中间件导入失败: {e}，将跳过中间件初始化")
            middleware_available = False
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(projects_bp, url_prefix='')
    
    # 初始化认证中间件（如果可用）
    if middleware_available:
        init_auth_middleware(app)
    
    # 初始化数据目录
    Config.init_directories()
    
    print("成功注册API模块")
except ImportError as e:
    print(f"API模块导入失败: {e}")
    # 如果导入失败，至少定义一个健康检查端点
    @app.route('/api/v1/health')
    def health():
        return {"status": "error", "service": "PixelForge", "msg": str(e)}

# 提供前端静态文件服务
@app.route('/')
def serve_index():
    try:
        # 使用绝对路径确保能找到文件
        frontend_dist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'dist')
        if os.path.exists(frontend_dist_path):
            return send_from_directory(frontend_dist_path, 'index.html')
        else:
            # 如果前端构建目录不存在，返回错误提示
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>PixelForge - 部署错误</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                    .container { max-width: 600px; margin: 0 auto; }
                    .error { color: red; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎮 像素风情感叙事冒险游戏设计平台</h1>
                    <p class="error">错误：前端构建文件不存在</p>
                    <p>请确保 frontend/dist 目录存在并包含构建文件</p>
                    <p>后端服务正常运行中...</p>
                    <p><a href="/api/v1/health">检查API状态</a></p>
                </div>
            </body>
            </html>
            '''
    except FileNotFoundError:
        # 如果前端文件不存在，返回一个简单的页面提示
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>PixelForge - 部署错误</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .container { max-width: 600px; margin: 0 auto; }
                .error { color: red; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎮 像素风情感叙事冒险游戏设计平台</h1>
                <p class="error">错误：前端构建文件不存在</p>
                <p>请确保 frontend/dist 目录存在并包含构建文件</p>
                <p>后端服务正常运行中...</p>
                <p><a href="/api/v1/health">检查API状态</a></p>
            </div>
        </body>
        </html>
        '''

@app.route('/<path:path>')
def serve_static(path):
    # 首先排除API路径，确保API路由优先
    if path.startswith('api/'):
        # 如果是API请求，抛出404异常，让Flask继续寻找其他路由
        from werkzeug.exceptions import NotFound
        raise NotFound()
    
    # 尝试提供前端静态文件
    try:
        # 使用绝对路径确保能找到文件
        frontend_dist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'dist')
        if os.path.exists(frontend_dist_path):
            # 检查文件是否存在
            file_path = os.path.join(frontend_dist_path, path)
            if os.path.exists(file_path):
                return send_from_directory(frontend_dist_path, path)
            else:
                # 如果文件不存在，返回index.html以支持前端路由
                return send_from_directory(frontend_dist_path, 'index.html')
        else:
            # 如果前端构建目录不存在，返回错误提示
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>PixelForge - 部署错误</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                    .container { max-width: 600px; margin: 0 auto; }
                    .error { color: red; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎮 像素风情感叙事冒险游戏设计平台</h1>
                    <p class="error">错误：前端构建文件不存在</p>
                    <p>请确保 frontend/dist 目录存在并包含构建文件</p>
                    <p>后端服务正常运行中...</p>
                    <p><a href="/api/v1/health">检查API状态</a></p>
                </div>
            </body>
            </html>
            '''
    except Exception as e:
        # 如果发生异常，返回index.html
        frontend_dist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'dist')
        if os.path.exists(frontend_dist_path):
            try:
                return send_from_directory(frontend_dist_path, 'index.html')
            except:
                pass  # 如果发送index.html也失败，继续执行后面的错误页面
        # 如果前端文件不存在，返回简单页面
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>PixelForge - 部署错误</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .container { max-width: 600px; margin: 0 auto; }
                .error { color: red; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎮 像素风情感叙事冒险游戏设计平台</h1>
                <p class="error">错误：前端构建文件不存在</p>
                <p>请确保 frontend/dist 目录存在并包含构建文件</p>
                <p>后端服务正常运行中...</p>
                <p><a href="/api/v1/health">检查API状态</a></p>
            </div>
        </body>
        </html>
        '''

if __name__ == '__main__':
    # 为魔搭创空间设置适当的主机和端口
    port = int(os.environ.get('PORT', 7860))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"启动 PixelForge 应用，监听 {host}:{port}")
    app.run(host=host, port=port, debug=False)