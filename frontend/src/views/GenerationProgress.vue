<template>
  <div class="generation-container">
    <el-card>
      <h2>🤖 正在为您生成游戏雏形...</h2>
      <p>任务 ID: {{ taskId }}</p>
      
      <div class="progress-section">
        <!-- 像素风加载动画 -->
        <div class="pixel-loader">
          <div class="pixel-block"></div>
          <div class="pixel-block"></div>
          <div class="pixel-block"></div>
          <div class="pixel-block"></div>
        </div>
        
        <!-- 进度条 -->
        <el-progress 
          type="circle" 
          :percentage="progress" 
          :status="status === 'completed' ? 'success' : status === 'failed' ? 'exception' : ''"
          :width="150"
          :stroke-width="10"
        />
        
        <p class="status-text">{{ statusMessage }}</p>
      </div>

      <div class="actions">
        <el-button @click="cancelTask" :disabled="status === 'completed' || status === 'failed'">❌ 取消任务</el-button>
        <el-button @click="backToEdit">✏️ 返回原稿编辑</el-button>
        <el-button 
          type="primary" 
          v-if="status === 'completed'" 
          @click="goToEditor"
        >
          ✨ 进入可视化编辑器
        </el-button>
        <el-button 
          type="warning" 
          v-if="status === 'failed'" 
          @click="retryGeneration"
        >
          🔄 重新生成
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '../utils/request'

const route = useRoute()
const router = useRouter()
const taskId = ref(route.query.taskId || '')
const progress = ref(0)
const status = ref('pending') // pending, completed, failed
const statusMessage = ref('AI 正在构思场景...')

let pollTimer = null

// 轮询任务状态
const pollStatus = async () => {
  try {
    const res = await request.get(`/ai/task/${taskId.value}`)
    
    if (res.code === 200) {
      progress.value = res.data.progress
      status.value = res.data.status
      
      if (status.value === 'completed') {
        statusMessage.value = '生成完成！'
        clearInterval(pollTimer)
        // 可以在这里保存生成的游戏数据到本地存储
        if (res.data.result) {
          localStorage.setItem(`game_${res.data.data.taskId}`, JSON.stringify(res.data.result))
        }
      } else if (status.value === 'failed') {
        statusMessage.value = `生成失败: ${res.data.errorMsg || '未知错误'}`
        clearInterval(pollTimer)
      } else if (status.value === 'pending') {
        statusMessage.value = `正在生成中... ${progress.value}%`
      }
    } else {
      console.error('获取任务状态失败:', res)
      statusMessage.value = '获取状态失败，正在重试...'
    }
  } catch (err) {
    console.error('轮询任务状态出错:', err)
    statusMessage.value = '网络错误，正在重试...'
  }
}

onMounted(() => {
  if (taskId.value) {
    // 立即执行一次查询
    pollStatus()
    // 然后每3秒轮询一次
    pollTimer = setInterval(pollStatus, 3000)
  } else {
    statusMessage.value = '无效的任务ID'
  }
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})

const cancelTask = () => {
  clearInterval(pollTimer)
  status.value = 'cancelled'
  statusMessage.value = '任务已取消'
}

const backToEdit = () => {
  clearInterval(pollTimer)
  router.push('/manuscript-input')
}

const goToEditor = () => {
  clearInterval(pollTimer)
  // 携带taskId和gameId跳转到可视化编辑器
  router.push(`/visual-editor?taskId=${taskId.value}&gameId=${taskId.value}`) // 在实际实现中，gameId应该从响应中获取
}

const retryGeneration = () => {
  // 重新开始生成，这里只是跳转回原稿编辑页面
  router.push('/manuscript-input')
}
</script>

<style scoped>
.generation-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  background-color: #2c3a47; /* 深蓝灰色背景 */
  padding: 20px;
}

.el-card {
  width: 100%;
  max-width: 600px;
  text-align: center;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  background-color: #34495e !important; /* 深蓝灰卡片背景 */
  border: 1px solid #4a6278 !important; /* 深蓝灰边框 */
}

.el-card h2 {
  color: white;
}

.el-card p {
  color: #ecf0f1; /* 浅灰色文字 */
}

.progress-section {
  text-align: center;
  margin: 40px 0;
  padding: 20px;
}

.status-text {
  margin-top: 20px;
  font-size: 18px;
  color: #ecf0f1; /* 浅灰色文字 */
  font-weight: bold;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
  margin-top: 30px;
}

/* 像素风加载动画 */
.pixel-loader {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
  height: 60px;
}

.pixel-block {
  width: 15px;
  height: 15px;
  background-color: #3498db; /* 深蓝灰主题色 */
  margin: 0 3px;
  animation: pixelBounce 1.5s infinite ease-in-out;
}

.pixel-block:nth-child(2) {
  animation-delay: 0.2s;
}

.pixel-block:nth-child(3) {
  animation-delay: 0.4s;
}

.pixel-block:nth-child(4) {
  animation-delay: 0.6s;
}

@keyframes pixelBounce {
  0%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-15px);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .generation-container {
    height: auto;
    padding: 20px 10px;
  }
  
  .el-card {
    margin: 10px;
  }
  
  .actions {
    flex-direction: column;
    align-items: center;
  }
  
  .el-button {
    width: 80%;
    margin: 5px 0;
  }
}
</style>