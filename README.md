# PixelForge

这是一个用于Web应用开发的项目，将部署到魔搭创空间，支持团队协作开发。

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

项目包含基础的前端模板，包含 HTML、CSS 和 JavaScript 文件，可根据需要扩展功能。

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