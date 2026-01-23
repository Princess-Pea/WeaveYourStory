"""
魔搭创空间部署入口文件
此文件用于适配魔搭创空间的部署要求
"""
import os
import sys
from flask import Flask, send_from_directory, request
from flask_cors import CORS

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# 从backend导入Flask应用
try:
    from backend.app import app
except ImportError:
    print("警告: 无法导入backend.app，使用默认Flask应用")
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/')
    def home():
        return "PixelForge 应用正在运行"
    
    @app.route('/health')
    def health():
        return {"status": "healthy", "service": "PixelForge"}

# 配置静态文件服务，用于前端
# 为所有非API路径提供前端服务
@app.route('/')
def serve_index():
    # 检查前端构建文件是否存在
    frontend_dist = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')
    index_path = os.path.join(frontend_dist, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory('frontend/dist', 'index.html')
    else:
        # 如果前端构建文件不存在，返回一个简单的HTML页面提示
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

# 为所有非API路径提供前端服务
@app.route('/<path:path>')
def serve_static(path):
    # 检查路径是否为API相关路径
    api_paths = ['api/', 'health', 'token', 'game', 'ai', 'user', 'auth', 'upload', 'download']
    is_api_path = any(path.startswith(api_path) for api_path in api_paths)
    
    if is_api_path:
        # 如果是API路径，让Flask继续处理（会返回404如果路由不存在）
        # 实际上，后端app已经有这些路由，所以会正常处理
        pass
        
    # 检查文件是否存在
    frontend_dist = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')
    file_path = os.path.join(frontend_dist, path)
    
    # 如果是API路径或文件不存在，返回index.html以支持前端路由
    if is_api_path or not os.path.exists(file_path):
        # 检查前端构建文件是否存在
        index_path = os.path.join(frontend_dist, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory('frontend/dist', 'index.html')
        else:
            # 如果前端构建文件不存在，返回一个简单的HTML页面提示
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
    else:
        # 如果文件存在，返回该文件
        directory = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')
        return send_from_directory(directory, path)

if __name__ == '__main__':
    # 为魔搭创空间设置适当的主机和端口
    port = int(os.environ.get('PORT', 7860))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"启动 PixelForge 应用，监听 {host}:{port}")
    app.run(host=host, port=port, debug=False)