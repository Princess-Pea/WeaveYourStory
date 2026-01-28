<template>
  <div class="game-preview-container">
    <!-- 游戏渲染区域 -->
    <div class="game-area" ref="gameAreaRef">
      <canvas 
        ref="gameCanvasRef" 
        id="game-canvas" 
        :width="canvasSize.width" 
        :height="canvasSize.height"
        tabindex="0"
        @keydown="handleKeyDown"
        @keyup="handleKeyUp"
        @mousedown="handleMouseDown"
        @mouseup="handleMouseUp"
        @mousemove="handleMouseMove"
        @focus="focusCanvas"
      ></canvas>
    </div>

    <!-- 控制面板 -->
    <div class="control-panel">
      <el-button-group>
        <el-button 
          type="primary" 
          icon="Back" 
          @click="goBackToEditor"
        >
          返回编辑
        </el-button>
        <el-button 
          type="success" 
          icon="Download" 
          @click="exportGame"
          :loading="exporting"
        >
          导出游戏
        </el-button>
      </el-button-group>
      
      <el-button-group>
        <el-button 
          :icon="isPaused ? 'VideoPlay' : 'VideoPause'" 
          @click="togglePause"
        >
          {{ isPaused ? '继续' : '暂停' }}
        </el-button>
        <el-button 
          icon="Refresh" 
          @click="resetGame"
        >
          重置
        </el-button>
      </el-button-group>
    </div>

    <!-- 导出进度弹窗 -->
    <el-dialog 
      v-model="showExportDialog" 
      title="正在导出游戏" 
      width="40%" 
      :show-close="false"
      :close-on-press-escape="false"
      :close-on-click-modal="false"
    >
      <div class="export-content">
        <el-progress 
          :percentage="exportProgress" 
          :status="exportProgress === 100 ? 'success' : ''"
          :indeterminate="exportProgress < 100"
        />
        <p>{{ exportStatus }}</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

// 导入素材配置
import { getSceneBackground, getCharacterSprite, getInteractiveElement } from '@/constants/assetConfig'

// 引入其他必要的模块
const router = useRouter()
const route = useRoute()

// 响应式数据
const gameCanvasRef = ref(null)
const gameAreaRef = ref(null)
const exporting = ref(false)
const showExportDialog = ref(false)
const exportProgress = ref(0)
const exportStatus = ref('准备导出...')
const isPaused = ref(false)
const canvasSize = ref({ width: 800, height: 600 })

// 游戏相关变量
let canvas = null
let ctx = null
let gameLoopId = null
let gameState = null
let gameData = null

// 初始化
onMounted(async () => {
  await nextTick()
  initializeGame()
  
  // 监听窗口大小变化，重新计算Canvas尺寸
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  // 清理游戏循环
  if (gameLoopId) {
    cancelAnimationFrame(gameLoopId)
  }
  
  // 移除事件监听器
  window.removeEventListener('resize', handleResize)
})

// 窗口大小改变时重新计算Canvas尺寸
function handleResize() {
  // 使用setTimeout确保DOM更新完成
  setTimeout(calculateCanvasSize, 100)
}

// 初始化游戏
async function initializeGame() {
  canvas = gameCanvasRef.value
  if (!canvas) {
    console.error('Canvas element not found')
    return
  }
  
  // 计算合适的Canvas尺寸
  calculateCanvasSize()
  
  ctx = canvas.getContext('2d')
  
  // 获取游戏数据
  const gameId = route.query.gameId
  if (gameId) {
    try {
      gameData = await loadGameFromServer(gameId)
      if (!gameData) {
        throw new Error('Failed to load game data')
      }
      startGame()
    } catch (error) {
      console.error('Error loading game:', error)
      ElMessage.error('加载游戏数据失败')
      // 默认创建一个简单的游戏
      createSampleGame()
      startGame()
    }
  } else {
    // 如果没有传入游戏ID，创建示例游戏
    createSampleGame()
    startGame()
  }
}

// 计算Canvas尺寸以适应容器
function calculateCanvasSize() {
  if (gameAreaRef.value) {
    // 获取容器的可用空间（减去padding）
    const containerWidth = gameAreaRef.value.clientWidth - 40 // 减去左右各20px的padding
    const containerHeight = gameAreaRef.value.clientHeight - 40 // 减去上下各20px的padding
    
    // Canvas原始尺寸
    const originalWidth = 800
    const originalHeight = 600
    
    // 计算缩放比例
    const scaleX = containerWidth / originalWidth
    const scaleY = containerHeight / originalHeight
    const scale = Math.min(scaleX, scaleY, 1) // 不超过1倍，即不超过原始尺寸
    
    // 计算新的Canvas尺寸
    const newWidth = Math.floor(originalWidth * scale)
    const newHeight = Math.floor(originalHeight * scale)
    
    // 更新Canvas尺寸
    canvasSize.value = {
      width: newWidth,
      height: newHeight
    }
  } else {
    // 默认尺寸
    canvasSize.value = {
      width: 800,
      height: 600
    }
  }
}

// 从服务器加载游戏数据
async function loadGameFromServer(gameId) {
  try {
    console.log('尝试加载游戏数据，gameId:', gameId);
    
    // 首先尝试从localStorage获取游戏数据（开发者模式）
    const localGameData = localStorage.getItem(`game_${gameId}`);
    if (localGameData) {
      try {
        const parsedData = JSON.parse(localGameData);
        console.log('从localStorage加载游戏数据成功:', parsedData);
        console.log('场景数量:', parsedData.scenes?.length || 0);
        console.log('角色数量:', parsedData.characters?.length || 0);
        console.log('场景背景图片存在:', !!parsedData.scenes?.[0]?.backgroundImage);
        console.log('角色精灵图片存在:', !!parsedData.characters?.[0]?.sprite);
        return parsedData;
      } catch (parseError) {
        console.error('解析本地游戏数据失败:', parseError);
        console.error('本地数据内容:', localGameData);
      }
    } else {
      console.log('未在localStorage中找到游戏数据:', `game_${gameId}`);
      
      // 检查是否处于开发者模式
      const isDeveloperMode = localStorage.getItem('developerMode') === 'true';
      if (isDeveloperMode) {
        console.log('开发者模式下未找到游戏数据，返回null');
        return null;
      }
    }
    
    // 如果不是开发者模式（即普通模式），才尝试网络请求
    const isDeveloperMode = localStorage.getItem('developerMode') === 'true';
    if (!isDeveloperMode) {  // 只有在非开发者模式下才发起网络请求
      // 首先尝试从游戏预览API获取数据（这是专门用于游戏预览的接口）
      const response = await fetch(`/api/v1/game/preview/${gameId}`)
      if (!response.ok) {
        // 如果预览API不可用，尝试从项目API获取数据
        const projectResponse = await fetch(`/api/v1/projects/${gameId}`)
        if (!projectResponse.ok) {
          throw new Error(`HTTP error! status: ${projectResponse.status}`)
        }
        const projectResult = await projectResponse.json()
        if (projectResult.code !== 200) {
          throw new Error(projectResult.msg || '获取项目数据失败')
        }
        
        // 提取项目数据并转换为游戏格式
        const projectData = projectResult.data.project
        return transformProjectToGameData(projectData)
      }
      
      const result = await response.json()
      if (result.code !== 200) {
        throw new Error(result.msg || '获取游戏数据失败')
      }
      
      // 直接返回游戏数据
      return result.data
    } else {
      console.log('开发者模式下不发起网络请求');
      return null;
    }
  } catch (error) {
    console.error('Error fetching game data:', error)
    return null
  }
}

// 将项目数据转换为游戏数据格式
function transformProjectToGameData(project) {
  // 如果项目中包含了manuscript_data，其中可能包含完整的可视化编辑数据
  const manuscriptData = project.manuscript_data || {}
  
  // 如果manuscriptData中包含gameData（即可视化编辑器保存的数据）
  if (manuscriptData.gameData) {
    return manuscriptData.gameData
  }
  
  // 否则尝试从manuscriptData构建游戏数据
  return {
    gameId: project.id,
    gameName: project.title || '未命名游戏',
    emotionalTone: manuscriptData.emotionalTone || '轻松愉快',
    style: manuscriptData.style || 'pixel_art',
    scenes: manuscriptData.scenes || [],
    characters: manuscriptData.characters || [],
    missions: manuscriptData.missions || [],
    interactionRules: manuscriptData.interactionRules || {
      movement: {
        up: '向上移动',
        down: '向下移动',
        left: '向左移动',
        right: '向右移动'
      },
      dialogueTrigger: {
        distance: 30,
        key: 'SPACE'
      },
      itemInteraction: {
        distance: 20,
        key: 'E'
      }
    }
  }
}

// 创建空游戏数据
function createSampleGame() {
  gameData = {
    gameId: 'empty',
    gameName: '空白游戏',
    emotionalTone: '默认',
    style: 'pixel_art',
    scenes: [], // 空场景数组
    characters: [],
    missions: [],
    interactionRules: {
      movement: {
        up: '向上移动',
        down: '向下移动',
        left: '向左移动',
        right: '向右移动'
      },
      dialogueTrigger: {
        distance: 30,
        key: 'SPACE'
      },
      itemInteraction: {
        distance: 20,
        key: 'E'
      }
    }
  }

  // 初始化游戏状态
  gameState = {
    currentSceneId: null,
    playerPosition: { x: 100, y: 100 },
    playerDirection: 'right',
    collectedItems: [],
    completedMissions: [],
    showDialogue: false,
    dialogueText: '',
    isMoving: false
  }
}

// 开始游戏
function startGame() {
  // 开始游戏主循环
  if (gameLoopId) {
    cancelAnimationFrame(gameLoopId)
  }
  gameLoopId = requestAnimationFrame(gameLoop)
}

// 游戏主循环
function gameLoop(timestamp) {
  if (!isPaused.value) {
    update()
    render()
  }
  gameLoopId = requestAnimationFrame(gameLoop)
}

// 更新游戏逻辑
function update() {
  // 在这里实现游戏逻辑更新
  // 如角色移动、碰撞检测、任务进度等
}

// 渲染游戏画面
function render() {
  if (!ctx) return
  
  // 清空画布
  ctx.fillStyle = '#87CEEB' // 天蓝色背景
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  
  // 绘制场景元素
  drawScene()
  
  // 绘制玩家角色
  drawPlayer()
  
  // 如果有对话，绘制对话框
  if (gameState.showDialogue) {
    drawDialogueBox()
  }
}

// 绘制场景
function drawScene() {
  if (!gameData || !gameState) return
  
  const currentScene = gameData.scenes.find(s => s.id === gameState.currentSceneId)
  
  // 绘制背景
  drawBackground(currentScene)
  
  // 绘制地形
  drawTerrain(currentScene)
  
  // 绘制场景中的交互元素
  if (currentScene) {
    currentScene.interactiveElements.forEach(element => {
      drawInteractiveElement(element)
    })
  }
  
  // 绘制场景名称
  if (currentScene) {
    drawSceneLabel(currentScene.name)
  }
}

// 绘制背景
function drawBackground(currentScene) {
  // 如果当前场景有预设的背景图片，优先使用
  if (currentScene && currentScene.backgroundImage) {
    const img = new Image();
    img.src = currentScene.backgroundImage;
    
    // 为了防止阻塞渲染，我们直接绘制渐变作为后备
    drawFallbackBackground(currentScene);
    
    // 在图片加载完成后绘制
    img.onload = () => {
      // 清除画布
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // 计算缩放比例以适应Canvas
      const scaleX = canvas.width / img.width;
      const scaleY = canvas.height / img.height;
      const scale = Math.min(scaleX, scaleY);
      
      // 计算居中位置
      const x = (canvas.width - img.width * scale) / 2;
      const y = (canvas.height - img.height * scale) / 2;
      
      // 绘制背景图片
      ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
      
      // 重新绘制场景细节
      const currentScene = gameData.scenes.find(s => s.id === gameState.currentSceneId);
      drawPixelDetails(currentScene);
      drawTerrain(currentScene);
      if (currentScene) {
        currentScene.interactiveElements.forEach(element => {
          drawInteractiveElement(element);
        });
      }
      drawPlayer();
      if (gameState.showDialogue) {
        drawDialogue();
      }
    };
  } else {
    // 如果没有预设图片，使用原有的渐变绘制
    drawFallbackBackground(currentScene);
  }
}

// 备用的渐变背景绘制
function drawFallbackBackground(currentScene) {
  // 根据场景描述设置不同的像素风格背景
  if (currentScene && currentScene.backgroundDescription) {
    const desc = currentScene.backgroundDescription.toLowerCase()
    if (desc.includes('夜晚') || desc.includes('夜')) {
      // 夜晚场景 - 深蓝色渐变
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
      gradient.addColorStop(0, '#000033') // 深蓝顶
      gradient.addColorStop(1, '#001122') // 更深的蓝底
      ctx.fillStyle = gradient
    } else if (desc.includes('森林') || desc.includes('树林')) {
      // 森林场景 - 绿色调
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
      gradient.addColorStop(0, '#a0d8ef') // 天空蓝
      gradient.addColorStop(0.7, '#6bbd8c') // 森林绿
      gradient.addColorStop(1, '#5a9c79') // 深森林绿
      ctx.fillStyle = gradient
    } else if (desc.includes('洞穴') || desc.includes('山洞')) {
      // 洞穴场景 - 暗灰色
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
      gradient.addColorStop(0, '#4a4a4a') // 灰顶
      gradient.addColorStop(1, '#2c2c2c') // 深灰底
      ctx.fillStyle = gradient
    } else if (desc.includes('城堡') || desc.includes('宫殿')) {
      // 城堡场景 - 金色调
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
      gradient.addColorStop(0, '#f0e6d2') // 淡金色天空
      gradient.addColorStop(1, '#d4b483') // 土黄色地面
      ctx.fillStyle = gradient
    } else if (desc.includes('海滩') || desc.includes('海边')) {
      // 海滩场景 - 蓝色和沙色
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
      gradient.addColorStop(0, '#87ceeb') // 天空蓝
      gradient.addColorStop(0.5, '#1e90ff') // 青蓝色海
      gradient.addColorStop(1, '#f4a460') // 沙滩色
      ctx.fillStyle = gradient
    } else {
      // 默认场景 - 柔和的天空
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
      gradient.addColorStop(0, '#87ceeb') // 天空蓝
      gradient.addColorStop(1, '#98fb98') // 柔和绿
      ctx.fillStyle = gradient
    }
  } else {
    // 默认背景
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
    gradient.addColorStop(0, '#87ceeb') // 天空蓝
    gradient.addColorStop(1, '#98fb98') // 柔和绿
    ctx.fillStyle = gradient
  }
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  // 添加像素艺术细节（如云朵、远山等）
  drawPixelDetails(currentScene);
}

// 绘制像素细节

// 绘制像素细节
function drawPixelDetails(currentScene) {
  // 根据场景类型添加不同的装饰元素
  if (currentScene && currentScene.backgroundDescription.toLowerCase().includes('夜晚')) {
    // 绘制星星
    ctx.fillStyle = 'white'
    for (let i = 0; i < 50; i++) {
      const x = Math.random() * canvas.width
      const y = Math.random() * (canvas.height * 0.4) // 上半部分
      ctx.fillRect(x, y, 1, 1)
    }
    // 绘制月亮
    ctx.fillStyle = '#f5f5dc' // 米色
    ctx.beginPath()
    ctx.arc(canvas.width - 80, 60, 30, 0, Math.PI * 2)
    ctx.fill()
  } else if (currentScene && currentScene.backgroundDescription.toLowerCase().includes('森林')) {
    // 绘制远山
    ctx.fillStyle = '#5a7d5d' // 深森林绿
    for (let i = 0; i < 5; i++) {
      const x = i * 150
      const height = 80 + Math.random() * 40
      ctx.beginPath()
      ctx.moveTo(x, canvas.height - 50)
      ctx.lineTo(x + 75, canvas.height - 50 - height)
      ctx.lineTo(x + 150, canvas.height - 50)
      ctx.closePath()
      ctx.fill()
    }
  }
}

// 绘制地形
function drawTerrain(currentScene) {
  // 绘制地面层
  ctx.fillStyle = '#8B4513' // 棕色地面
  ctx.fillRect(0, canvas.height - 50, canvas.width, 50)
  
  // 绘制草地区域
  ctx.fillStyle = '#2E8B57' // 绿色草
  ctx.fillRect(0, canvas.height - 50, canvas.width, 20)
  
  // 添加一些静态像素草丛效果（移除随机性以避免视觉滚动效果）
  ctx.fillStyle = '#3CB371' // 中海绿色
  // 使用固定的种子而不是随机数，这样每次渲染都是一样的
  for (let x = 0; x < canvas.width; x += 10) {
    // 使用一个可预测的模式代替随机数
    const seed = (x * 97) % 100; // 使用质数97来产生伪随机分布
    if (seed > 30) { // 相当于原来的 > 0.3
      const height = 5 + (seed % 10); // 高度也是确定性的
      ctx.fillRect(x, canvas.height - 50, 3, -height)
    }
  }
}

// 绘制互动元素
function drawInteractiveElement(element) {
  // 根据元素类型绘制不同的像素艺术风格
  switch (element.type) {
    case 'npc':
      drawPixelNPC(element)
      break
    case 'item':
      drawPixelItem(element)
      break
    case 'building':
      drawPixelBuilding(element)
      break
    case 'quest_npc':
      drawPixelQuestNPC(element)
      break
    default:
      drawPixelGenericElement(element)
      break
  }
}

// 绘制像素NPC
function drawPixelNPC(element) {
  const [x, y] = element.position
  
  // 如果元素有预设的精灵图片，优先使用
  if (element.sprite) {
    const img = new Image();
    img.src = element.sprite;
    
    img.onload = () => {
      // 计算缩放比例以适应角色大小
      const targetSize = 32; // 目标角色大小
      const scale = targetSize / Math.max(img.width, img.height);
      
      // 绘制精灵图片
      ctx.drawImage(img, x - (img.width * scale) / 2, y - (img.height * scale), 
                 img.width * scale, img.height * scale);
    };
    
    // 如果图片未加载完成，绘制备用图形
    drawFallbackNPC(element);
  } else if (element.characterSprite) {
    // 如果没有sprite但有characterSprite（如NPC），使用characterSprite
    const img = new Image();
    img.src = element.characterSprite;
    
    img.onload = () => {
      // 计算缩放比例以适应角色大小
      const targetSize = 32; // 目标角色大小
      const scale = targetSize / Math.max(img.width, img.height);
      
      // 绘制精灵图片
      ctx.drawImage(img, x - (img.width * scale) / 2, y - (img.height * scale), 
                 img.width * scale, img.height * scale);
    };
    
    // 如果图片未加载完成，绘制备用图形
    drawFallbackNPC(element);
  } else {
    // 如果没有预设精灵，使用原有绘制方式
    drawFallbackNPC(element);
  }
}

// 备用的NPC绘制
function drawFallbackNPC(element) {
  const [x, y] = element.position
  // 绘制NPC身体（更精美的像素风格）
  // 衣服颜色可以根据元素属性变化
  ctx.fillStyle = element.color || '#FF69B4' // 粉色身体，默认为粉色
  ctx.fillRect(x - 8, y - 15, 16, 15) // 身体
  
  // 添加衣服细节
  ctx.fillStyle = '#CC5577' // 深粉色
  ctx.fillRect(x - 6, y - 15, 12, 3) // 衣领
  
  // 绘制头部
  ctx.fillStyle = '#FFDBAC' // 肤色
  ctx.fillRect(x - 6, y - 25, 12, 10) // 头部
  
  // 绘制头发
  ctx.fillStyle = element.hairColor || '#333333' // 默认黑色头发
  ctx.fillRect(x - 7, y - 26, 14, 4) // 头发
  
  // 绘制眼睛
  ctx.fillStyle = element.eyeColor || '#000' // 眼睛颜色，默认黑色
  ctx.fillRect(x - 4, y - 23, 2, 2) // 左眼
  ctx.fillRect(x + 2, y - 23, 2, 2) // 右眼
  
  // 绘制瞳孔
  ctx.fillStyle = '#FFF'
  ctx.fillRect(x - 3, y - 22, 1, 1) // 左瞳孔
  ctx.fillRect(x + 3, y - 22, 1, 1) // 右瞳孔
  
  // 绘制嘴巴
  ctx.fillStyle = '#8B4513' // 嘴巴颜色
  ctx.fillRect(x - 1, y - 20, 2, 1) // 微笑嘴
  
  // 绘制名字标签
  drawPixelLabel(element.name, x, y - 30)
}

// 绘制像素任务NPC
function drawPixelQuestNPC(element) {
  const [x, y] = element.position
  // 绘制带感叹号的NPC
  drawPixelNPC(element)
  
  // 绘制感叹号标识
  ctx.fillStyle = '#FFFF00' // 黄色
  ctx.fillRect(x, y - 40, 6, 6) // 感叹号点
  ctx.fillRect(x, y - 48, 6, 6) // 感叹号点
}

// 绘制像素物品
function drawPixelItem(element) {
  const [x, y] = element.position
  
  // 如果元素有预设的精灵图片，优先使用
  if (element.sprite) {
    const img = new Image();
    img.src = element.sprite;
    
    img.onload = () => {
      // 计算缩放比例以适应物品大小
      const targetSize = 24; // 目标物品大小
      const scale = targetSize / Math.max(img.width, img.height);
      
      // 绘制精灵图片
      ctx.drawImage(img, x - (img.width * scale) / 2, y - (img.height * scale), 
                 img.width * scale, img.height * scale);
    };
    
    // 如果图片未加载完成，绘制备用图形
    drawFallbackItem(element);
  } else {
    // 如果没有预设精灵，使用原有绘制方式
    drawFallbackItem(element);
  }
}

// 备用的物品绘制
function drawFallbackItem(element) {
  const [x, y] = element.position
  // 绘制宝箱或其他物品（更精美的像素风格）
  // 物品类型决定外观
  if (element.itemType === 'treasure' || element.name.toLowerCase().includes('宝箱') || element.name.toLowerCase().includes('chest')) {
    // 绘制宝箱
    ctx.fillStyle = '#CD7F32' // 铜色
    ctx.fillRect(x - 10, y - 10, 20, 15) // 宝箱主体
    
    // 宝箱盖子
    ctx.fillStyle = '#A52A2A' // 棕色
    ctx.fillRect(x - 10, y - 15, 20, 5) // 盖子
    
    // 宝箱装饰
    ctx.fillStyle = '#FFD700' // 金色装饰
    ctx.fillRect(x - 2, y - 12, 4, 4) // 中央装饰
  } else if (element.itemType === 'key' || element.name.toLowerCase().includes('钥匙') || element.name.toLowerCase().includes('key')) {
    // 绘制钥匙
    ctx.fillStyle = '#FFD700' // 金色
    ctx.fillRect(x - 8, y - 5, 16, 3) // 钥匙柄
    ctx.fillRect(x + 6, y - 8, 3, 6) // 钥匙齿
  } else if (element.itemType === 'book' || element.name.toLowerCase().includes('书') || element.name.toLowerCase().includes('book')) {
    // 绘制书本
    ctx.fillStyle = '#8B4513' // 棕色书皮
    ctx.fillRect(x - 8, y - 12, 16, 12) // 书本主体
    ctx.fillStyle = '#FFFFFF' // 白色页面
    ctx.fillRect(x - 6, y - 10, 12, 8) // 页面
  } else {
    // 默认物品
    ctx.fillStyle = element.color || '#CD7F32' // 默认铜色
    ctx.fillRect(x - 10, y - 10, 20, 15) // 物品主体
    
    // 添加装饰
    ctx.fillStyle = element.accentColor || '#A52A2A' // 默认棕色装饰
    ctx.fillRect(x - 2, y - 8, 4, 4) // 中央装饰
  }
  
  // 绘制名字标签
  drawPixelLabel(element.name, x, y - 20)
}

// 绘制像素建筑
function drawPixelBuilding(element) {
  const [x, y] = element.position
  // 绘制建筑（更精美的像素风格）
  // 根据建筑类型决定外观
  if (element.buildingType === 'house' || element.name.toLowerCase().includes('房屋') || element.name.toLowerCase().includes('home')) {
    // 绘制房屋
    ctx.fillStyle = '#A52A2A' // 棕色房子
    ctx.fillRect(x - 20, y - 30, 40, 30) // 房子主体
    
    // 屋顶
    ctx.fillStyle = '#800000' // 深红屋顶
    ctx.beginPath()
    ctx.moveTo(x - 25, y - 30) // 左顶点
    ctx.lineTo(x + 25, y - 30) // 右顶点
    ctx.lineTo(x, y - 50)      // 屋顶尖
    ctx.closePath()
    ctx.fill()
    
    // 门
    ctx.fillStyle = '#5D4037' // 门的颜色
    ctx.fillRect(x - 5, y - 10, 10, 10) // 门
    
    // 窗户
    ctx.fillStyle = '#87CEEB' // 天蓝色窗户
    ctx.fillRect(x - 12, y - 20, 8, 8) // 左窗
    ctx.fillRect(x + 4, y - 20, 8, 8) // 右窗
  } else if (element.buildingType === 'tower' || element.name.toLowerCase().includes('塔') || element.name.toLowerCase().includes('tower')) {
    // 绘制塔
    ctx.fillStyle = '#708090' // 石灰色
    ctx.fillRect(x - 8, y - 60, 16, 60) // 塔身
    
    // 塔尖
    ctx.fillStyle = '#C0C0C0' // 银色
    ctx.beginPath()
    ctx.moveTo(x - 12, y - 60) // 左顶点
    ctx.lineTo(x + 12, y - 60) // 右顶点
    ctx.lineTo(x, y - 75)      // 塔顶尖
    ctx.closePath()
    ctx.fill()
  } else if (element.buildingType === 'castle' || element.name.toLowerCase().includes('城堡') || element.name.toLowerCase().includes('castle')) {
    // 绘制城堡
    ctx.fillStyle = '#B8860B' // 深金色
    ctx.fillRect(x - 30, y - 40, 60, 40) // 城堡主体
    
    // 城堡塔楼
    ctx.fillRect(x - 35, y - 60, 15, 60) // 左塔
    ctx.fillRect(x + 20, y - 60, 15, 60) // 右塔
    
    // 城堡旗子
    ctx.fillStyle = '#DC143C' // 鲜红色
    ctx.fillRect(x + 25, y - 75, 10, 5) // 右塔旗子
    ctx.fillRect(x - 30, y - 75, 10, 5) // 左塔旗子
    
    // 城堡门
    ctx.fillStyle = '#5D4037' // 木门色
    ctx.fillRect(x - 8, y - 10, 16, 10) // 城堡门
  } else {
    // 默认建筑
    ctx.fillStyle = element.color || '#A52A2A' // 默认棕色
    ctx.fillRect(x - 20, y - 30, 40, 30) // 建筑主体
    
    // 默认屋顶
    ctx.fillStyle = element.roofColor || '#800000' // 默认深红
    ctx.beginPath()
    ctx.moveTo(x - 25, y - 30) // 左顶点
    ctx.lineTo(x + 25, y - 30) // 右顶点
    ctx.lineTo(x, y - 50)      // 屋顶尖
    ctx.closePath()
    ctx.fill()
    
    // 默认门
    ctx.fillStyle = '#5D4037' // 门的颜色
    ctx.fillRect(x - 5, y - 10, 10, 10) // 门
  }
  
  // 绘制名字标签
  drawPixelLabel(element.name, x, y - 80)
}

// 绘制通用像素元素
function drawPixelGenericElement(element) {
  const [x, y] = element.position
  // 绘制一个通用像素块
  ctx.fillStyle = '#8A2BE2' // 紫色
  ctx.fillRect(x - 8, y - 8, 16, 16)
  
  // 绘制名字标签
  drawPixelLabel(element.name, x, y - 18)
}

// 绘制像素标签
function drawPixelLabel(text, x, y) {
  // 绘制标签背景
  ctx.fillStyle = 'rgba(0, 0, 0, 0.7)'
  const textWidth = ctx.measureText(text).width
  ctx.fillRect(x - textWidth/2 - 5, y - 15, textWidth + 10, 15)
  
  // 绘制文字
  ctx.fillStyle = '#FFFFFF'
  ctx.font = '12px monospace' // 使用等宽字体以获得更好的像素效果
  ctx.textAlign = 'center'
  ctx.fillText(text, x, y - 5)
}

// 绘制场景标签
function drawSceneLabel(sceneName) {
  // 绘制场景名称标签
  ctx.fillStyle = 'rgba(0, 0, 0, 0.6)'
  const textWidth = ctx.measureText(sceneName).width
  ctx.fillRect(20, 20, textWidth + 20, 30)
  
  ctx.fillStyle = '#FFFFFF'
  ctx.font = 'bold 16px monospace'
  ctx.textAlign = 'left'
  ctx.fillText(sceneName, 30, 42)
}

// 绘制玩家
function drawPlayer() {
  if (!gameState) return
  
  const { x, y } = gameState.playerPosition
  
  // 如果游戏数据中有玩家精灵，优先使用
  if (gameData.playerSprite) {
    const img = new Image();
    img.src = gameData.playerSprite;
    
    img.onload = () => {
      // 计算缩放比例以适应角色大小
      const targetSize = 32; // 目标角色大小
      const scale = targetSize / Math.max(img.width, img.height);
      
      // 绘制精灵图片
      ctx.drawImage(img, x - (img.width * scale) / 2, y - (img.height * scale), 
                 img.width * scale, img.height * scale);
      
      // 绘制方向指示
      drawPlayerDirectionIndicator(x, y);
    };
    
    // 如果图片未加载完成，绘制备用图形
    drawFallbackPlayer();
  } else {
    // 如果没有预设精灵，使用原有绘制方式
    drawFallbackPlayer();
  }
}

// 绘制玩家方向指示
function drawPlayerDirectionIndicator(x, y) {
  // 绘制方向指示（像素箭头）
  ctx.fillStyle = '#FFFF00' // 黄色方向指示
  switch (gameState.playerDirection) {
    case 'up':
      ctx.fillRect(x - 2, y - 30, 4, 6) // 上箭头
      ctx.fillRect(x - 1, y - 32, 2, 4) // 箭头顶
      break
    case 'down':
      ctx.fillRect(x - 2, y - 5, 4, 6) // 下箭头
      ctx.fillRect(x - 1, y + 7, 2, 4) // 箭头底
      break
    case 'left':
      ctx.fillRect(x - 15, y - 2, 6, 4) // 左箭头
      ctx.fillRect(x - 17, y - 1, 4, 2) // 箭头左
      break
    case 'right':
      ctx.fillRect(x + 9, y - 2, 6, 4) // 右箭头
      ctx.fillRect(x + 13, y - 1, 4, 2) // 箭头右
      break
  }
}

// 备用的玩家绘制
function drawFallbackPlayer() {
  if (!gameState) return
  
  const { x, y } = gameState.playerPosition
  
  // 绘制玩家身体（更精美的像素风格）
  ctx.fillStyle = '#4169E1' // 皇家蓝衣服
  ctx.fillRect(x - 8, y - 15, 16, 15) // 身体
  
  // 添加衣服细节
  ctx.fillStyle = '#1E3A8A' // 深蓝色
  ctx.fillRect(x - 6, y - 15, 12, 3) // 衣领
  
  // 绘制头部
  ctx.fillStyle = '#FFDBAC' // 肤色
  ctx.fillRect(x - 6, y - 25, 12, 10) // 头部
  
  // 绘制头发
  ctx.fillStyle = '#333333' // 黑色头发
  ctx.fillRect(x - 7, y - 26, 14, 4) // 头发
  
  // 绘制眼睛
  ctx.fillStyle = '#000'
  ctx.fillRect(x - 4, y - 23, 2, 2) // 左眼
  ctx.fillRect(x + 2, y - 23, 2, 2) // 右眼
  
  // 绘制瞳孔
  ctx.fillStyle = '#FFF'
  ctx.fillRect(x - 3, y - 22, 1, 1) // 左瞳孔
  ctx.fillRect(x + 3, y - 22, 1, 1) // 右瞳孔
  
  // 绘制嘴巴
  ctx.fillStyle = '#8B4513' // 嘴巴颜色
  ctx.fillRect(x - 1, y - 20, 2, 1) // 微笑嘴
  
  // 绘制方向指示（像素箭头）
  ctx.fillStyle = '#FFFF00' // 黄色方向指示
  switch (gameState.playerDirection) {
    case 'up':
      ctx.fillRect(x - 2, y - 30, 4, 6) // 上箭头
      ctx.fillRect(x - 1, y - 32, 2, 4) // 箭头顶
      break
    case 'down':
      ctx.fillRect(x - 2, y - 5, 4, 6) // 下箭头
      ctx.fillRect(x - 1, y + 7, 2, 4) // 箭头底
      break
    case 'left':
      ctx.fillRect(x - 15, y - 2, 6, 4) // 左箭头
      ctx.fillRect(x - 17, y - 1, 4, 2) // 箭头左
      break
    case 'right':
      ctx.fillRect(x + 9, y - 2, 6, 4) // 右箭头
      ctx.fillRect(x + 13, y - 1, 4, 2) // 箭头右
      break
  }
}

// 绘制对话框
function drawDialogueBox() {
  if (!gameState || !gameState.showDialogue) return
  
  // 对话框背景 - 确保不超出画布边界
  const dialogueBoxHeight = 80;
  const dialogueBoxY = Math.max(50, canvas.height - 120);
  // 确保对话框不超出画布上边界
  const finalDialogueBoxY = Math.min(dialogueBoxY, canvas.height - dialogueBoxHeight - 20);
  ctx.fillStyle = 'rgba(255, 255, 255, 0.9)'
  ctx.fillRect(50, finalDialogueBoxY, canvas.width - 100, dialogueBoxHeight)
  
  // 对话框边框
  ctx.strokeStyle = '#E9A33B'
  ctx.lineWidth = 2
  ctx.strokeRect(50, finalDialogueBoxY, canvas.width - 100, dialogueBoxHeight)
  
  // 对话文本
  ctx.fillStyle = '#000'
  ctx.font = '14px Arial'
  ctx.textAlign = 'left'
  
  // 自动换行处理
  const maxWidth = canvas.width - 120
  const lineHeight = 18
  let x = 70
  let y = finalDialogueBoxY + 25 // 从对话框顶部偏移开始绘制文本
  
  const words = gameState.dialogueText.split(' ')
  let line = ''
  
  for (let n = 0; n < words.length; n++) {
    const testLine = line + words[n] + ' '
    const metrics = ctx.measureText(testLine)
    const testWidth = metrics.width
    
    if (testWidth > maxWidth && n > 0) {
      // 确保文本不会超出对话框底部
      if (y + lineHeight <= finalDialogueBoxY + dialogueBoxHeight - 10) {
        ctx.fillText(line, x, y)
        line = words[n] + ' '
        y += lineHeight
      } else {
        // 如果超出对话框，则截断文本
        ctx.fillText(line + '...', x, y)
        break
      }
    } else {
      line = testLine
    }
  }
  // 绘制最后一行，如果还有剩余空间
  if (y + lineHeight <= finalDialogueBoxY + dialogueBoxHeight - 10 && line.trim() !== '') {
    ctx.fillText(line, x, y)
  }
}

// 键盘事件处理
function handleKeyDown(event) {
  if (!gameState) return
  
  switch (event.key) {
    case 'ArrowUp':
    case 'w':
      event.preventDefault()
      gameState.playerPosition.y -= 5
      gameState.playerDirection = 'up'
      break
    case 'ArrowDown':
    case 's':
      event.preventDefault()
      gameState.playerPosition.y += 5
      gameState.playerDirection = 'down'
      break
    case 'ArrowLeft':
    case 'a':
      event.preventDefault()
      gameState.playerPosition.x -= 5
      gameState.playerDirection = 'left'
      break
    case 'ArrowRight':
    case 'd':
      event.preventDefault()
      gameState.playerPosition.x += 5
      gameState.playerDirection = 'right'
      break
    case ' ':
      event.preventDefault()
      // 尝试与附近NPC对话
      tryInteractWithNpc()
      break
    case 'e':
      event.preventDefault()
      // 尝试与附近物品交互
      tryInteractWithItem()
      break
    case 'Escape':
      event.preventDefault()
      togglePause()
      break
  }
}

function handleKeyUp(event) {
  // 处理按键释放事件
}

function handleMouseDown(event) {
  // 处理鼠标按下事件
}

function handleMouseUp(event) {
  // 处理鼠标释放事件
}

function handleMouseMove(event) {
  // 处理鼠标移动事件
}

function focusCanvas() {
  if (gameCanvasRef.value) {
    gameCanvasRef.value.focus()
  }
}

// 与NPC交互
function tryInteractWithNpc() {
  if (!gameData || !gameState) return
  
  const currentScene = gameData.scenes.find(s => s.id === gameState.currentSceneId)
  if (!currentScene) return
  
  // 查找附近的NPC
  for (const element of currentScene.interactiveElements) {
    if (element.type === 'npc') {
      const distance = Math.sqrt(
        Math.pow(element.position[0] - gameState.playerPosition.x, 2) +
        Math.pow(element.position[1] - gameState.playerPosition.y, 2)
      )
      
      if (distance < 30) { // 交互距离
        gameState.showDialogue = true
        
        // 尝试获取NPC的对话，如果没有则使用描述
        if (element.dialogue && element.dialogue.length > 0) {
          // 如果有多个对话，随机选择一个
          const randomIndex = Math.floor(Math.random() * element.dialogue.length)
          gameState.dialogueText = element.dialogue[randomIndex]
        } else {
          gameState.dialogueText = element.description || '你好！'
        }
        return
      }
    }
  }
  
  // 如果没有找到NPC，关闭对话
  gameState.showDialogue = false
}

// 与物品交互
function tryInteractWithItem() {
  if (!gameData || !gameState) return
  
  const currentScene = gameData.scenes.find(s => s.id === gameState.currentSceneId)
  if (!currentScene) return
  
  // 查找附近的物品
  for (let i = 0; i < currentScene.interactiveElements.length; i++) {
    const element = currentScene.interactiveElements[i]
    if (element.type === 'item') {
      const distance = Math.sqrt(
        Math.pow(element.position[0] - gameState.playerPosition.x, 2) +
        Math.pow(element.position[1] - gameState.playerPosition.y, 2)
      )
      
      if (distance < 20) { // 交互距离
        // 添加到收集物品列表
        gameState.collectedItems.push(element.name)
        
        // 从场景中移除物品
        currentScene.interactiveElements.splice(i, 1)
        
        // 显示获得物品的消息
        gameState.showDialogue = true
        gameState.dialogueText = `获得了: ${element.name}`
        return
      }
    }
  }
  
  // 如果没有找到物品，关闭对话
  gameState.showDialogue = false
}

// 返回编辑器
async function goBackToEditor() {
  try {
    await ElMessageBox.confirm(
      '确定要返回编辑器吗？未保存的更改可能会丢失。',
      '返回编辑器',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 获取当前游戏ID并跳转到可视化编辑器
    const gameId = route.query.gameId
    if (gameId) {
      router.push(`/visual-editor?gameId=${gameId}`)
    } else {
      // 如果没有游戏ID，返回到普通的可视化编辑器
      router.push('/visual-editor')
    }
  } catch {
    // 用户取消操作
  }
}

// 导出游戏
async function exportGame() {
  exporting.value = true
  showExportDialog.value = true
  exportProgress.value = 0
  exportStatus.value = '正在准备导出...'
  
  // 模拟导出进度
  const interval = setInterval(() => {
    exportProgress.value += Math.floor(Math.random() * 10) + 1
    if (exportProgress.value >= 100) {
      exportProgress.value = 100
      exportStatus.value = '导出完成！'
      clearInterval(interval)
      
      // 完成后延迟关闭对话框
      setTimeout(() => {
        showExportDialog.value = false
        exporting.value = false
        
        // 这里可以触发实际的下载
        ElMessage.success('游戏导出成功！')
      }, 1000)
    }
  }, 200)
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

// 重置游戏
function resetGame() {
  ElMessageBox.confirm(
    '确定要重置游戏吗？这将恢复到初始状态。',
    '重置游戏',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // 重新初始化游戏状态
    initializeGame()
    ElMessage.success('游戏已重置')
  }).catch(() => {
    // 用户取消操作
  })
}
</script>

<style scoped>
.game-preview-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #020817;
  color: #fff;
  overflow: hidden; /* 防止出现滚动条 */
}

.game-area {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  overflow: hidden; /* 防止出现滚动条 */
}

#game-canvas {
  border: 2px solid #E9A33B;
  background-color: #87CEEB;
  outline: none;
  max-width: 100%;
  max-height: 100%;
  display: block; /* 防止canvas底部出现多余空间 */
}

.control-panel {
  padding: 15px 20px;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #E9A33B;
}

.export-content {
  text-align: center;
}

.export-content p {
  margin-top: 15px;
  font-size: 14px;
  color: #666;
}
</style>