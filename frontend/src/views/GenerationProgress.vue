<template>
  <div class="generation-container">
    <el-card>
      <h2>🎮 正在为您生成游戏雏形...</h2>
      <p>任务 ID: {{ taskId }}</p>
      
      <div class="progress-section">
        <el-progress 
          type="circle" 
          :percentage="progress" 
          :status="status === 'completed' ? 'success' : ''"
        />
        <p class="status-text">{{ statusMessage }}</p>
      </div>

      <div class="actions">
        <el-button @click="cancelTask" :disabled="status === 'completed'">取消生成</el-button>
        <el-button type="primary" v-if="status === 'completed'" @click="goToEditor">进入编辑器</el-button>
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
const taskId = ref(route.query.taskId)
const progress = ref(0)
const status = ref('processing')
const statusMessage = ref('AI 正在构思场景...')

let timer = null

const pollStatus = async () => {
  try {
    const res = await request.get(`/ai/task/${taskId.value}`)
    progress.value = res.progress
    status.value = res.status
    
    if (status.value === 'completed') {
      statusMessage.value = '生成完成！'
      clearInterval(timer)
    } else if (status.value === 'processing') {
      statusMessage.value = `正在生成中... ${progress.value}%`
    }
  } catch (err) {
    clearInterval(timer)
  }
}

onMounted(() => {
  if (taskId.value) {
    timer = setInterval(pollStatus, 2000)
  }
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

const cancelTask = () => {
  clearInterval(timer)
  router.push('/workplace')
}

const goToEditor = () => {
  router.push(`/editor?taskId=${taskId.value}`)
}
</script>

<style scoped>
.generation-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}
.progress-section {
  text-align: center;
  margin: 40px 0;
}
.status-text {
  margin-top: 20px;
  font-size: 18px;
  color: #666;
}
.actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}
</style>
