"""
魔搭创空间部署入口文件
此文件用于适配魔搭创空间的部署要求
"""
import os
import sys
from flask import Flask, send_from_directory
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
@app.route('/')
def serve_index():
    return send_from_directory('frontend/dist', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.startswith('api/'):
        # API请求，让后端处理
        return backend_app.full_dispatch_request()
    else:
        # 静态文件请求，从前端dist目录提供
        try:
            return send_from_directory('frontend/dist', path)
        except FileNotFoundError:
            return send_from_directory('frontend/dist', 'index.html')

if __name__ == '__main__':
    # 为魔搭创空间设置适当的主机和端口
    port = int(os.environ.get('PORT', 7860))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"启动 PixelForge 应用，监听 {host}:{port}")
    app.run(host=host, port=port, debug=False)