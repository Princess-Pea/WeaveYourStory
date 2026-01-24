FROM modelscope-registry.cn-beijing.cr.aliyuncs.com/modelscope-repo/python:3.10

WORKDIR /home/user/app

# 复制所有文件到容器
COPY ./ /home/user/app/

# 安装Python依赖
RUN pip install flask flask-cors pyjwt python-dotenv

# 前端已经构建，直接使用
# 返回到项目根目录
WORKDIR /home/user/app

# 启动应用
ENTRYPOINT ["python", "-u", "modelspace_app.py"]