FROM modelscope-registry.cn-beijing.cr.aliyuncs.com/modelscope-repo/python:3.10

WORKDIR /home/user/app

# 复制所有文件到容器
COPY ./ /home/user/app/

# 安装Python依赖
RUN pip install flask flask-cors pyjwt python-dotenv

# 安装Node.js依赖
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs

# 构建前端
WORKDIR /home/user/app/frontend
RUN npm install
RUN npx vite build

# 返回到项目根目录
WORKDIR /home/user/app

# 启动应用
ENTRYPOINT ["python", "-u", "modelscope_app.py"]