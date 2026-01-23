FROM modelscope-registry.cn-beijing.cr.aliyuncs.com/modelscope-repo/python:3.10

WORKDIR /home/user/app

# 复制所有文件到容器
COPY ./ /home/user/app/

# 安装后端依赖
RUN pip install flask flask-cors pyjwt python-dotenv

# 安装前端依赖并构建
WORKDIR /home/user/app/frontend
RUN npm install

WORKDIR /home/user/app

# 启动后端服务
ENTRYPOINT ["python", "-u", "backend/app.py"]