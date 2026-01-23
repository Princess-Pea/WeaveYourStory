"""
魔搭创空间部署入口文件
此文件用于适配魔搭创空间的部署要求
"""
import os
import sys
from flask import Flask, send_from_directory, request
from flask_cors import CORS
import threading
import subprocess
import time

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# 从backend导入Flask应用
try:
    from backend.app import app as backend_app
except ImportError:
    print("警告: 无法导入backend.app，使用默认Flask应用")
    from flask import Flask
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/')
    def home():
        return "PixelForge 应用正在运行"
    
    @app.route('/health')
    def health():
        return {"status": "healthy", "service": "PixelForge"}
else:
    # 使用backend中的Flask应用
    app = backend_app

# 配置静态文件服务，用于前端
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    # 如果是API请求，交给后端处理
    if path.startswith('api/') or '/api/' in path or path.startswith('health') or path.startswith('token') or path.startswith('game') or path.startswith('ai'):
        # 为API请求，使用当前应用处理
        return app.handle_request(request)
    else:
        # 非API请求，尝试返回前端静态文件
        try:
            # 如果请求的是根路径或前端路由，返回index.html
            if path == '' or path == '/' or not '.' in path.split('/')[-1]:
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
                        </div>
                    </body>
                    </html>
                    '''
            # 如果请求的是静态资源文件，返回对应文件
            else:
                return send_from_directory('frontend/dist', path)
        except Exception as e:
            # 如果文件不存在，返回index.html以支持前端路由
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