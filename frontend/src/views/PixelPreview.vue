<template>
  <div class="pixel-preview-container">
    <div class="preview-header">
      <h2>🎮 像素风游戏预览</h2>
      <div class="control-buttons">
        <el-button 
          :type="isPaused ? 'success' : 'warning'" 
          @click="togglePause"
        >
          {{ isPaused ? '▶️ 继续' : '⏸️ 暂停' }}
        </el-button>
        <el-button @click="resetScene">🔄 重置场景</el-button>
        <el-button type="primary" @click="backToEditor">↩️ 返回编辑页</el-button>
      </div>
    </div>
    
    <div class="game-container">
      <!-- 像素风网格背景 -->
      <div 
        class="game-scene" 
        :style="{ backgroundImage: getSceneBackground(currentScene) }"
        @click="handleSceneClick"
      >
        <!-- 场景边界指示器 -->
        <div class="boundary-indicator top" @click="transitionToScene('top')">🚪</div>
        <div class="boundary-indicator right" @click="transitionToScene('right')">🚪</div>
        <div class="boundary-indicator bottom" @click="transitionToScene('bottom')">🚪</div>
        <div class="boundary-indicator left" @click="transitionToScene('left')">🚪</div>
        
        <!-- 像素风角色 -->
        <div 
          class="pixel-character" 
          :style="{ left: playerPosition.x + 'px', top: playerPosition.y + 'px' }"
        >
          {{ getPlayerIcon }}
        </div>
        
        <!-- 像素风NPC和互动元素 -->
        <div 
          v-for="(element, index) in currentScene.interactiveElements" 
          :key="index"
          class="pixel-element"
          :class="{ 'near-player': isNearPlayer(element.position[0], element.position[1]) }"
          :style="{ left: element.position[0] + 'px', top: element.position[1] + 'px' }"
          @click="interactWithElement(element)"
        >
          <div class="element-icon">{{ getElementIcon(element.type) }}</div>
          <div class="element-label">{{ element.name }}</div>
        </div>
        
        <!-- 网格线（装饰性） -->
        <div class="grid-overlay" v-if="showGrid"></div>
      </div>
      
      <!-- 像素风对话框 -->
      <div 
        v-if="showDialog" 
        class="pixel-dialog-box"
        :style="{ left: dialogPosition.x + 'px', top: dialogPosition.y + 'px' }"
      >
        <div class="dialog-header">
          <span>{{ currentDialog.npcName }}</span>
          <el-button 
            type="danger" 
            size="small" 
            icon="Close" 
            circle 
            @click="closeDialog"
            class="close-btn"
          />
        </div>
        <div class="dialog-content">
          <p>{{ currentDialog.text[currentDialog.currentIndex] }}</p>
        </div>
        <div class="dialog-controls">
          <el-button 
            v-if="currentDialog.currentIndex < currentDialog.text.length - 1" 
            @click="nextDialog"
            size="small"
          >
            下一页
          </el-button>
          <el-button 
            @click="closeDialog"
            size="small"
          >
            关闭
          </el-button>
        </div>
      </div>
      
      <!-- 任务提示框 -->
      <div v-if="showTaskPrompt" class="task-prompt">
        <div class="prompt-content">
          <h4>✨ 任务触发</h4>
          <p>{{ currentTaskPrompt }}</p>
          <el-button @click="closeTaskPrompt" size="small">知道了</el-button>
        </div>
      </div>
      
      <!-- 控制说明 -->
      <div class="controls-help">
        <p>⌨️ 使用方向键移动角色</p>
        <p>🖱️ 点击NPC或道具进行互动</p>
      </div>
    </div>
    
    <!-- 移动控制按钮（移动端友好） -->
    <div class="mobile-controls" v-if="isMobile">
      <div class="control-row">
        <div class="control-btn" @click="movePlayer('up')">⬆️</div>
      </div>
      <div class="control-row">
        <div class="control-btn" @click="movePlayer('left')">⬅️</div>
        <div class="control-btn" @click="movePlayer('down')">⬇️</div>
        <div class="control-btn" @click="movePlayer('right')">➡️</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../utils/request'

const route = useRoute()
const router = useRouter()

// 游戏数据
const gameData = ref({})
const currentScene = ref({})
const playerPosition = ref({ x: 100, y: 100 })

// 控制状态
const isPaused = ref(false)
const showDialog = ref(false)
const currentDialog = ref({
  npcName: '',
  text: [],
  currentIndex: 0
})
const dialogPosition = ref({ x: 100, y: 100 })
const showTaskPrompt = ref(false)
const currentTaskPrompt = ref('')
const showGrid = ref(true)

// 设备检测
const isMobile = computed(() => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
})

// 获取游戏ID
const gameId = route.query.id || 'default'

// 初始化
onMounted(async () => {
  await loadGamePreview()
  setupKeyboardControls()
  
  // 如果是从编辑器跳转过来的，可能需要从本地存储获取最新数据
  const localData = localStorage.getItem(`game_${gameId}`)
  if (localData) {
    try {
      gameData.value = JSON.parse(localData)
      setCurrentScene(gameData.value.scenes[0])
      ElMessage.success('已加载最新编辑数据')
    } catch (error) {
      console.error('加载本地游戏数据失败:', error)
    }
  }
})

// 销毁时清理
onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
})

// 加载游戏预览数据
async function loadGamePreview() {
  try {
    const response = await request.get(`/game/preview/${gameId}`)
    if (response.code === 200) {
      gameData.value = response.data
      setCurrentScene(gameData.value.scenes[0])
      ElMessage.success('游戏数据加载成功！')
    } else {
      throw new Error(response.msg || '获取游戏数据失败')
    }
  } catch (error) {
    console.error('加载游戏预览数据失败:', error)
    ElMessage.error('加载游戏数据失败，使用默认数据')
    
    // 使用默认数据
    gameData.value = getDefaultGameData()
    setCurrentScene(gameData.value.scenes[0])
  }
}

// 设置当前场景
function setCurrentScene(scene) {
  currentScene.value = scene
  // 重置玩家位置到场景默认位置
  playerPosition.value = { x: 100, y: 100 }
}

// 获取默认游戏数据
function getDefaultGameData() {
  return {
    gameId: 'default',
    gameName: '像素风冒险游戏',
    scenes: [
      {
        id: 'scene_start',
        name: '村庄广场',
        backgroundDescription: '宁静的像素风格村庄',
        interactiveElements: [
          { type: 'npc', name: '村长', position: [150, 120], dialogue: ['欢迎来到我们的村庄！', '有什么可以帮助你的吗？']},
          { type: 'item', name: '宝箱', position: [250, 200], description: '看起来很珍贵的宝箱'},
          { type: 'building', name: '商店', position: [300, 150], description: '杂货店'}
        ],
        transitions: [
          { targetSceneId: 'scene_forest', condition: 'edge_right', description: '前往森林'}
        ]
      },
      {
        id: 'scene_forest',
        name: '森林',
        backgroundDescription: '茂密的像素风格森林',
        interactiveElements: [
          { type: 'npc', name: '精灵', position: [120, 100], dialogue: ['小心森林中的危险！', '前方有神秘洞穴']},
          { type: 'item', name: '蘑菇', position: [200, 180], description: '看起来可以食用的蘑菇'}
        ],
        transitions: [
          { targetSceneId: 'scene_start', condition: 'edge_left', description: '返回村庄'}
        ]
      }
    ],
    characters: [
      {
        id: 'player',
        name: '玩家',
        appearance: '像素风冒险者',
        personality: '勇敢好奇',
        initialPosition: 'scene_start',
        dialogues: ['我将探索这个奇妙的世界！']
      }
    ],
    missions: [
      {
        id: 'mission_1',
        name: '新手教程',
        triggerScene: 'scene_start',
        triggerCondition: '与村长对话',
        completionCondition: '了解基本操作',
        dialogueContent: '欢迎来到游戏世界！',
        reward: { xp: 50, items: ['铜币'] },
        nextMissionId: null
      }
    ]
  }
}

// 键盘控制设置
function setupKeyboardControls() {
  window.addEventListener('keydown', handleKeyDown)
}

// 处理键盘事件
function handleKeyDown(event) {
  if (isPaused.value) return
  
  switch(event.key) {
    case 'ArrowUp':
      event.preventDefault()
      movePlayer('up')
      break
    case 'ArrowDown':
      event.preventDefault()
      movePlayer('down')
      break
    case 'ArrowLeft':
      event.preventDefault()
      movePlayer('left')
      break
    case 'ArrowRight':
      event.preventDefault()
      movePlayer('right')
      break
    case ' ': // 空格键触发互动
      event.preventDefault()
      triggerInteraction()
      break
  }
}

// 移动玩家
function movePlayer(direction) {
  if (isPaused.value) return
  
  const step = 20 // 每次移动20像素
  let newX = playerPosition.value.x
  let newY = playerPosition.value.y
  
  switch(direction) {
    case 'up':
      newY = Math.max(20, newY - step)
      break
    case 'down':
      newY = Math.min(380, newY + step) // 假设场景高度400px
      break
    case 'left':
      newX = Math.max(20, newX - step)
      break
    case 'right':
      newX = Math.min(580, newX + step) // 假设场景宽度600px
      break
  }
  
  playerPosition.value = { x: newX, y: newY }
  
  // 检查是否到达边界，触发场景跳转
  checkBoundaryTransition(newX, newY)
}

// 检查边界跳转
function checkBoundaryTransition(x, y) {
  // 检查是否接近边缘（比如边缘20像素内）
  if (x < 30) { // 左边界
    const transition = currentScene.value.transitions.find(t => t.condition.includes('left'))
    if (transition) {
      transitionToSceneById(transition.targetSceneId)
    }
  } else if (x > 570) { // 右边界
    const transition = currentScene.value.transitions.find(t => t.condition.includes('right'))
    if (transition) {
      transitionToSceneById(transition.targetSceneId)
    }
  } else if (y < 30) { // 上边界
    const transition = currentScene.value.transitions.find(t => t.condition.includes('up'))
    if (transition) {
      transitionToSceneById(transition.targetSceneId)
    }
  } else if (y > 370) { // 下边界
    const transition = currentScene.value.transitions.find(t => t.condition.includes('down'))
    if (transition) {
      transitionToSceneById(transition.targetSceneId)
    }
  }
}

// 跳转到指定场景
function transitionToSceneById(sceneId) {
  const targetScene = gameData.value.scenes.find(s => s.id === sceneId)
  if (targetScene) {
    setCurrentScene(targetScene)
    ElMessage.success(`已进入 ${targetScene.name}`)
  }
}

// 处理场景点击（用于移动角色到点击位置）
function handleSceneClick(event) {
  if (isPaused.value) return
  
  const rect = event.currentTarget.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  // 限制在场景范围内
  playerPosition.value = {
    x: Math.max(20, Math.min(580, x)),
    y: Math.max(20, Math.min(380, y))
  }
}

// 检查是否接近某个元素
function isNearPlayer(x, y) {
  const distance = Math.sqrt(
    Math.pow(playerPosition.value.x - x, 2) + 
    Math.pow(playerPosition.value.y - y, 2)
  )
  return distance < 40 // 40像素内的视为接近
}

// 与元素互动
function interactWithElement(element) {
  if (element.type === 'npc' && element.dialogue) {
    showDialog.value = true
    currentDialog.value = {
      npcName: element.name,
      text: element.dialogue,
      currentIndex: 0
    }
    // 对话框位置在元素附近
    dialogPosition.value = {
      x: Math.min(500, element.position[0]), // 限制在窗口内
      y: Math.max(50, element.position[1] - 100) // 在元素上方
    }
  } else if (element.type === 'item') {
    ElMessage.success(`获得了: ${element.description || element.name}`)
  } else if (element.type === 'building') {
    ElMessage.info(`${element.name}: ${element.description}`)
  }
}

// 触发互动（空格键）
function triggerInteraction() {
  // 遍历场景中的元素，找到接近玩家的可互动元素
  for (const element of currentScene.value.interactiveElements) {
    if (isNearPlayer(element.position[0], element.position[1])) {
      interactWithElement(element)
      break
    }
  }
}

// 下一条对话
function nextDialog() {
  if (currentDialog.value.currentIndex < currentDialog.value.text.length - 1) {
    currentDialog.value.currentIndex++
  } else {
    closeDialog()
  }
}

// 关闭对话框
function closeDialog() {
  showDialog.value = false
  currentDialog.value = {
    npcName: '',
    text: [],
    currentIndex: 0
  }
}

// 显示任务提示
function showTaskNotification(promptText) {
  currentTaskPrompt.value = promptText
  showTaskPrompt.value = true
  
  // 3秒后自动关闭
  setTimeout(() => {
    closeTaskPrompt()
  }, 3000)
}

// 关闭任务提示
function closeTaskPrompt() {
  showTaskPrompt.value = false
  currentTaskPrompt.value = ''
}

// 跳转到场景（通过边界指示器）
function transitionToScene(direction) {
  // 根据方向查找对应的跳转
  const transition = currentScene.value.transitions.find(t => t.condition.toLowerCase().includes(direction))
  if (transition) {
    transitionToSceneById(transition.targetSceneId)
  } else {
    ElMessage.info('此方向没有可通行的道路')
  }
}

// 切换暂停状态
function togglePause() {
  isPaused.value = !isPaused.value
  if (isPaused.value) {
    ElMessage.info('游戏已暂停')
  } else {
    ElMessage.success('游戏继续')
  }
}

// 重置场景
function resetScene() {
  if (gameData.value.scenes && gameData.value.scenes.length > 0) {
    setCurrentScene(gameData.value.scenes[0])
    playerPosition.value = { x: 100, y: 100 }
    ElMessage.success('场景已重置')
  }
}

// 返回编辑页
function backToEditor() {
  router.push(`/visual-editor?gameId=${gameId}`)
}

// 获取玩家图标
const getPlayerIcon = computed(() => {
  return '🧍' // 可以根据角色外观设置不同图标
})

// 获取元素图标
function getElementIcon(type) {
  switch(type) {
    case 'npc': return '👤'
    case 'item': return '📦'
    case 'building': return '🏠'
    case 'quest_npc': return '👑'
    default: return '❓'
  }
}

// 获取场景背景
function getSceneBackground(scene) {
  // 根据场景名称或描述返回对应的背景
  if (scene.name.includes('森林')) {
    return 'linear-gradient(45deg, #2ecc71, #27ae60)'
  } else if (scene.name.includes('村庄')) {
    return 'linear-gradient(45deg, #f1c40f, #f39c12)'
  } else if (scene.name.includes('洞穴')) {
    return 'linear-gradient(45deg, #7f8c8d, #95a5a6)'
  } else {
    return 'linear-gradient(45deg, #3498db, #2980b9)'
  }
}
</script>

<style scoped>
.pixel-preview-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #020817; /* 新的深蓝灰色背景 */
  color: white;
  font-family: 'Courier New', Courier, monospace;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #383F59; /* 功能块色 */
  border-bottom: 4px solid #E9A33B; /* 高亮边框 */
}

.control-buttons {
  display: flex;
  gap: 10px;
}

.game-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.game-scene {
  width: 600px;
  height: 400px;
  position: relative;
  border: 4px solid #E9A33B; /* 高亮边框 */
  box-shadow: 0 0 20px rgba(233, 163, 59, 0.5); /* 高亮阴影 */
  background-size: 40px 40px;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  overflow: hidden;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  pointer-events: none;
}

.boundary-indicator {
  position: absolute;
  font-size: 24px;
  color: #E9A33B; /* 高亮色 */
  opacity: 0.7;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 10;
}

.boundary-indicator:hover {
  opacity: 1;
  transform: scale(1.2);
  text-shadow: 0 0 10px #E9A33B; /* 氛围荧光效果 */
}

.boundary-indicator.top {
  top: 5px;
  left: 50%;
  transform: translateX(-50%);
}

.boundary-indicator.right {
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
}

.boundary-indicator.bottom {
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
}

.boundary-indicator.left {
  left: 5px;
  top: 50%;
  transform: translateY(-50%);
}

.pixel-character {
  position: absolute;
  font-size: 30px;
  transition: all 0.2s ease;
  z-index: 5;
  text-shadow: 2px 2px 0 #000;
}

.pixel-element {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 4;
}

.pixel-element.near-player {
  transform: scale(1.2);
  filter: brightness(1.3);
  box-shadow: 0 0 10px #E9A33B; /* 氛围荧光效果 */
}

.element-icon {
  font-size: 24px;
  margin-bottom: 5px;
  text-shadow: 1px 1px 0 #000;
}

.element-label {
  font-size: 12px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 2px 6px;
  border-radius: 10px;
  white-space: nowrap;
}

.pixel-dialog-box {
  position: absolute;
  background: #383F59; /* 功能块色对话框背景 */
  border: 4px solid #E9A33B; /* 高亮边框 */
  border-radius: 8px;
  padding: 15px;
  min-width: 250px;
  z-index: 100;
  box-shadow: 0 0 20px #E9A33B; /* 氛围荧光效果 */
  font-family: 'Courier New', Courier, monospace;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 5px;
  border-bottom: 2px solid #E9A33B; /* 高亮分割线 */
  font-weight: bold;
}

.close-btn {
  padding: 2px !important;
}

.dialog-content {
  margin-bottom: 15px;
}

.dialog-content p {
  margin: 0;
  line-height: 1.5;
  color: #ecf0f1; /* 浅灰色文字 */
}

.dialog-controls {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.task-prompt {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  animation: slideIn 0.3s;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.prompt-content {
  background: #E9A33B; /* 高亮色 */
  color: black;
  padding: 15px;
  border-radius: 8px;
  border: 3px solid #383F59; /* 功能块色边框 */
  box-shadow: 0 0 15px #E9A33B; /* 氛围荧光效果 */
  min-width: 250px;
}

.prompt-content h4 {
  margin: 0 0 5px 0;
}

.prompt-content p {
  margin: 5px 0;
  font-size: 14px;
}

.controls-help {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background: rgba(56, 63, 89, 0.8); /* 功能块色半透明 */
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 12px;
}

.mobile-controls {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 50;
}

.control-row {
  display: flex;
  justify-content: center;
  margin-bottom: 5px;
}

.control-btn {
  width: 50px;
  height: 50px;
  background: #383F59; /* 功能块色 */
  border: 2px solid #E9A33B; /* 高亮边框 */
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  cursor: pointer;
  user-select: none;
  box-shadow: 0 4px 0 #E9A33B; /* 高亮阴影 */
  transition: all 0.1s;
}

.control-btn:active {
  transform: translateY(2px);
  box-shadow: 0 2px 0 #E9A33B; /* 高亮阴影 */
}

.control-btn:hover {
  background: #E9A33B; /* 高亮色 */
  color: black;
  box-shadow: 0 0 15px #E9A33B; /* 氛围荧光效果 */
}

/* 响应式设计 */
@media (max-width: 768px) {
  .game-scene {
    width: 90vw;
    max-width: 400px;
    height: 300px;
  }
  
  .mobile-controls {
    position: static;
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}
</style>