<template>
  <!-- 装饰元素：左右城堡森林 -->
  <div class="decorative-left-castle"></div>
  <div class="decorative-right-castle"></div>
  
  <!-- 装饰元素：小河 -->
  <div class="decorative-river"></div>
  <div class="decorative-river-overlay"></div>
  
  <!-- 装饰元素：像素星星 -->
  <div class="decorative-star star-1"></div>
  <div class="decorative-star star-2"></div>
  <div class="decorative-star star-3"></div>
  <div class="decorative-star star-4"></div>
  <div class="decorative-star star-5"></div>
  
  <!-- 装饰元素：像素云朵 -->
  <div class="decorative-cloud cloud-1"></div>
  <div class="decorative-cloud cloud-2"></div>

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
        <p class="subtitle animate-fade-in-base">将你的故事打造成可游玩的像素风情感叙事冒险游戏。<br/>设计独属于你的角色和剧情,让ai为其赋予生命力,再打磨每一处细节。</p>
      </div>
      <div class="header-right">
        <router-link to="/profile" class="profile-link">👤 个人中心</router-link>
      </div>
    </div>
    
    <div class="actions-section">
      <el-button type="primary" size="large" @click="navigateTo('/manuscript-input')" class="create-btn animate-fade-in-base">
        EXPLORE
      </el-button>
      <p class="button-subtext animate-fade-in-base">start your own game.</p>
    </div>

    <!-- 像素小人动画 -->
    <div class="character-animation-container">
      <div class="pixel-character girl-with-sword"></div>
      <div class="pixel-character boy-with-staff"></div>
    </div>

    <div class="features-section">
      <h3 class="animate-fade-in-base">指引</h3>
      <p class="subtitle animate-fade-in-base">4步让你的故事从想象转变为现实：</p>
      <div class="features-grid">
        <div class="feature-card animate-fade-in-base" @click="onCardClick">
          <div class="feature-number">01</div>
          <div class="feature-icon">
            <!-- 像素小房子 -->
            <svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <!-- 屋顶 -->
              <rect x="20" y="8" width="8" height="4" fill="#8B4513"/>
              <rect x="16" y="12" width="16" height="4" fill="#8B4513"/>
              <rect x="12" y="16" width="24" height="4" fill="#D2691E"/>
              <!-- 房子主体 -->
              <rect x="12" y="20" width="24" height="20" fill="#FFD4A3" stroke="#000"/>
              <!-- 门 -->
              <rect x="18" y="28" width="8" height="12" fill="#8B4513"/>
              <rect x="20" y="32" width="2" height="2" fill="#FFD700"/>
              <!-- 窗户 -->
              <rect x="28" y="24" width="6" height="6" fill="#87CEEB" stroke="#000"/>
              <rect x="30" y="24" width="2" height="6" fill="#000"/>
              <rect x="28" y="27" width="6" height="2" fill="#000"/>
            </svg>
          </div>
          <h4>结构化原稿输入</h4>
          <p>通过模板化表单输入剧情、角色和任务线</p>
        </div>
        
        <div class="feature-card animate-fade-in-base" @click="onCardClick">
          <div class="feature-number">02</div>
          <div class="feature-icon">
            <!-- 两个手牵手的像素小人 -->
            <svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <!-- 左边小人 -->
              <rect x="8" y="12" width="6" height="6" fill="#FFD4A3"/>
              <rect x="8" y="18" width="6" height="8" fill="#FF6B6B"/>
              <rect x="14" y="20" width="4" height="4" fill="#FFD4A3"/>
              <rect x="8" y="26" width="3" height="8" fill="#4A4A4A"/>
              <rect x="11" y="26" width="3" height="8" fill="#4A4A4A"/>
              <!-- 右边小人 -->
              <rect x="34" y="12" width="6" height="6" fill="#FFD4A3"/>
              <rect x="34" y="18" width="6" height="8" fill="#4ECDC4"/>
              <rect x="30" y="20" width="4" height="4" fill="#FFD4A3"/>
              <rect x="34" y="26" width="3" height="8" fill="#2C3E50"/>
              <rect x="37" y="26" width="3" height="8" fill="#2C3E50"/>
              <!-- 手牵手 -->
              <rect x="18" y="20" width="12" height="4" fill="#FFD4A3"/>
              <!-- 爱心 -->
              <rect x="22" y="6" width="4" height="2" fill="#FF6B6B"/>
              <rect x="20" y="8" width="8" height="4" fill="#FF6B6B"/>
              <rect x="22" y="12" width="4" height="2" fill="#FF6B6B"/>
            </svg>
          </div>
          <h4>AI生成游戏雏形</h4>
          <p>智能AI根据原稿生成可编辑的游戏雏形</p>
        </div>
        
        <div class="feature-card animate-fade-in-base" @click="onCardClick">
          <div class="feature-number">03</div>
          <div class="feature-icon">
            <!-- 风景像素图案 -->
            <svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <!-- 太阳 -->
              <rect x="36" y="8" width="6" height="6" fill="#FFD700"/>
              <rect x="34" y="10" width="2" height="2" fill="#FFD700"/>
              <rect x="42" y="10" width="2" height="2" fill="#FFD700"/>
              <!-- 云朵 -->
              <rect x="10" y="10" width="12" height="4" fill="#FFF"/>
              <rect x="12" y="8" width="8" height="2" fill="#FFF"/>
              <!-- 山 -->
              <rect x="20" y="28" width="4" height="4" fill="#8B7355"/>
              <rect x="16" y="32" width="12" height="4" fill="#A0826D"/>
              <!-- 树 -->
              <rect x="8" y="28" width="4" height="8" fill="#8B4513"/>
              <rect x="6" y="24" width="8" height="4" fill="#228B22"/>
              <rect x="8" y="20" width="4" height="4" fill="#228B22"/>
              <!-- 草地 -->
              <rect x="4" y="36" width="40" height="8" fill="#7CFC00"/>
            </svg>
          </div>
          <h4>可视化编辑</h4>
          <p>直观编辑场景、角色、任务,实时预览效果</p>
        </div>
        
        <div class="feature-card animate-fade-in-base" @click="onCardClick">
          <div class="feature-number">04</div>
          <div class="feature-icon">
            <!-- 像素小车 -->
            <svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <!-- 车身 -->
              <rect x="8" y="24" width="32" height="8" fill="#FF6B6B" stroke="#000"/>
              <!-- 车顶 -->
              <rect x="14" y="16" width="20" height="8" fill="#FF6B6B" stroke="#000"/>
              <!-- 窗户 -->
              <rect x="16" y="18" width="8" height="6" fill="#87CEEB"/>
              <rect x="26" y="18" width="6" height="6" fill="#87CEEB"/>
              <!-- 车轮 -->
              <rect x="12" y="32" width="8" height="8" fill="#2C3E50" stroke="#000"/>
              <rect x="14" y="34" width="4" height="4" fill="#696969"/>
              <rect x="28" y="32" width="8" height="8" fill="#2C3E50" stroke="#000"/>
              <rect x="30" y="34" width="4" height="4" fill="#696969"/>
              <!-- 车灯 -->
              <rect x="38" y="26" width="2" height="4" fill="#FFD700"/>
            </svg>
          </div>
          <h4>像素风预览</h4>
          <p>实时体验设计的游戏,支持简单交互</p>
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
  // 触发粒子爆炸效果
  const btn = document.querySelector('.create-btn')
  if (btn) {
    btn.classList.add('particle-burst')
  }
  
  // 粒子效果后跳转
  setTimeout(() => {
    router.push(path)
  }, 600)
}

const onCardClick = (event) => {
  // 触发卡片粒子爆炸效果
  const card = event.currentTarget
  if (card && !card.classList.contains('card-burst')) {
    card.classList.add('card-burst')
    // 1秒后移除效果类，允许再次触发
    setTimeout(() => {
      card.classList.remove('card-burst')
    }, 1000)
  }
}

let animationObserver = null;

// 每次进入页面时重置动画
onMounted(async () => {
  // 确保DOM完全渲染
  await nextTick();
  
  // 立即触发动画序列
  triggerAnimations();

  // 使用Intersection Observer监听页面是否可见,以便在页面重新进入时再次触发
  animationObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && entry.target.classList.contains('.home-container')) {
        // 当页面重新进入视窗时,再次触发动画
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
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #020817;
  border-radius: 10px;
  color: #ecf0f1;
  min-height: 100vh;
  overflow: visible;
  position: relative;
}

/* 网格背景 */
.grid-background {
  position: absolute;
  top: 90px;
  left: 0;
  right: 0;
  bottom: 300px;
  background-image: 
    linear-gradient(to right, rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
  background-size: 30px 30px, auto;
  opacity: 0.6;
  z-index: 0;
  pointer-events: none;
  mask-image: linear-gradient(to bottom, 
    rgba(0, 0, 0, 1) 0%, 
    rgba(0, 0, 0, 1) 10%, 
    rgba(0, 0, 0, 0.8) 30%, 
    rgba(0, 0, 0, 0.5) 50%, 
    rgba(0, 0, 0, 0.2) 70%, 
    rgba(0, 0, 0, 0) 90%, 
    rgba(0, 0, 0, 0) 100%);
}

/* 粒子效果 */
.particle {
  position: absolute;
  background-color: #E9A33B;
  border-radius: 2px;
  animation: spin-float 8s infinite ease-in-out;
  z-index: 1;
  pointer-events: none;
}

.particle-1 {
  top: 25%;
  left: 15%;
  animation-delay: 0s;
  background-color: #E9A33B;
  width: 10px;
  height: 10px;
}

.particle-2 {
  top: 30%;
  right: 20%;
  animation-delay: 2s;
  background-color: #5D8AA8;
  width: 14px;
  height: 14px;
}

.particle-3 {
  bottom: 40%;
  left: 25%;
  animation-delay: 4s;
  background-color: #FF6B6B;
  width: 12px;
  height: 12px;
}

.particle-4 {
  bottom: 35%;
  right: 30%;
  animation-delay: 6s;
  background-color: #9C51B6;
  width: 11px;
  height: 11px;
}

@keyframes spin-float {
  0%, 100% {
    transform: rotate(0deg) translate(0, 0);
    opacity: 0.8;
  }
  15% {
    transform: rotate(90deg) translate(10px, -5px);
  }
  35% {
    transform: rotate(180deg) translate(5px, 10px);
  }
  55% {
    transform: rotate(270deg) translate(-10px, 5px);
  }
  75% {
    transform: rotate(360deg) translate(0, 0);
  }
}

/* 动画样式 */
.animate-bounce-base {
  opacity: 0;
  transform: translateY(-20px);
}

.animate-bounce {
  animation: bounce-in 1.2s ease-out forwards;
}

.animate-fade-in-base {
  opacity: 0;
}

.animate-fade-in {
  animation: fade-in 0.8s ease-out 0.3s forwards;
}

@keyframes bounce-in {
  0% {
    opacity: 0;
    transform: translateY(-40px) scale(0.1);
  }
  50% {
    opacity: 1;
    transform: translateY(10px) scale(1.1);
  }
  75% {
    transform: translateY(-10px) scale(0.95);
  }
  100% {
    transform: translateY(0) scale(1);
    opacity: 1;
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

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 64px;
  padding: 60px 10px 10px 10px;
  position: relative;
  z-index: 3;
}

.logo-section {
  text-align: center;
  flex: 1;
}

.pixel-logo {
  font-size: 5rem;
  font-weight: bold;
  color: #E9A33B;
  text-shadow: 0 0 5px #E9A33B, 0 0 10px #E9A33B;
  margin: 0 0 10px 0;
  letter-spacing: 3px;
  font-family: 'Unifont Medium', 'Courier New', 'monospace', sans-serif;
  font-variant: small-caps;
  text-transform: capitalize;
}

.subheading {
  font-size: 24px;
  color: white;
  margin: 16px 0;
  font-family: 'Courier New', 'monospace', sans-serif;
  letter-spacing: 1px;
}

.subtitle {
  color: white;
  font-size: 14px;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
  text-align: center;
  font-family: 'Courier New', 'monospace', sans-serif;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
  position: fixed;
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
  background-color: #383F59;
}

.profile-link:hover {
  background-color: #E9A33B;
  color: black;
  text-decoration: underline;
  border: 2px solid #E9A33B;
  box-shadow: 0 0 10px #E9A33B;
}

.actions-section {
  text-align: center;
  margin: 64px 0 48px;
  position: relative;
  z-index: 3;
}

.create-btn {
  width: 128px;
  height: 48px;
  padding: 0;
  font-family: 'Press Start 2P', cursive;
  font-size: 16px;
  background-color: #8a2be2 !important;
  border: 1px solid black !important;
  color: white !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  transition: all 0.1s ease !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: visible;
}

.create-btn:hover {
  transform: translateY(-1px);
  border-color: #ff8c00 !important;
  background-color: #8a2be2 !important;
}

/* 粒子爆炸效果 */
.create-btn.particle-burst::before,
.create-btn.particle-burst::after {
  content: '';
  position: absolute;
  width: 8px;
  height: 8px;
  background-color: #ff8c00;
  left: 50%;
  top: 50%;
  animation: burst-particle 0.6s ease-out;
}

.create-btn.particle-burst::before {
  animation-name: burst-particle-1;
}

.create-btn.particle-burst::after {
  animation-name: burst-particle-2;
}

@keyframes burst-particle-1 {
  0% {
    transform: translate(0, 0);
    opacity: 1;
  }
  25% {
    box-shadow: -16px -16px 0 2px #ff8c00, 16px -16px 0 2px #ff8c00, -16px 16px 0 2px #8a2be2, 16px 16px 0 2px #8a2be2;
  }
  100% {
    box-shadow: -48px -48px 0 2px transparent, 48px -48px 0 2px transparent, -48px 48px 0 2px transparent, 48px 48px 0 2px transparent;
    opacity: 0;
  }
}

@keyframes burst-particle-2 {
  0% {
    transform: translate(0, 0);
    opacity: 1;
  }
  25% {
    box-shadow: 0 -16px 0 2px #8a2be2, 16px 0 0 2px #ff8c00, 0 16px 0 2px #8a2be2, -16px 0 0 2px #ff8c00;
  }
  100% {
    box-shadow: 0 -64px 0 2px transparent, 64px 0 0 2px transparent, 0 64px 0 2px transparent, -64px 0 0 2px transparent;
    opacity: 0;
  }
}

.button-subtext {
  font-family: 'Courier New', 'monospace', sans-serif;
  font-size: 14px;
  color: white;
  margin-top: 16px;
  opacity: 0.8;
}

/* 像素小人动画样式 */
.character-animation-container {
  position: relative;
  width: 100%;
  height: 96px;
  margin: 32px auto 0;
  pointer-events: none;
  z-index: 2;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 48px;
}

.pixel-character {
  width: 72px;
  height: 72px;
  background-size: 288px 72px;
  image-rendering: pixelated;
  animation: sprite-walk 0.8s steps(4) infinite;
}

.girl-with-sword {
  background-image: url('/girl-sword-sprite.svg');
}

.boy-with-staff {
  background-image: url('/boy-staff-sprite.svg');
}

@keyframes sprite-walk {
  from { background-position: 0 0; }
  to { background-position: -288px 0; }
}

.features-section {
  margin-top: 240px;
  position: relative;
  z-index: 3;
}

.features-section h3 {
  color: white;
  margin-bottom: 32px;
  text-align: center;
  font-size: 32px;
  font-family: 'Courier New', 'monospace', sans-serif;
}

.features-section > .subtitle {
  color: white;
  font-size: 14px;
  max-width: 800px;
  margin: 0 auto 48px;
  line-height: 1.6;
  text-align: center;
  font-family: 'Courier New', 'monospace', sans-serif;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 48px;
  margin-top: 64px;
  padding: 32px;
}

.feature-card {
  border: none;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background-color: transparent;
  color: white;
  position: relative;
  overflow: visible;
}

/* 使用伪元素创建像素圆角，避免clip-path裁剪序号 */
.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #383F59;
  border: 1px solid black;
  z-index: -1;
  clip-path: polygon(
    0 4px, 4px 4px, 4px 0,
    calc(100% - 4px) 0, calc(100% - 4px) 4px, 100% 4px,
    100% calc(100% - 4px), calc(100% - 4px) calc(100% - 4px), calc(100% - 4px) 100%,
    4px 100%, 4px calc(100% - 4px), 0 calc(100% - 4px)
  );
  transition: all 0.2s;
}

.feature-card:hover {
  transform: translateY(-2px);
}

.feature-card:hover::before {
  border: 1px solid #ff8c00;
  box-shadow: 0 0 16px rgba(255, 140, 0, 0.3);
}

/* 卡片粒子爆炸效果 */
.feature-card.card-burst::after {
  content: '';
  position: absolute;
  width: 8px;
  height: 8px;
  background-color: transparent;
  left: 50%;
  top: 50%;
  animation: card-burst-particles 0.8s ease-out;
  pointer-events: none;
  z-index: 10;
}

@keyframes card-burst-particles {
  0% {
    box-shadow: 
      0 0 0 2px #ff8c00,
      0 0 0 2px #ff8c00,
      0 0 0 2px #ff8c00,
      0 0 0 2px #ff8c00,
      0 0 0 2px #8a2be2,
      0 0 0 2px #8a2be2,
      0 0 0 2px #8a2be2,
      0 0 0 2px #8a2be2;
    opacity: 1;
  }
  100% {
    box-shadow: 
      -48px -48px 0 2px transparent,
      48px -48px 0 2px transparent,
      -48px 48px 0 2px transparent,
      48px 48px 0 2px transparent,
      0 -64px 0 2px transparent,
      64px 0 0 2px transparent,
      0 64px 0 2px transparent,
      -64px 0 0 2px transparent;
    opacity: 0;
  }
}

.feature-number {
  position: absolute;
  top: -24px;
  left: -24px;
  background-color: #ff8c00;
  color: white;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  font-family: 'Press Start 2P', cursive;
  border: 1px solid black;
  z-index: 100;
  clip-path: polygon(
    0 4px, 4px 4px, 4px 0,
    calc(100% - 4px) 0, calc(100% - 4px) 4px, 100% 4px,
    100% calc(100% - 4px), calc(100% - 4px) calc(100% - 4px), calc(100% - 4px) 100%,
    4px 100%, 4px calc(100% - 4px), 0 calc(100% - 4px)
  );
}

.feature-icon {
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
}

.feature-card h4 {
  margin: 16px 0;
  color: white;
  font-family: 'Courier New', 'monospace', sans-serif;
  font-size: 16px;
}

.feature-card p {
  color: white;
  font-size: 14px;
  font-family: 'Courier New', 'monospace', sans-serif;
  line-height: 1.4;
}

.bottom-spacer {
  height: 200px;
  margin-top: 40px;
}

/* 装饰元素样式 */
.decorative-left-castle {
  position: fixed;
  left: 20px;
  top: 50%;
  transform: translateY(-50%) scale(0.8);
  width: 200px;
  height: 300px;
  background-image: url('/left-castle-forest.svg');
  background-size: contain;
  background-repeat: no-repeat;
  opacity: 0.9;
  z-index: 1;
  pointer-events: none;
}

.decorative-right-castle {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%) scale(0.8);
  width: 200px;
  height: 300px;
  background-image: url('/right-castle-forest.svg');
  background-size: contain;
  background-repeat: no-repeat;
  opacity: 0.9;
  z-index: 1;
  pointer-events: none;
}

.decorative-river {
  position: fixed;
  bottom: 50px;
  left: 0;
  width: 100%;
  height: 80px;
  background-image: url("/pixel-river.svg");
  background-size: auto 100%;
  background-repeat: repeat-x;
  opacity: 0.9;
  z-index: 1;
  pointer-events: none;
  animation: river-flow 8s linear infinite;
}

.decorative-walking-characters {
  position: fixed;
  bottom: 100px;
  left: 10%;
  width: 100px;
  height: 50px;
  background-image: url("/walking-characters.svg");
  background-size: contain;
  background-repeat: no-repeat;
  opacity: 0.9;
  z-index: 2;
  pointer-events: none;
  animation: walk-along-river 12s linear infinite;
}

@keyframes walk-along-river {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(calc(100vw - 200px));
  }
}

@keyframes river-flow {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50px);
  }
}
</style>

<style>
/* 全局装饰元素样式 - 不使用scoped以确保应用到根级元素 */
.decorative-left-castle {
  position: fixed !important;
  left: 20px !important;
  top: 50% !important;
  transform: translateY(-50%) scale(0.8) !important;
  width: 200px !important;
  height: 300px !important;
  background-image: url('/left-castle-forest.svg') !important;
  background-size: contain !important;
  background-repeat: no-repeat !important;
  opacity: 0.85 !important;
  z-index: 1 !important;
  pointer-events: none !important;
}

.decorative-right-castle {
  position: fixed !important;
  right: 20px !important;
  top: 50% !important;
  transform: translateY(-50%) scale(0.8) !important;
  width: 200px !important;
  height: 300px !important;
  background-image: url('/right-castle-forest.svg') !important;
  background-size: contain !important;
  background-repeat: no-repeat !important;
  opacity: 0.85 !important;
  z-index: 1 !important;
  pointer-events: none !important;
}

.decorative-river {
  position: fixed !important;
  bottom: 48px !important;
  left: 0 !important;
  width: 200% !important;
  height: 48px !important;
  background-image: url('/pixel-river.svg') !important;
  background-size: 320px 48px !important;
  background-repeat: repeat-x !important;
  opacity: 0.85 !important;
  z-index: 1 !important;
  pointer-events: none !important;
  animation: river-flow-main 5s linear infinite !important;
}

.decorative-river-overlay {
  position: fixed !important;
  bottom: 48px !important;
  left: 0 !important;
  width: 200% !important;
  height: 48px !important;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(135, 206, 250, 0.12) 25%, 
    rgba(100, 149, 237, 0.15) 50%, 
    rgba(135, 206, 250, 0.12) 75%, 
    transparent 100%) !important;
  background-size: 320px 48px !important;
  opacity: 0.85 !important;
  z-index: 1 !important;
  pointer-events: none !important;
  animation: river-shimmer 3s linear infinite !important;
}

/* 像素星星装饰 */
.decorative-star {
  position: fixed !important;
  width: 16px !important;
  height: 16px !important;
  background: #FFD700 !important;
  clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%) !important;
  opacity: 0.85 !important;
  z-index: 1 !important;
  pointer-events: none !important;
  animation: star-twinkle 2s ease-in-out infinite !important;
}

.star-1 { top: 80px !important; left: 10% !important; animation-delay: 0s !important; }
.star-2 { top: 120px !important; right: 8% !important; animation-delay: 0.4s !important; width: 12px !important; height: 12px !important; }
.star-3 { top: 200px !important; left: 5% !important; animation-delay: 0.8s !important; width: 10px !important; height: 10px !important; }
.star-4 { top: 160px !important; right: 12% !important; animation-delay: 1.2s !important; }
.star-5 { bottom: 200px !important; left: 8% !important; animation-delay: 1.6s !important; width: 14px !important; height: 14px !important; }

/* 像素云朵装饰 */
.decorative-cloud {
  position: fixed !important;
  width: 64px !important;
  height: 32px !important;
  opacity: 0.85 !important;
  z-index: 1 !important;
  pointer-events: none !important;
  background: 
    radial-gradient(circle at 16px 20px, rgba(255,255,255,0.9) 12px, transparent 12px),
    radial-gradient(circle at 32px 16px, rgba(255,255,255,0.9) 16px, transparent 16px),
    radial-gradient(circle at 48px 20px, rgba(255,255,255,0.9) 12px, transparent 12px) !important;
  animation: cloud-float 20s linear infinite !important;
}

.cloud-1 { top: 100px !important; left: -64px !important; animation-duration: 25s !important; }
.cloud-2 { top: 180px !important; left: -64px !important; animation-duration: 30s !important; animation-delay: 10s !important; width: 80px !important; height: 40px !important; }

@keyframes river-flow-main {
  0% { transform: translateX(0); }
  100% { transform: translateX(-320px); }
}

@keyframes river-shimmer {
  0% { transform: translateX(0); }
  100% { transform: translateX(-320px); }
}

@keyframes star-twinkle {
  0%, 100% { opacity: 0.85; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.8); }
}

@keyframes cloud-float {
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(100vw + 128px)); }
}
</style>
