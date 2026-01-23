<template>
  <div class="home-container">
    <!-- 网格背景 -->
    <div class="grid-background"></div>
    
    <!-- 粒子效果 -->
    <div class="particle particle-1"></div>
    <div class="particle particle-2"></div>
    <div class="particle particle-3"></div>
    <div class="particle particle-4"></div>
    
    <div class="header-section">
      <div class="logo-section">
        <h1 class="pixel-logo animate-bounce-base">PixelForge</h1>
        <h2 class="subheading animate-fade-in-base">像素风情感叙事冒险游戏设计平台</h2>
        <p class="subtitle animate-fade-in-base">将你的故事打造成可游玩的像素风情感叙事冒险游戏。<br/>设计独属于你的角色和剧情，让ai为其赋予生命力，再打磨每一处细节。</p>
      </div>
      <div class="header-right">
        <router-link to="/profile" class="profile-link">👤 个人中心</router-link>
      </div>
    </div>
    
    <div class="actions-section">
      <el-button type="primary" size="large" @click="navigateTo('/manuscript-input')" class="create-btn animate-fade-in-base">
        🆕 新建项目
      </el-button>
    </div>

    <div class="features-section">
      <h3 class="animate-fade-in-base">指引</h3>
      <p class="subtitle animate-fade-in-base">4步让你的故事从想象转变为现实：</p>
      <div class="features-grid">
        <div class="feature-card animate-fade-in-base">
          <div class="feature-number">01</div>
          <div class="feature-icon">📝</div>
          <h4>结构化原稿输入</h4>
          <p>通过模板化表单输入剧情、角色和任务线</p>
        </div>
        
        <div class="feature-card animate-fade-in-base">
          <div class="feature-number">02</div>
          <div class="feature-icon">🤖</div>
          <h4>AI生成游戏雏形</h4>
          <p>智能AI根据原稿生成可编辑的游戏雏形</p>
        </div>
        
        <div class="feature-card animate-fade-in-base">
          <div class="feature-number">03</div>
          <div class="feature-icon">✏️</div>
          <h4>可视化编辑</h4>
          <p>直观编辑场景、角色、任务，实时预览效果</p>
        </div>
        
        <div class="feature-card animate-fade-in-base">
          <div class="feature-number">04</div>
          <div class="feature-icon">🕹️</div>
          <h4>像素风预览</h4>
          <p>实时体验设计的游戏，支持简单交互</p>
        </div>
      </div>
    </div>
    
    <!-- 底部空白区域 -->
    <div class="bottom-spacer"></div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { onMounted, nextTick, onUnmounted } from 'vue'

const router = useRouter()

const navigateTo = (path) => {
  router.push(path)
}

let animationObserver = null;

// 每次进入页面时重置动画
onMounted(async () => {
  // 确保DOM完全渲染
  await nextTick();
  
  // 立即触发动画序列
  triggerAnimations();
  
  // 使用Intersection Observer监听页面是否可见，以便在页面重新进入时再次触发
  animationObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && entry.target.classList.contains('home-container')) {
        // 当页面重新进入视窗时，再次触发动画
        setTimeout(() => {
          triggerAnimations();
        }, 100);
      }
    });
  }, {
    threshold: 0.1
  });
  
  animationObserver.observe(document.querySelector('.home-container'));
});

// 组件卸载时断开观察器
onUnmounted(() => {
  if (animationObserver) {
    animationObserver.disconnect();
  }
});

// 重新触发动画的函数
const triggerAnimations = () => {
  // 为所有动画元素添加动画类
  setTimeout(() => {
    // 首先触发PixelForge logo的弹跳动画
    const logo = document.querySelector('.pixel-logo');
    if (logo) {
      logo.classList.remove('animate-bounce');
      void logo.offsetWidth; // 强制重排
      logo.classList.add('animate-bounce');
    }
    
    // 然后触发所有元素的渐显动画
    setTimeout(() => {
      const fadeElements = document.querySelectorAll('.animate-fade-in-base');
      fadeElements.forEach(el => {
        el.classList.remove('animate-fade-in');
        void el.offsetWidth; // 强制重排
        el.classList.add('animate-fade-in');
      });
    }, 300);
  }, 10);
};
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
  overflow: hidden; /* 防止粒子效果溢出 */
  position: relative; /* 为绝对定位的元素提供参考 */
}

/* 网格背景 */
.grid-background {
  position: absolute;
  top: 80px; /* 从导航栏下方开始 */
  left: 0;
  right: 0;
  bottom: 600px; /* 在"指引"字段上方结束，增加更多距离 */
  background-image: 
    linear-gradient(to right, rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 30px 30px; /* 网格大小介于字号之间 */
  opacity: 0.6; /* 进一步提高透明度使网格更明显 */
  z-index: 0; /* 网格在内容后面 */
  pointer-events: none; /* 不影响鼠标交互 */
  mask-image: linear-gradient(to bottom, 
    rgba(0, 0, 0, 0) 0%, 
    rgba(0, 0, 0, 0.2) 10%, 
    rgba(0, 0, 0, 0.8) 30%, 
    rgba(0, 0, 0, 1) 50%, 
    rgba(0, 0, 0, 0.8) 70%, 
    rgba(0, 0, 0, 0.2) 90%, 
    rgba(0, 0, 0, 0) 100%);
  -webkit-mask-image: linear-gradient(to bottom, 
    rgba(0, 0, 0, 0) 0%, 
    rgba(0, 0, 0, 0.2) 10%, 
    rgba(0, 0, 0, 0.8) 30%, 
    rgba(0, 0, 0, 1) 50%, 
    rgba(0, 0, 0, 0.8) 70%, 
    rgba(0, 0, 0, 0.2) 90%, 
    rgba(0, 0, 0, 0) 100%);
}

/* 粒子效果 */
.particle {
  position: absolute;
  background-color: #E9A33B; /* 荧光黄色 */
  border-radius: 2px;
  animation: spin-float 8s infinite ease-in-out;
  z-index: 1;
  pointer-events: none; /* 不影响鼠标交互 */
}

.particle-1 {
  top: 15%;
  left: 10%;
  animation-delay: 0s;
  background-color: #E9A33B; /* 荧光黄色 */
  width: 10px; /* 略小 */
  height: 10px;
}

.particle-2 {
  top: 40%;
  right: 15%;
  animation-delay: 2s;
  background-color: #5D8AA8; /* 荧光蓝色 */
  width: 14px; /* 略大 */
  height: 14px;
}

.particle-3 {
  bottom: 30%;
  left: 20%;
  animation-delay: 4s;
  background-color: #FF6B6B; /* 荧光红色 */
  width: 12px; /* 标准大小 */
  height: 12px;
}

.particle-4 {
  bottom: 20%;
  right: 25%;
  animation-delay: 6s;
  background-color: #9C51B6; /* 荧光紫色 */
  width: 11px; /* 略小 */
  height: 11px;
}

@keyframes spin-float {
  0% {
    transform: rotate(0deg) translateX(0) translateY(0);
    opacity: 0.8;
  }
  15% {
    transform: rotate(90deg) translateX(10px) translateY(-5px);
  }
  20% {
    transform: rotate(90deg) translateX(10px) translateY(-5px); /* 短暂停顿 */
  }
  35% {
    transform: rotate(180deg) translateX(5px) translateY(10px);
  }
  40% {
    transform: rotate(180deg) translateX(5px) translateY(10px); /* 短暂停顿 */
  }
  55% {
    transform: rotate(270deg) translateX(-10px) translateY(5px);
  }
  60% {
    transform: rotate(270deg) translateX(-10px) translateY(5px); /* 短暂停顿 */
  }
  75% {
    transform: rotate(360deg) translateX(0) translateY(0);
  }
  80% {
    transform: rotate(360deg) translateX(0) translateY(0); /* 短暂停顿 */
  }
  100% {
    transform: rotate(0deg) translateX(0) translateY(0);
    opacity: 0.8;
  }
}

/* 子动画：模拟洒落的小粒子 */
.particle::before {
  content: '';
  position: absolute;
  width: 3px; /* 小粒子尺寸 */
  height: 3px;
  background-color: currentColor;
  border-radius: 1px;
  opacity: 0;
  animation: sprinkle 8s infinite;
}

@keyframes sprinkle {
  20%, 40%, 60%, 80% {
    opacity: 1;
    transform: scale(1);
  }
  25%, 45%, 65%, 85% {
    opacity: 0;
    transform: scale(0) rotate(180deg);
  }
}

/* 动画样式 */
.animate-bounce-base {
  opacity: 0;
  transform: translateY(-20px);
}

.animate-bounce {
  animation: bounce-in 0.6s ease-out forwards;
}

.animate-fade-in-base {
  opacity: 0;
}

.animate-fade-in {
  animation: fade-in 0.8s ease-out 0.3s forwards;
}

.animate-block-text-base {
  position: relative;
}

.animate-block-text::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #383F59;
  z-index: 5;
}

.animate-block-text {
  animation: reveal-text 1s ease-out 0.6s forwards;
}

@keyframes bounce-in {
  0% {
    opacity: 0;
    transform: translateY(-40px) scale(0.8);
  }
  60% {
    opacity: 1;
    transform: translateY(5px) scale(1.05);
  }
  80% {
    transform: translateY(-5px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes fade-in {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes reveal-text {
  0% {
    opacity: 1;
    clip-path: inset(0 100% 0 0);
  }
  100% {
    opacity: 1;
    clip-path: inset(0 0 0 0);
  }
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 50px; /* 增加间距 */
  padding: 150px 10px 10px 10px; /* 增加上内边距 */
  position: relative; /* 相对定位 */
  z-index: 2; /* 确保内容在网格之上 */
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
  margin-top: 240px; /* 大幅增加间距，约为之前距离的三倍 */
  position: relative; /* 相对定位 */
  z-index: 2; /* 确保内容在网格之上 */
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
  background-color: #383F59; /* 灰色背景 */
  color: white; /* 白色文字 */
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
  transition: all 0.3s ease; /* 添加过渡效果 */
}

.feature-card:hover .feature-number {
  background-color: #E9A33B; /* 黄色背景 */
  color: #020817; /* 黑色文字 */
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
  margin: 80px 0; /* 增加间距，使页面分为上下两部分 */
  position: relative; /* 相对定位 */
  z-index: 2; /* 确保内容在网格之上 */
}

.create-btn {
  padding: 15px 30px;
  font-size: 18px;
}

.bottom-spacer {
  height: 200px; /* 添加底部空白区域 */
  margin-top: 40px;
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