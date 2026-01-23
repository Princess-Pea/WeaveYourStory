<template>
  <div class="visual-editor-container">
    <el-container>
      <el-header class="editor-header">
        <h2>🎨 像素风游戏可视化编辑器</h2>
        <div class="header-actions">
          <el-button type="primary" @click="saveChanges">💾 保存修改</el-button>
          <el-button type="success" @click="previewGame">👀 预览游戏</el-button>
          <el-button @click="backToManuscript">↩️ 返回原稿</el-button>
        </div>
      </el-header>
      
      <el-container>
        <el-aside width="300px" class="editor-sidebar">
          <el-tabs v-model="activeTab" class="sidebar-tabs">
            <el-tab-pane label="场景管理" name="scenes">
              <div class="scene-list">
                <el-card 
                  v-for="scene in gameData.scenes" 
                  :key="scene.id"
                  class="scene-item"
                  @click="selectScene(scene.id)"
                  :class="{ active: selectedSceneId === scene.id }"
                >
                  <div class="scene-info">
                    <h4>{{ scene.name }}</h4>
                    <p>{{ scene.backgroundDescription.substring(0, 30) }}...</p>
                  </div>
                </el-card>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="角色管理" name="characters">
              <div class="character-list">
                <el-card 
                  v-for="character in gameData.characters" 
                  :key="character.id"
                  class="character-item"
                >
                  <div class="character-info">
                    <h4>{{ character.name }}</h4>
                    <p>位置: {{ character.initialPosition }}</p>
                  </div>
                </el-card>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="任务管理" name="missions">
              <div class="mission-list">
                <el-card 
                  v-for="mission in gameData.missions" 
                  :key="mission.id"
                  class="mission-item"
                >
                  <div class="mission-info">
                    <h4>{{ mission.name }}</h4>
                    <p>触发场景: {{ mission.triggerScene }}</p>
                  </div>
                </el-card>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-aside>
        
        <el-main class="editor-main">
          <div v-if="selectedSceneId" class="scene-editor">
            <h3>编辑场景: {{ selectedScene.name }}</h3>
            
            <el-form :model="selectedScene" label-position="top">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="场景名称">
                    <el-input v-model="selectedScene.name" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="背景描述">
                    <el-input v-model="selectedScene.backgroundDescription" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item label="可互动元素">
                <el-table :data="selectedScene.interactiveElements" style="width: 100%">
                  <el-table-column prop="type" label="类型" width="100" />
                  <el-table-column prop="name" label="名称" width="120" />
                  <el-table-column prop="position" label="位置" width="150">
                    <template #default="{ row }">
                      [{{ row.position[0] }}, {{ row.position[1] }}]
                    </template>
                  </el-table-column>
                  <el-table-column prop="description" label="描述" />
                </el-table>
              </el-form-item>
              
              <el-form-item label="场景跳转关系">
                <el-table :data="selectedScene.transitions" style="width: 100%">
                  <el-table-column prop="targetSceneId" label="目标场景" width="150" />
                  <el-table-column prop="condition" label="触发条件" width="120" />
                  <el-table-column prop="description" label="描述" />
                </el-table>
              </el-form-item>
            </el-form>
          </div>
          
          <div v-else class="no-selection">
            <el-empty description="请选择左侧的场景进行编辑" />
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

// 编辑器状态
const activeTab = ref('scenes')
const gameData = ref({
  gameId: '',
  gameName: '未命名游戏',
  emotionalTone: 'neutral',
  style: 'pixel_art',
  scenes: [],
  characters: [],
  missions: [],
  interactionRules: {}
})
const selectedSceneId = ref('')
const selectedScene = ref(null)

// 初始化数据
onMounted(async () => {
  const taskId = route.query.taskId
  if (taskId) {
    // 从本地存储获取生成的游戏数据
    const savedData = localStorage.getItem(`game_${taskId}`)
    if (savedData) {
      try {
        const parsedData = JSON.parse(savedData)
        gameData.value = parsedData
        if (parsedData.scenes && parsedData.scenes.length > 0) {
          selectScene(parsedData.scenes[0].id)
        }
        ElMessage.success('游戏数据加载成功！')
      } catch (error) {
        console.error('解析游戏数据失败:', error)
        ElMessage.error('加载游戏数据失败')
      }
    } else {
      ElMessage.error('未找到对应的游戏数据')
      router.push('/manuscript-input')
    }
  } else {
    ElMessage.error('缺少任务ID参数')
    router.push('/manuscript-input')
  }
})

// 选择场景
const selectScene = (sceneId) => {
  selectedSceneId.value = sceneId
  selectedScene.value = gameData.value.scenes.find(s => s.id === sceneId)
}

// 保存修改
const saveChanges = () => {
  // 在实际实现中，这里会调用API保存修改
  ElMessage.success('修改已保存！')
  console.log('保存游戏数据:', gameData.value)
}

// 预览游戏
const previewGame = () => {
  // 跳转到预览页面，携带游戏ID
  router.push(`/pixel-preview?id=${gameData.value.gameId}`)
}

// 返回原稿
const backToManuscript = () => {
  router.push('/manuscript-input')
}
</script>

<style scoped>
.visual-editor-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #409EFF;
  color: white;
  padding: 0 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.editor-sidebar {
  background-color: #f5f5f5;
  padding: 15px;
  height: calc(100vh - 60px);
}

.sidebar-tabs {
  height: 100%;
}

.scene-item, .character-item, .mission-item {
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.scene-item:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.scene-item.active {
  border: 2px solid #409EFF;
  box-shadow: 0 4px 8px rgba(64, 158, 255, 0.3);
}

.scene-info h4, .character-info h4, .mission-info h4 {
  margin: 0 0 5px 0;
  color: #303133;
}

.scene-info p, .character-info p, .mission-info p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.editor-main {
  padding: 20px;
  background-color: #fafafa;
}

.scene-editor {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.no-selection {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

:deep(.el-table) {
  border-radius: 4px;
  overflow: hidden;
}
</style>