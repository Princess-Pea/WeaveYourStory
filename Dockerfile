FROM modelscope-registry.cn-beijing.cr.aliyuncs.com/modelscope-repo/python:3.10

WORKDIR /home/user/app

# 复制所有文件到容器
COPY ./ /home/user/app/

# 安装Python依赖
RUN pip install flask flask-cors pyjwt python-dotenv

# 前端已经构建，直接使用
# 如果前端尚未构建，则构建前端（可选）
WORKDIR /home/user/app/frontend
RUN if [ ! -d "dist" ]; then npm install && npx vite build; fi

# 返回到项目根目录
WORKDIR /home/user/app

# 启动应用
ENTRYPOINT ["python", "-u", "modelspace_app.py"]