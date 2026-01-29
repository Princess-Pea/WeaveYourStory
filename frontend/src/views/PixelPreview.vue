<template>
  <div class="preview-container">
    <div class="preview-header">
      <h2>🎮 项目预览</h2>
      <p>在此预览已生成的游戏内容</p>
    </div>
    
    <div class="preview-content">
      <!-- 游戏预览组件 -->
      <div class="game-preview-wrapper">
        <GamePreview />
      </div>
    </div>
  </div>
</template>

<script setup>
import GamePreview from './GamePreview.vue'
</script>

<style scoped>
.preview-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #020817;
  color: white;
  overflow: hidden;
}

.preview-header {
  padding: 20px;
  text-align: center;
  background-color: rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid #E9A33B;
}

.preview-header h2 {
  margin: 0 0 10px 0;
  color: #E9A33B;
}

.preview-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.game-preview-wrapper {
  width: 100%;
  height: 100%;
}
</style>
