# 贡献指南

欢迎参与 PixelForge 项目的开发！本文档提供了关于如何贡献代码、报告问题和参与项目开发的指导。

## 项目结构

```
PixelForge/
├── index.html          # 主页面
├── script.js           # JavaScript 逻辑
├── README.md           # 项目介绍
├── CONTRIBUTING.md     # 贡献指南
├── .gitignore          # Git 忽略规则
├── package.json        # 项目配置和依赖
├── modao.config.json   # 魔搭创空间部署配置
└── ...
```

## 开发环境设置

1. 克隆仓库：
   ```bash
   git clone <your-repository-url>
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

## 分支策略

我们使用以下分支策略进行团队协作：

- `main` - 主分支，用于生产环境部署
- `develop` - 开发主分支
- `feature/*` - 功能开发分支
- `bugfix/*` - 修复分支
- `release/*` - 发布准备分支

## 提交规范

请遵循以下提交消息格式：

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

类型包括：
- feat: 新功能
- fix: 修复错误
- docs: 文档更新
- style: 格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

## 代码规范

- 使用 2 个空格作为缩进
- 文件名使用小写字母和短横线分隔
- 提交前确保代码通过验证

## 团队协作流程

1. 从 `develop` 分支创建新的功能分支
2. 在功能分支上完成开发
3. 提交 Pull Request 到 `develop` 分支
4. 团队成员审查代码
5. 合并到 `develop` 分支
6. 定期合并 `develop` 到 `main` 分支进行发布

## 部署到魔搭创空间

项目配置为自动部署到魔搭创空间。当代码推送到 `main` 分支时，会自动触发构建和部署流程。

手动部署步骤：
1. 确保所有更改已提交并推送
2. 检查 `modao.config.json` 配置是否正确
3. 触发部署流程