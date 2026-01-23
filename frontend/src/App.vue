<template>
  <div id="app">
    <el-container>
      <el-header>
        <h1>🎮 像素风情感叙事冒险游戏设计平台</h1>
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
}

.el-header {
  background-color: #409EFF;
  color: #fff;
  display: flex;
  align-items: center;
}

.el-header h1 {
  margin: 0;
}

.el-footer {
  background-color: #f5f5f5;
  text-align: center;
  line-height: 60px;
}
</style>