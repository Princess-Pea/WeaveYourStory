<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
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
  background-color: #020817; /* 与背景同色，使其隐形 */
  color: #fff;
  display: flex;
  align-items: center;
  border-bottom: none; /* 移除底部边框 */
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