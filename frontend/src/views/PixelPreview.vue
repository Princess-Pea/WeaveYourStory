<template>
  <div class="empty-preview-container">
    <div class="empty-content">
      <h2>🎮 项目预览</h2>
      <p>此功能正在开发中，敬请期待...</p>
    </div>
  </div>
</template>

<script setup>
// 此页面为预留的空界面，等待其他成员开发
</script>

<style scoped>
.empty-preview-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #020817; /* 新的深蓝灰色背景 */
  color: white;
}

.empty-content {
  text-align: center;
}

.empty-content h2 {
  margin-bottom: 20px;
  color: #E9A33B; /* 高亮色 */
}

.empty-content p {
  font-size: 16px;
  color: #ccc;
}
</style>