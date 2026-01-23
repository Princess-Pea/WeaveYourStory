"""
魔搭创空间部署入口文件
此文件用于适配魔搭创空间的部署要求
"""
import os
import sys
from flask import Flask, send_from_directory, request, redirect, url_for
from flask_cors import CORS

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 从backend导入所有路由
try:
    from backend.app import app as backend_app
    # 将backend的路由规则复制到当前app
    import backend.app
    # 遍历backend应用的所有路由并添加到当前app
    for rule in backend_app.url_map.iter_rules():
        func = backend_app.view_functions[rule.endpoint]
        app.add_url_rule(rule.rule, endpoint=rule.endpoint, view_func=func, methods=rule.methods)
except ImportError as e:
    print(f"警告: 无法导入backend.app: {e}")
    # 定义一些基本的API路由以防导入失败
    @app.route('/api/v1/health')
    def health():
        return {"status": "healthy", "service": "PixelForge"}

# 提供前端静态文件服务
@app.route('/')
def serve_index():
    try:
        return send_from_directory('frontend/dist', 'index.html')
    except:
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
    # 检查是否为API请求
    if path.startswith('api/'):
        # 如果是API路径，应该由上面导入的路由处理
        # 如果没有匹配的路由，Flask会自动返回404
        pass
    
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