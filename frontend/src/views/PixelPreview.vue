<template>
  <div class="preview-page">
    <div class="pixel-container pixel-grid">
      <div class="game-header">
        <span class="pixel-text">{{ gameData.title }}</span>
      </div>

      <div class="scene-content">
        <p class="dialog-text">{{ currentScene.text }}</p>
      </div>

      <div class="pixel-dialog">
        <div v-for="opt in currentScene.options" :key="opt.text" 
             class="pixel-button" @click="handleOption(opt.next)">
          > {{ opt.text }}
        </div>
      </div>

      <div class="character-sprite">
        🚶
      </div>
    </div>
    
    <div class="controls">
      <el-button @click="$router.back()">返回编辑器</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import request from '../utils/request'
import '../assets/pixel.css'

const route = useRoute()
const gameData = ref({ title: '加载中...', scenes: [] })
const currentSceneId = ref('s1')
const currentScene = ref({ text: '加载中...', options: [] })

const loadGame = async () => {
  const res = await request.get(`/projects/${route.query.id || '1'}/data`)
  gameData.value = res.game_data
  currentSceneId.value = gameData.value.scenes[0].id
  updateScene()
}

const updateScene = () => {
  currentScene.value = gameData.value.scenes.find(s => s.id === currentSceneId.value) || gameData.value.scenes[0]
}

const handleOption = (nextId) => {
  currentSceneId.value = nextId
  updateScene()
}

onMounted(loadGame)
</script>

<style scoped>
.preview-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}
.game-header {
  border-bottom: 2px solid #fff;
  padding-bottom: 10px;
  margin-bottom: 20px;
}
.pixel-text {
  font-size: 24px;
  text-transform: uppercase;
}
.scene-content {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.dialog-text {
  font-size: 20px;
  line-height: 1.5;
  text-align: center;
}
.character-sprite {
  position: absolute;
  bottom: 20px;
  right: 20px;
  font-size: 40px;
}
.controls {
  margin-top: 20px;
  text-align: center;
}
</style>
