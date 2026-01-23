<template>
  <div class="home-container">
    <div class="hero-section">
      <h2>🎮 欢迎使用像素风情感叙事冒险游戏设计平台</h2>
      <p>轻松创建属于你的像素风冒险世界，无需编程经验</p>
    </div>
    
    <div class="features-section">
      <h3>✨ 平台核心功能</h3>
      <div class="features-grid">
        <div class="feature-card" @click="navigateTo('/manuscript-input')">
          <div class="feature-icon">📝</div>
          <h4>结构化原稿输入</h4>
          <p>通过模板化表单输入剧情、角色和任务线</p>
        </div>
        
        <div class="feature-card" @click="navigateTo('/generation-progress')">
          <div class="feature-icon">🤖</div>
          <h4>AI生成游戏雏形</h4>
          <p>智能AI根据原稿生成可编辑的游戏雏形</p>
        </div>
        
        <div class="feature-card" @click="navigateTo('/visual-editor')">
          <div class="feature-icon">✏️</div>
          <h4>可视化编辑</h4>
          <p>直观编辑场景、角色、任务，实时预览效果</p>
        </div>
        
        <div class="feature-card" @click="navigateTo('/pixel-preview')">
          <div class="feature-icon">🕹️</div>
          <h4>像素风预览</h4>
          <p>实时体验设计的游戏，支持简单交互</p>
        </div>
      </div>
    </div>
    
    <div class="games-section">
      <h3>📁 我的游戏作品</h3>
      <div class="games-list">
        <div class="game-item">
          <div class="game-info">
            <h4>新手村冒险</h4>
            <p>状态: 已编辑</p>
          </div>
          <div class="game-actions">
            <el-button type="primary" size="small">继续编辑</el-button>
            <el-button size="small">预览</el-button>
          </div>
        </div>
        <div class="game-item">
          <div class="game-info">
            <h4>森林探险记</h4>
            <p>状态: 生成中</p>
          </div>
          <div class="game-actions">
            <el-button type="primary" size="small">查看进度</el-button>
            <el-button size="small">重新生成</el-button>
          </div>
        </div>
        <div class="game-item">
          <div class="game-info">
            <h4>神秘洞穴之谜</h4>
            <p>状态: 待生成</p>
          </div>
          <div class="game-actions">
            <el-button type="primary" size="small">开始生成</el-button>
            <el-button size="small">编辑</el-button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="actions-section">
      <el-button type="primary" size="large" @click="navigateTo('/manuscript-input')" class="create-btn">
        🆕 创建新游戏
      </el-button>
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
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #020817; /* 新的深蓝灰色背景 */
  border-radius: 10px;
  color: #ecf0f1; /* 浅灰色文字 */
}

.hero-section {
  text-align: center;
  margin-bottom: 40px;
  padding: 30px;
  background: linear-gradient(135deg, #383F59 0%, #020817 100%); /* 功能块色到背景色渐变 */
  color: white;
  border-radius: 10px;
}

.hero-section h2 {
  margin: 0 0 10px 0;
  color: white;
}

.hero-section p {
  margin: 0;
  color: #bdc3c7; /* 浅灰色文字 */
}

.features-section {
  margin-bottom: 40px;
}

.features-section h3 {
  color: white;
  margin-bottom: 20px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.feature-card {
  border: 1px solid #383F59; /* 功能块色边框 */
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #383F59; /* 功能块色背景 */
  color: white;
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

.games-section {
  margin-bottom: 40px;
}

.games-section h3 {
  color: white;
  margin-bottom: 20px;
}

.games-list {
  margin-top: 20px;
}

.game-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 1px solid #383F59; /* 功能块色边框 */
  border-radius: 8px;
  margin-bottom: 10px;
  background-color: #383F59; /* 功能块色背景 */
  color: white;
}

.game-info h4 {
  margin: 0 0 5px 0;
  color: #ecf0f1; /* 浅灰色文字 */
}

.game-info p {
  margin: 0;
  color: #bdc3c7; /* 浅灰色文字 */
  font-size: 14px;
}

.game-actions {
  display: flex;
  gap: 10px;
}

.actions-section {
  text-align: center;
  margin-top: 40px;
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