"""
魔搭创空间部署入口文件
此文件用于适配魔搭创空间的部署要求
"""
import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# 创建Flask应用
app = Flask(__name__, static_folder='frontend/dist')

# 配置CORS，允许前端的所有请求
CORS(app, 
     origins="*",
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

# 手动注册API蓝图（避免与backend.app的潜在冲突）
try:
    from backend.api.auth import auth_bp
    from backend.api.projects import projects_bp
    from backend.config.settings import Config
    from backend.middleware.auth_middleware import init_auth_middleware
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(projects_bp, url_prefix='')
    
    # 初始化认证中间件
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
        return send_from_directory('frontend/dist', 'index.html')
    except FileNotFoundError:
        # 如果前端文件不存在，返回一个简单的页面提示
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>PixelForge - 像素风情感叙事冒险游戏设计平台</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .container { max-width: 600px; margin: 0 auto; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎮 像素风情感叙事冒险游戏设计平台</h1>
                <p>后端服务正常运行中...</p>
                <p>正在等待前端构建完成...</p>
                <p><a href="/api/v1/health">检查API状态</a></p>
            </div>
        </body>
        </html>
        '''

@app.route('/<path:path>')
def serve_static(path):
    # 尝试提供前端静态文件
    try:
        # 检查文件是否存在
        file_path = os.path.join(os.getcwd(), 'frontend', 'dist', path)
        if os.path.exists(file_path):
            return send_from_directory('frontend/dist', path)
        else:
            # 如果文件不存在，返回index.html以支持前端路由
            return send_from_directory('frontend/dist', 'index.html')
    except:
        # 如果发生异常，返回index.html
        try:
            return send_from_directory('frontend/dist', 'index.html')
        except:
            # 如果前端文件不存在，返回简单页面
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>PixelForge - 像素风情感叙事冒险游戏设计平台</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                    .container { max-width: 600px; margin: 0 auto; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎮 像素风情感叙事冒险游戏设计平台</h1>
                    <p>后端服务正常运行中...</p>
                    <p>正在等待前端构建完成...</p>
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