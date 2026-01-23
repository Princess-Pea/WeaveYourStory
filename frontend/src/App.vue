<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>🎮 像素风情感叙事冒险游戏设计平台</h1>
          <nav class="navigation">
            <router-link to="/">首页</router-link>
            <router-link to="/manuscript-input">原稿输入</router-link>
            <router-link to="/visual-editor">可视化编辑</router-link>
            <router-link to="/pixel-preview">像素风预览</router-link>
            <router-link to="/profile">个人中心</router-link>
          </nav>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        <p>Powered by PixelForge - 设计属于你的像素冒险世界</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  background-color: #2c3a47; /* 深蓝灰色背景 */
}

.el-header {
  background-color: #34495e; /* 深蓝灰标题栏 */
  color: #fff;
  display: flex;
  align-items: center;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.navigation {
  display: flex;
  gap: 20px;
}

.navigation a {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.navigation a.router-link-exact-active,
.navigation a:hover {
  background-color: #4a6278; /* 深蓝灰悬停背景 */
  text-decoration: underline;
}

.el-footer {
  background-color: #34495e; /* 深蓝灰页脚 */
  color: #fff;
  text-align: center;
  line-height: 60px;
}

/* 全局滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #2c3a47;
}

::-webkit-scrollbar-thumb {
  background: #34495e;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #4a6278;
}
</style>