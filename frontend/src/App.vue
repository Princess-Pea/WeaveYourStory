<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1 class="app-title">PixelForge</h1>
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
  background-color: #020817; /* 新的深蓝灰色背景 */
}

.el-header {
  background-color: #383F59; /* 功能块色 */
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

.app-title {
  font-family: 'Times New Roman', Times, serif; /* 使用Times New Roman字体 */
  font-size: 1.5rem;
  margin: 0;
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
  transition: all 0.3s;
  border: 2px solid transparent; /* 初始透明边框，为悬停效果预留空间 */
}

.navigation a.router-link-exact-active,
.navigation a:hover {
  background-color: #383F59; /* 功能块色 */
  text-decoration: underline;
  border: 2px solid #E9A33B; /* 悬停高亮色 */
  box-shadow: 0 0 10px #E9A33B; /* 氛围荧光效果 */
}

.el-footer {
  background-color: #383F59; /* 功能块色 */
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
  background: #020817;
}

::-webkit-scrollbar-thumb {
  background: #383F59;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #E9A33B;
}
</style>