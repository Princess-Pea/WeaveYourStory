<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>🎮 像素风情感叙事冒险游戏设计平台</h1>
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