<template>
  <div class="home-container">
    <div class="header-section">
      <div class="logo-section">
        <h1 class="pixel-logo">PixelForge</h1>
        <h2 class="subheading">像素风情感叙事冒险游戏设计平台</h2>
        <p class="subtitle">将你的故事打造成可游玩的像素风情感叙事冒险游戏。<br/>设计独属于你的角色和剧情，让ai为其赋予生命力，再打磨每一处细节。</p>
      </div>
      <div class="header-right">
        <router-link to="/profile" class="profile-link">👤 个人中心</router-link>
      </div>
    </div>
    
    <div class="actions-section">
      <el-button type="primary" size="large" @click="navigateTo('/manuscript-input')" class="create-btn">
        🆕 新建项目
      </el-button>
    </div>

    <div class="features-section">
      <h3>指引</h3>
      <p class="subtitle">4步让你的故事从想象转变为现实：</p>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-number">01</div>
          <div class="feature-icon">📝</div>
          <h4>结构化原稿输入</h4>
          <p>通过模板化表单输入剧情、角色和任务线</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-number">02</div>
          <div class="feature-icon">🤖</div>
          <h4>AI生成游戏雏形</h4>
          <p>智能AI根据原稿生成可编辑的游戏雏形</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-number">03</div>
          <div class="feature-icon">✏️</div>
          <h4>可视化编辑</h4>
          <p>直观编辑场景、角色、任务，实时预览效果</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-number">04</div>
          <div class="feature-icon">🕹️</div>
          <h4>像素风预览</h4>
          <p>实时体验设计的游戏，支持简单交互</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
.home-container {
  padding: 40px 20px; /* 增加垂直padding使页面更宽松 */
  max-width: 1200px;
  margin: 0 auto;
  background-color: #020817; /* 新的深蓝灰色背景 */
  border-radius: 10px;
  color: #ecf0f1; /* 浅灰色文字 */
  min-height: 100vh;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 50px; /* 增加间距 */
  padding: 10px 0;
  position: sticky;
  top: 20px;
  z-index: 100;
  background-color: #020817; /* 背景色与页面一致 */
}

.logo-section {
  text-align: center;
  flex: 1;
}

.pixel-logo {
  font-size: 5rem; /* 再次增大字号 */
  font-weight: bold;
  color: #E9A33B; /* 高亮色 */
  text-shadow: 0 0 5px #E9A33B, 0 0 10px #E9A33B; /* 减弱的荧光效果 */
  margin: 0 0 10px 0;
  letter-spacing: 3px;
  font-family: 'Unifont Medium', 'Courier New', 'monospace', sans-serif; /* 使用Unifont Medium字体 */
  font-variant: small-caps; /* 小型大写字母效果 */
  text-transform: capitalize; /* 保持首字母大写 */
}

.subheading {
  font-size: 1.8rem; /* 介于主标题和副标题之间的字号 */
  color: white;
  margin: 10px 0 15px;
  font-family: 'Courier New', 'monospace', sans-serif;
  letter-spacing: 1px;
}

.subtitle {
  color: #bdc3c7; /* 浅灰色文字 */
  font-size: 1.1rem;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
  text-align: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
  position: fixed; /* 固定定位，不随滚动变化 */
  right: 20px;
  top: 20px;
  z-index: 1000;
}

.profile-link {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.3s;
  border: 2px solid transparent;
  background-color: #383F59; /* 功能块色背景 */
}

.profile-link:hover {
  background-color: #E9A33B; /* 悬停高亮色 */
  color: black;
  text-decoration: underline;
  border: 2px solid #E9A33B; /* 悬停高亮色 */
  box-shadow: 0 0 10px #E9A33B; /* 氛围荧光效果 */
}

.features-section {
  margin-top: 60px; /* 增加间距 */
}

.features-section h3 {
  color: white;
  margin-bottom: 20px; /* 调整间距 */
  text-align: center;
  font-size: 1.8rem;
}

.features-section > .subtitle {
  color: #bdc3c7; /* 浅灰色文字 */
  font-size: 1.1rem;
  max-width: 800px;
  margin: 0 auto 40px; /* 增加下方间距 */
  line-height: 1.6;
  text-align: center;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px; /* 增加网格间距 */
  margin-top: 20px;
}

.feature-card {
  border: 1px solid #383F59; /* 功能块色边框 */
  border-radius: 8px;
  padding: 30px 20px; /* 增加内边距 */
  text-align: center;
  cursor: default; /* 改为默认光标，因为不再有点击功能 */
  transition: all 0.3s;
  background-color: #383F59; /* 功能块色背景 */
  color: white;
  position: relative; /* 为序号定位做准备 */
}

.feature-number {
  position: absolute;
  top: -12px;
  left: -12px;
  background-color: #E9A33B; /* 高亮色背景 */
  color: #020817; /* 深色文字 */
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
  border: 2px solid #E9A33B;
  z-index: 10;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(233, 163, 59, 0.5); /* #E9A33B氛围荧光效果 */
  border: 1px solid #E9A33B; /* 悬停高亮色 */
  box-shadow: 0 0 20px #E9A33B; /* 氛围荧光效果 */
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.feature-card h4 {
  margin: 10px 0;
  color: #ecf0f1; /* 浅灰色文字 */
}

.feature-card p {
  color: #bdc3c7; /* 浅灰色文字 */
  font-size: 14px;
}

.actions-section {
  text-align: center;
  margin: 60px 0; /* 增加间距 */
}

.create-btn {
  padding: 15px 30px;
  font-size: 18px;
}

/* 按钮样式 */
:deep(.el-button--primary) {
  --el-button-bg-color: #383F59 !important; /* 功能块色 */
  --el-button-border-color: #383F59 !important;
  --el-button-hover-bg-color: #E9A33B !important; /* 悬停高亮色 */
  --el-button-hover-border-color: #E9A33B !important;
  --el-button-active-bg-color: #E9A33B !important;
  --el-button-active-border-color: #E9A33B !important;
  transition: all 0.3s !important;
}

:deep(.el-button--primary):hover {
  box-shadow: 0 0 15px #E9A33B !important; /* 氛围荧光效果 */
}

:deep(.el-button) {
  --el-button-bg-color: #383F59 !important; /* 功能块色 */
  --el-button-border-color: #383F59 !important;
  --el-button-hover-bg-color: #E9A33B !important; /* 悬停高亮色 */
  --el-button-hover-border-color: #E9A33B !important;
  --el-button-active-bg-color: #E9A33B !important;
  --el-button-active-border-color: #E9A33B !important;
  color: white !important;
  transition: all 0.3s !important;
}

:deep(.el-button):hover {
  box-shadow: 0 0 15px #E9A33B !important; /* 氛围荧光效果 */
}
</style>