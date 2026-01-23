---
# 详细文档见https://modelscope.cn/docs/%E5%88%9B%E7%A9%BA%E9%97%B4%E5%8D%A1%E7%89%87
domain: #领域：cv/nlp/audio/multi-modal/AutoML
# - cv
tags: #自定义标签
-
datasets: #关联数据集
  evaluation:
  #- iic/ICDAR13_HCTR_Dataset
  test:
  #- iic/MTWI
  train:
  #- iic/SIBR
models: #关联模型
#- iic/ofa_ocr-recognition_general_base_zh

## 启动文件(若SDK为Gradio/Streamlit，默认为app.py, 若为Static HTML, 默认为index.html)
# deployspec:
#   entry_file: app.py
license: Apache License 2.0
---
#### Clone with HTTP
```bash
 git clone https://www.modelscope.cn/studios/Legency/Weave_Your_Story.git
```
>>>>>>> 7afb7c5428ee7dbc0b95dc2917c13fbeb0c5deaf
# PixelForge

这是一个「像素风情感叙事冒险游戏设计平台」项目，将部署到魔搭创空间，支持团队协作开发。

## 项目设置

### 创建远程仓库

1. 在 GitHub/GitLab/码云 等平台创建一个新的仓库
2. 将本地仓库连接到远程仓库：

```bash
git remote add origin <your-remote-repository-url>
git branch -M main
git push -u origin main
```

### 团队协作

1. 团队成员克隆仓库：

```bash
git clone <your-remote-repository-url>
cd pixelforge
```

2. 安装依赖：

```bash
npm install
```

3. 启动开发服务器：

```bash
npm run dev
```

详细协作流程请参考 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 开发

项目包含完整的前后端分离架构，前端使用 Vue3 + Vite + Element Plus，后端使用 Python + Flask，支持AI辅助功能。

## 部署到魔搭创空间

项目已配置支持部署到魔搭创空间，包含所需的 `app.py` 和 `Dockerfile` 文件。

### 部署步骤

1. 克隆项目空间：
   ```bash
   git lfs install
   git clone http://oauth2:YOUR_TOKEN@www.modelscope.cn/studios/YOUR_USERNAME/YOUR_STUDIO_NAME.git
   ```

2. 复制项目文件到克隆的仓库

3. 提交文件：
   ```bash
   git add app.py Dockerfile
   git commit -m "Add application and Dockerfile"
   git push
   ```

项目将会自动构建并部署到魔搭创空间。
=======
---
# 详细文档见https://modelscope.cn/docs/%E5%88%9B%E7%A9%BA%E9%97%B4%E5%8D%A1%E7%89%87
domain: #领域：cv/nlp/audio/multi-modal/AutoML
# - cv
tags: #自定义标签
-
datasets: #关联数据集
  evaluation:
  #- iic/ICDAR13_HCTR_Dataset
  test:
  #- iic/MTWI
  train:
  #- iic/SIBR
models: #关联模型
#- iic/ofa_ocr-recognition_general_base_zh

## 启动文件(若SDK为Gradio/Streamlit，默认为app.py, 若为Static HTML, 默认为index.html)
# deployspec:
#   entry_file: app.py
license: Apache License 2.0
---
#### Clone with HTTP
```bash
 git clone https://www.modelscope.cn/studios/Legency/Weave_Your_Story.git
```
>>>>>>> 7afb7c5428ee7dbc0b95dc2917c13fbeb0c5deaf
