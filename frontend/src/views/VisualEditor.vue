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
        <!-- 左侧游戏结构树 -->
        <el-aside width="300px" class="editor-sidebar">
          <el-tabs v-model="activeTab" class="sidebar-tabs">
            <el-tab-pane label="场景" name="scenes">
              <div class="structure-tree">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="addScene"
                  style="margin-bottom: 10px;"
                >
                  + 新增场景
                </el-button>
                <el-tree
                  :data="gameData.scenes"
                  :props="treeProps.scenes"
                  @node-click="handleSceneClick"
                  node-key="id"
                  :expand-on-click-node="false"
                  :default-expand-all="true"
                >
                  <template #default="{ node, data }">
                    <span class="custom-tree-node">
                      <span>{{ data.name }}</span>
                      <span>
                        <el-button
                          type="text"
                          size="small"
                          @click="() => removeScene(node, data)"
                        >
                          删除
                        </el-button>
                      </span>
                    </span>
                  </template>
                </el-tree>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="角色" name="characters">
              <div class="structure-tree">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="addCharacter"
                  style="margin-bottom: 10px;"
                >
                  + 新增角色
                </el-button>
                <el-tree
                  :data="gameData.characters"
                  :props="treeProps.characters"
                  @node-click="handleCharacterClick"
                  node-key="id"
                  :expand-on-click-node="false"
                  :default-expand-all="true"
                >
                  <template #default="{ node, data }">
                    <span class="custom-tree-node">
                      <span>{{ data.name }}</span>
                      <span>
                        <el-button
                          type="text"
                          size="small"
                          @click="() => removeCharacter(node, data)"
                        >
                          删除
                        </el-button>
                      </span>
                    </span>
                  </template>
                </el-tree>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="任务线" name="missions">
              <div class="structure-tree">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="addMission"
                  style="margin-bottom: 10px;"
                >
                  + 新增任务
                </el-button>
                <el-tree
                  :data="gameData.missions"
                  :props="treeProps.missions"
                  @node-click="handleMissionClick"
                  node-key="id"
                  :expand-on-click-node="false"
                  :default-expand-all="true"
                >
                  <template #default="{ node, data }">
                    <span class="custom-tree-node">
                      <span>{{ data.name }}</span>
                      <span>
                        <el-button
                          type="text"
                          size="small"
                          @click="() => removeMission(node, data)"
                        >
                          删除
                        </el-button>
                      </span>
                    </span>
                  </template>
                </el-tree>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-aside>
        
        <!-- 中间可视化编辑区 -->
        <el-main class="editor-main">
          <div v-if="editingSection" class="editing-panel">
            <h3>{{ editingSectionTitle }}</h3>
            
            <!-- 场景编辑 -->
            <div v-if="editingSection === 'scene' && currentScene">
              <el-form :model="currentScene" label-position="top">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="场景名称">
                      <el-input v-model="currentScene.name" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="背景描述">
                      <el-input v-model="currentScene.backgroundDescription" />
                      <el-button 
                        type="info" 
                        size="small" 
                        @click="aiAssistScene"
                        :loading="aiLoading.scene"
                        style="margin-top: 5px;"
                      >
                        🤖 AI生成场景
                      </el-button>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-form-item label="可互动元素">
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click="addInteractiveElement(currentScene)"
                    style="margin-bottom: 10px;"
                  >
                    + 添加互动元素
                  </el-button>
                  <el-table :data="currentScene.interactiveElements" style="width: 100%">
                    <el-table-column prop="type" label="类型" width="100" />
                    <el-table-column prop="name" label="名称" width="120" />
                    <el-table-column label="位置" width="150">
                      <template #default="{ row }">
                        [{{ row.position[0] }}, {{ row.position[1] }}]
                        <el-button 
                          type="text" 
                          size="small"
                          @click="editPosition(row)"
                        >
                          编辑
                        </el-button>
                      </template>
                    </el-table-column>
                    <el-table-column prop="description" label="描述" />
                    <el-table-column label="操作" width="100">
                      <template #default="{ row, $index }">
                        <el-button 
                          type="text" 
                          size="small"
                          @click="removeInteractiveElement(currentScene, $index)"
                        >
                          删除
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-form-item>
                
                <el-form-item label="场景跳转关系">
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click="addTransition(currentScene)"
                    style="margin-bottom: 10px;"
                  >
                    + 添加跳转关系
                  </el-button>
                  <el-table :data="currentScene.transitions" style="width: 100%">
                    <el-table-column prop="targetSceneId" label="目标场景" width="150" />
                    <el-table-column prop="condition" label="触发条件" width="120" />
                    <el-table-column prop="description" label="描述" />
                    <el-table-column label="操作" width="100">
                      <template #default="{ row, $index }">
                        <el-button 
                          type="text" 
                          size="small"
                          @click="removeTransition(currentScene, $index)"
                        >
                          删除
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-form-item>
              </el-form>
            </div>
            
            <!-- 角色编辑 -->
            <div v-if="editingSection === 'character' && currentCharacter">
              <el-form :model="currentCharacter" label-position="top">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="角色姓名">
                      <el-input v-model="currentCharacter.name" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="像素风形象">
                      <el-input v-model="currentCharacter.appearance" />
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="性格">
                      <el-input v-model="currentCharacter.personality" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="初始位置">
                      <el-input v-model="currentCharacter.initialPosition" />
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-form-item label="多段对话">
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click="addDialog(currentCharacter)"
                    style="margin-bottom: 10px;"
                  >
                    + 添加对话
                  </el-button>
                  <div class="dialogs-container">
                    <div 
                      v-for="(dialog, index) in currentCharacter.dialogues" 
                      :key="index" 
                      class="dialog-item"
                    >
                      <el-input 
                        v-model="currentCharacter.dialogues[index]" 
                        type="textarea"
                        :rows="2"
                        :placeholder="`对话 ${index + 1}`"
                      />
                      <div class="dialog-actions">
                        <el-button 
                          type="primary" 
                          size="mini" 
                          @click="moveDialogUp(currentCharacter, index)"
                          :disabled="index === 0"
                        >
                          ↑
                        </el-button>
                        <el-button 
                          type="primary" 
                          size="mini" 
                          @click="moveDialogDown(currentCharacter, index)"
                          :disabled="index === currentCharacter.dialogues.length - 1"
                        >
                          ↓
                        </el-button>
                        <el-button 
                          type="danger" 
                          size="mini" 
                          @click="removeDialog(currentCharacter, index)"
                        >
                          删除
                        </el-button>
                        <el-button 
                          type="info" 
                          size="mini" 
                          @click="aiAssistDialog(currentCharacter, index)"
                          :loading="aiLoading.dialog === index"
                        >
                          🤖 AI续写对话
                        </el-button>
                      </div>
                    </div>
                  </div>
                </el-form-item>
              </el-form>
            </div>
            
            <!-- 任务线编辑 -->
            <div v-if="editingSection === 'mission' && currentMission">
              <el-form :model="currentMission" label-position="top">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="任务名称">
                      <el-input v-model="currentMission.name" />
                      <el-button 
                        type="info" 
                        size="small" 
                        @click="aiAssistTask"
                        :loading="aiLoading.task"
                        style="margin-top: 5px;"
                      >
                        🤖 AI设计任务
                      </el-button>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="触发场景">
                      <el-select v-model="currentMission.triggerScene" placeholder="请选择触发场景" style="width: 100%;">
                        <el-option 
                          v-for="scene in gameData.scenes" 
                          :key="scene.id" 
                          :label="scene.name" 
                          :value="scene.id"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="触发条件">
                      <el-input v-model="currentMission.triggerCondition" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="完成条件">
                      <el-input v-model="currentMission.completionCondition" />
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-form-item label="对话内容">
                  <el-input 
                    v-model="currentMission.dialogueContent" 
                    type="textarea" 
                    :rows="3"
                    placeholder="任务相关的对话内容"
                  />
                </el-form-item>
                
                <el-form-item label="奖励">
                  <el-input v-model="currentMission.reward.xp" placeholder="经验奖励" style="width: 30%; margin-right: 10px;" />
                  <el-input v-model="currentMission.reward.items[0]" placeholder="物品奖励" style="width: 60%;" />
                </el-form-item>
                
                <el-form-item label="后续任务">
                  <el-select v-model="currentMission.nextMissionId" placeholder="无后续任务" style="width: 100%;">
                    <el-option label="无后续任务" :value="null" />
                    <el-option 
                      v-for="mission in gameData.missions.filter(m => m.id !== currentMission.id)" 
                      :key="mission.id" 
                      :label="mission.name" 
                      :value="mission.id"
                    />
                  </el-select>
                </el-form-item>
              </el-form>
            </div>
            
            <!-- 互动规则编辑 -->
            <div v-if="editingSection === 'rules'">
              <h4>角色移动设置</h4>
              <el-row :gutter="20">
                <el-col :span="6">
                  <el-form-item label="上">
                    <el-input v-model="gameData.interactionRules.movement.up" />
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="下">
                    <el-input v-model="gameData.interactionRules.movement.down" />
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="左">
                    <el-input v-model="gameData.interactionRules.movement.left" />
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="右">
                    <el-input v-model="gameData.interactionRules.movement.right" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <h4>对话触发设置</h4>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="触发距离">
                    <el-input-number 
                      v-model="gameData.interactionRules.dialogueTrigger.distance" 
                      :min="1" 
                      :max="100"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="触发按键">
                    <el-input v-model="gameData.interactionRules.dialogueTrigger.key" />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </div>
          
          <div v-else class="no-selection">
            <el-empty description="请选择左侧的项目进行编辑" />
          </div>
        </el-main>
        
        <!-- 右侧像素风预览区 -->
        <el-aside width="350px" class="preview-area">
          <h3>🎮 像素风预览</h3>
          <div class="pixel-preview-container">
            <div 
              v-if="currentScene" 
              class="pixel-scene"
              :style="{ backgroundColor: getSceneColor(currentScene.name) }"
            >
              <h4>{{ currentScene.name }}</h4>
              <p>{{ currentScene.backgroundDescription }}</p>
              
              <!-- 显示互动元素 -->
              <div 
                v-for="(element, index) in currentScene.interactiveElements" 
                :key="index"
                class="pixel-element"
                :style="{ left: element.position[0] + 'px', top: element.position[1] + 'px' }"
              >
                <div class="element-icon">{{ getElementIcon(element.type) }}</div>
                <div class="element-label">{{ element.name }}</div>
              </div>
              
              <!-- 简单的角色表示 -->
              <div class="pixel-character" style="left: 100px; top: 100px;">😊</div>
            </div>
            
            <div v-else class="no-scene-selected">
              <p>请选择一个场景进行预览</p>
            </div>
          </div>
        </el-aside>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../utils/request'

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
})

// 当前编辑项
const editingSection = ref('') // 'scene', 'character', 'mission', 'rules'
const editingSectionTitle = computed(() => {
  switch(editingSection.value) {
    case 'scene': return '场景编辑'
    case 'character': return '角色编辑'
    case 'mission': return '任务线编辑'
    case 'rules': return '互动规则设置'
    default: return '编辑面板'
  }
})

const currentScene = ref(null)
const currentCharacter = ref(null)
const currentMission = ref(null)

// AI加载状态
const aiLoading = ref({
  scene: false,
  dialog: null, // 对话索引
  task: false
})

// 树形控件配置
const treeProps = {
  scenes: {
    children: 'children',
    label: 'name'
  },
  characters: {
    children: 'children',
    label: 'name'
  },
  missions: {
    children: 'children',
    label: 'name'
  }
}

// 初始化数据
onMounted(async () => {
  const gameId = route.query.gameId || route.query.taskId
  if (gameId) {
    // 从本地存储获取生成的游戏数据
    const savedData = localStorage.getItem(`game_${gameId}`)
    if (savedData) {
      try {
        const parsedData = JSON.parse(savedData)
        gameData.value = parsedData
        ElMessage.success('游戏数据加载成功！')
      } catch (error) {
        console.error('解析游戏数据失败:', error)
        ElMessage.error('加载游戏数据失败')
      }
    } else {
      // 尝试从后端API获取数据
      try {
        const response = await request.get(`/game/${gameId}`)
        if (response.code === 200) {
          gameData.value = response.data
          ElMessage.success('游戏数据加载成功！')
        } else {
          throw new Error(response.msg || '获取游戏数据失败')
        }
      } catch (error) {
        console.error('获取游戏数据失败:', error)
        ElMessage.error('获取游戏数据失败')
        // 使用默认数据
        gameData.value = getDefaultGameData()
      }
    }
  } else {
    // 使用默认数据
    gameData.value = getDefaultGameData()
    ElMessage.info('已加载默认游戏数据')
  }
})

// 获取默认游戏数据
function getDefaultGameData() {
  return {
    gameId: 'default',
    gameName: '新像素风游戏',
    emotionalTone: '治愈',
    style: 'pixel_art',
    scenes: [
      {
        id: 'scene_start',
        name: '起点',
        backgroundDescription: '像素风格的宁静村庄',
        interactiveElements: [
          { type: 'npc', name: '向导', position: [50, 100], dialogue: ['欢迎来到这个世界！']},
          { type: 'item', name: '神秘宝箱', position: [200, 150], description: '似乎藏着重要物品'}
        ],
        transitions: [
          { targetSceneId: 'scene_forest', condition: 'start_game', description: '进入森林'}
        ]
      }
    ],
    characters: [
      {
        id: 'player',
        name: '玩家',
        appearance: '像素风格的冒险者',
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
        triggerCondition: '与向导对话',
        completionCondition: '了解基本操作',
        dialogueContent: '欢迎来到游戏世界！',
        reward: { xp: 50, items: ['铜币'] },
        nextMissionId: null
      }
    ],
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
}

// 处理场景点击
function handleSceneClick(data) {
  currentScene.value = data
  currentCharacter.value = null
  currentMission.value = null
  editingSection.value = 'scene'
}

// 处理角色点击
function handleCharacterClick(data) {
  currentCharacter.value = data
  currentScene.value = null
  currentMission.value = null
  editingSection.value = 'character'
}

// 处理任务点击
function handleMissionClick(data) {
  currentMission.value = data
  currentScene.value = null
  currentCharacter.value = null
  editingSection.value = 'mission'
}

// 添加场景
function addScene() {
  const newScene = {
    id: `scene_${Date.now()}`,
    name: `新场景 ${gameData.value.scenes.length + 1}`,
    backgroundDescription: '像素风格的新场景',
    interactiveElements: [],
    transitions: []
  }
  gameData.value.scenes.push(newScene)
  handleSceneClick(newScene)
}

// 删除场景
function removeScene(node, data) {
  ElMessageBox.confirm(
    `确定要删除场景 "${data.name}" 吗？`,
    '删除场景',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    const index = gameData.value.scenes.findIndex(s => s.id === data.id)
    if (index > -1) {
      gameData.value.scenes.splice(index, 1)
      if (currentScene.value && currentScene.value.id === data.id) {
        currentScene.value = null
        editingSection.value = ''
      }
    }
    ElMessage.success('场景已删除')
  }).catch(() => {
    // 取消删除
  })
}

// 添加角色
function addCharacter() {
  const newCharacter = {
    id: `char_${Date.now()}`,
    name: `新角色 ${gameData.value.characters.length + 1}`,
    appearance: '像素风角色',
    personality: '普通',
    initialPosition: 'scene_start',
    dialogues: ['你好！']
  }
  gameData.value.characters.push(newCharacter)
  handleCharacterClick(newCharacter)
}

// 删除角色
function removeCharacter(node, data) {
  ElMessageBox.confirm(
    `确定要删除角色 "${data.name}" 吗？`,
    '删除角色',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    const index = gameData.value.characters.findIndex(c => c.id === data.id)
    if (index > -1) {
      gameData.value.characters.splice(index, 1)
      if (currentCharacter.value && currentCharacter.value.id === data.id) {
        currentCharacter.value = null
        editingSection.value = ''
      }
    }
    ElMessage.success('角色已删除')
  }).catch(() => {
    // 取消删除
  })
}

// 添加任务
function addMission() {
  const newMission = {
    id: `mission_${Date.now()}`,
    name: `新任务 ${gameData.value.missions.length + 1}`,
    triggerScene: gameData.value.scenes[0]?.id || 'scene_start',
    triggerCondition: '与NPC对话',
    completionCondition: '完成目标',
    dialogueContent: '新的任务等待着你...',
    reward: { xp: 50, items: ['金币'] },
    nextMissionId: null
  }
  gameData.value.missions.push(newMission)
  handleMissionClick(newMission)
}

// 删除任务
function removeMission(node, data) {
  ElMessageBox.confirm(
    `确定要删除任务 "${data.name}" 吗？`,
    '删除任务',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    const index = gameData.value.missions.findIndex(m => m.id === data.id)
    if (index > -1) {
      gameData.value.missions.splice(index, 1)
      if (currentMission.value && currentMission.value.id === data.id) {
        currentMission.value = null
        editingSection.value = ''
      }
    }
    ElMessage.success('任务已删除')
  }).catch(() => {
    // 取消删除
  })
}

// 添加互动元素
function addInteractiveElement(scene) {
  scene.interactiveElements.push({
    type: 'npc',
    name: `新元素 ${scene.interactiveElements.length + 1}`,
    position: [100, 100],
    description: '新添加的互动元素',
    dialogue: ['你好！']
  })
}

// 删除互动元素
function removeInteractiveElement(scene, index) {
  scene.interactiveElements.splice(index, 1)
}

// 添加跳转关系
function addTransition(scene) {
  scene.transitions.push({
    targetSceneId: gameData.value.scenes[0]?.id || 'scene_start',
    condition: 'default',
    description: '跳转到另一个场景'
  })
}

// 删除跳转关系
function removeTransition(scene, index) {
  scene.transitions.splice(index, 1)
}

// 添加对话
function addDialog(character) {
  character.dialogues.push(`新对话 ${character.dialogues.length + 1}`)
}

// 移动对话上移
function moveDialogUp(character, index) {
  if (index > 0) {
    const temp = character.dialogues[index]
    character.dialogues[index] = character.dialogues[index - 1]
    character.dialogues[index - 1] = temp
  }
}

// 移动对话下移
function moveDialogDown(character, index) {
  if (index < character.dialogues.length - 1) {
    const temp = character.dialogues[index]
    character.dialogues[index] = character.dialogues[index + 1]
    character.dialogues[index + 1] = temp
  }
}

// 删除对话
function removeDialog(character, index) {
  if (character.dialogues.length > 1) {
    character.dialogues.splice(index, 1)
  } else {
    ElMessage.warning('至少需要保留一个对话')
  }
}

// 保存修改
async function saveChanges() {
  try {
    // 调用后端API保存修改
    const response = await request.post('/game/save', {
      gameId: gameData.value.gameId,
      gameData: gameData.value
    })
    
    if (response.code === 200) {
      // 同时保存到本地存储
      localStorage.setItem(`game_${gameData.value.gameId}`, JSON.stringify(gameData.value))
      ElMessage.success('修改已保存！')
    } else {
      throw new Error(response.msg || '保存失败')
    }
  } catch (error) {
    console.error('保存游戏数据失败:', error)
    ElMessage.error(error.message || '保存失败，请重试')
  }
}

// 预览游戏
function previewGame() {
  // 跳转到预览页面，携带游戏ID
  router.push(`/pixel-preview?id=${gameData.value.gameId}`)
}

// 返回原稿
function backToManuscript() {
  router.push('/manuscript-input')
}

// AI辅助功能
async function aiAssistScene() {
  if (!currentScene.value) return
  
  aiLoading.value.scene = true
  try {
    const response = await request.post('/ai/assist/scene', {
      content: currentScene.value.backgroundDescription,
      context: { 
        sceneName: currentScene.value.name,
        gameId: gameData.value.gameId 
      },
      params: { 
        style: gameData.value.style,
        emotion: gameData.value.emotionalTone
      }
    })
    
    if (response.code === 200) {
      currentScene.value.backgroundDescription = response.data.result
      ElMessage.success('AI辅助生成场景成功！')
    } else {
      throw new Error(response.msg || 'AI生成失败')
    }
  } catch (error) {
    console.error('AI辅助生成场景失败:', error)
    ElMessage.error(error.message || 'AI生成失败，请重试')
  } finally {
    aiLoading.value.scene = false
  }
}

async function aiAssistDialog(character, index) {
  if (!character) return
  
  aiLoading.value.dialog = index
  try {
    const response = await request.post('/ai/assist/dialog', {
      content: character.dialogues[index],
      context: { 
        characterName: character.name,
        gameId: gameData.value.gameId 
      },
      params: { 
        style: gameData.value.style,
        emotion: gameData.value.emotionalTone
      }
    })
    
    if (response.code === 200) {
      character.dialogues[index] = response.data.result
      ElMessage.success('AI辅助生成对话成功！')
    } else {
      throw new Error(response.msg || 'AI生成失败')
    }
  } catch (error) {
    console.error('AI辅助生成对话失败:', error)
    ElMessage.error(error.message || 'AI生成失败，请重试')
  } finally {
    aiLoading.value.dialog = null
  }
}

async function aiAssistTask() {
  if (!currentMission.value) return
  
  aiLoading.value.task = true
  try {
    const response = await request.post('/ai/assist/task', {
      content: currentMission.value.name,
      context: { 
        taskName: currentMission.value.name,
        gameId: gameData.value.gameId 
      },
      params: { 
        style: gameData.value.style,
        emotion: gameData.value.emotionalTone
      }
    })
    
    if (response.code === 200) {
      // 解析AI返回的任务信息并更新当前任务
      const result = response.data.result;
      // 这里应该解析返回的结果并适当更新任务属性
      // 为了简化，我们暂时只更新名称和描述
      currentMission.value.name = result.substring(0, result.indexOf('\n')) || currentMission.value.name;
      currentMission.value.dialogueContent = result;
      ElMessage.success('AI辅助设计任务成功！')
    } else {
      throw new Error(response.msg || 'AI生成失败')
    }
  } catch (error) {
    console.error('AI辅助设计任务失败:', error)
    ElMessage.error(error.message || 'AI生成失败，请重试')
  } finally {
    aiLoading.value.task = false
  }
}

// 辅助函数
function getSceneColor(sceneName) {
  const colors = ['#f0f9eb', '#e6f4ff', '#ffeef0', '#f6ffed', '#fff7e6']
  return colors[sceneName.charCodeAt(0) % colors.length]
}

function getElementIcon(type) {
  switch(type) {
    case 'npc': return '👤'
    case 'item': return '📦'
    case 'building': return '🏠'
    case 'quest_npc': return '👑'
    default: return '❓'
  }
}

function editPosition(row) {
  // 简单的位置编辑功能，实际应用中可能需要更复杂的界面
  const x = prompt('X坐标:', row.position[0])
  const y = prompt('Y坐标:', row.position[1])
  if (x !== null && y !== null) {
    row.position[0] = parseInt(x) || 0
    row.position[1] = parseInt(y) || 0
  }
}
</script>

<style scoped>
.visual-editor-container {
  height: calc(100vh - 60px);
  background-color: #2c3a47; /* 深蓝灰色背景 */
  color: #ecf0f1; /* 浅灰色文字 */
}

.editor-header {
  background-color: #34495e; /* 深蓝灰头部 */
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.editor-sidebar {
  background-color: #34495e; /* 深蓝灰侧边栏 */
  padding: 15px;
  border-right: 1px solid #4a6278; /* 深蓝灰边框 */
}

.sidebar-tabs {
  height: 100%;
}

.structure-tree {
  height: calc(100% - 40px);
  overflow-y: auto;
}

.custom-tree-node {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  padding-right: 8px;
}

.editor-main {
  background-color: #2c3a47; /* 深蓝灰主内容区 */
  padding: 20px;
  overflow-y: auto;
}

.editing-panel {
  background-color: #34495e; /* 深蓝灰编辑面板 */
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #4a6278; /* 深蓝灰边框 */
}

.no-selection {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.editing-panel h3 {
  color: white;
  margin-bottom: 20px;
  border-bottom: 1px solid #4a6278; /* 深蓝灰分割线 */
  padding-bottom: 10px;
}

.preview-area {
  background-color: #34495e; /* 深蓝灰预览区 */
  padding: 15px;
  border-left: 1px solid #4a6278; /* 深蓝灰边框 */
  color: white;
}

.pixel-preview-container {
  height: calc(100vh - 150px);
  overflow-y: auto;
  background-color: #2c3a47; /* 深蓝灰容器 */
  border-radius: 8px;
  padding: 10px;
}

.pixel-scene {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 300px;
  border: 1px solid #4a6278; /* 深蓝灰边框 */
  border-radius: 4px;
  padding: 10px;
  background-color: #3d566e; /* 较浅的深蓝灰背景 */
}

.pixel-scene h4 {
  color: white;
  margin-top: 0;
}

.pixel-scene p {
  color: #bdc3c7; /* 浅灰色文字 */
  font-size: 14px;
}

.pixel-element {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.element-icon {
  font-size: 24px;
}

.element-label {
  font-size: 12px;
  color: white;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 2px 4px;
  border-radius: 4px;
  margin-top: 2px;
}

.pixel-character {
  position: absolute;
  font-size: 32px;
}

.no-scene-selected {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #bdc3c7; /* 浅灰色文字 */
}

.dialog-item {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #3d566e; /* 较浅的深蓝灰背景 */
  border-radius: 4px;
  border: 1px solid #4a6278; /* 深蓝灰边框 */
}

.dialog-actions {
  margin-top: 8px;
  display: flex;
  gap: 5px;
  justify-content: flex-end;
}

/* 表格样式 */
:deep(.el-table) {
  background-color: #3d566e !important; /* 深蓝灰表格背景 */
  border: 1px solid #4a6278 !important; /* 深蓝灰边框 */
}

:deep(.el-table th),
:deep(.el-table td) {
  background-color: #3d566e !important; /* 深蓝灰单元格背景 */
  color: #ecf0f1 !important; /* 浅灰色文字 */
  border-color: #4a6278 !important; /* 深蓝灰边框 */
}

:deep(.el-table__header tr),
:deep(.el-table__body tr) {
  background-color: #3d566e !important; /* 深蓝灰行背景 */
}

:deep(.el-table__body tr:hover > td) {
  background-color: #4a6278 !important; /* 悬停行背景 */
}

/* 输入框样式 */
:deep(.el-input__wrapper),
:deep(.el-textarea__inner),
:deep(.el-select__wrapper) {
  background-color: #3d566e !important; /* 深蓝灰输入框背景 */
  border: 1px solid #4a6278 !important; /* 深蓝灰边框 */
  color: white !important; /* 白色输入文字 */
}

:deep(.el-input__inner),
:deep(.el-textarea__inner) {
  color: white !important;
}

/* 标签样式 */
:deep(.el-form-item__label) {
  color: #ecf0f1 !important; /* 浅灰色标签文字 */
  font-weight: bold;
}

/* 树形控件样式 */
:deep(.el-tree) {
  background-color: transparent !important;
}

:deep(.el-tree-node__content:hover) {
  background-color: #4a6278 !important; /* 悬停节点背景 */
}

:deep(.el-tree-node:focus) > .el-tree-node__content {
  background-color: #4a6278 !important; /* 选中节点背景 */
}

/* 卡片样式 */
:deep(.el-card__body) {
  background-color: #3d566e !important; /* 深蓝灰卡片背景 */
  color: white !important;
}

/* 空状态样式 */
:deep(.el-empty__description span) {
  color: #bdc3c7 !important; /* 浅灰色空状态文字 */
}

/* Tab标签页样式 */
:deep(.el-tabs__item) {
  color: #ecf0f1 !important; /* 浅灰色标签文字 */
}

:deep(.el-tabs__nav-wrap::after) {
  background-color: #4a6278 !important; /* 深蓝灰底部边框 */
}

/* 按钮样式 */
:deep(.el-button--primary) {
  --el-button-bg-color: #3498db !important; /* 主要按钮颜色 */
  --el-button-border-color: #3498db !important;
  --el-button-hover-bg-color: #2980b9 !important;
  --el-button-hover-border-color: #2980b9 !important;
  --el-button-active-bg-color: #2980b9 !important;
  --el-button-active-border-color: #2980b9 !important;
}

:deep(.el-button--success) {
  --el-button-bg-color: #2ecc71 !important; /* 成功按钮颜色 */
  --el-button-border-color: #2ecc71 !important;
  --el-button-hover-bg-color: #27ae60 !important;
  --el-button-hover-border-color: #27ae60 !important;
  --el-button-active-bg-color: #27ae60 !important;
  --el-button-active-border-color: #27ae60 !important;
}

:deep(.el-button--info) {
  --el-button-bg-color: #95a5a6 !important; /* 信息按钮颜色 */
  --el-button-border-color: #95a5a6 !important;
  --el-button-hover-bg-color: #7f8c8d !important;
  --el-button-hover-border-color: #7f8c8d !important;
  --el-button-active-bg-color: #7f8c8d !important;
  --el-button-active-border-color: #7f8c8d !important;
}

:deep(.el-button--danger) {
  --el-button-bg-color: #e74c3c !important; /* 危险按钮颜色 */
  --el-button-border-color: #e74c3c !important;
  --el-button-hover-bg-color: #c0392b !important;
  --el-button-hover-border-color: #c0392b !important;
  --el-button-active-bg-color: #c0392b !important;
  --el-button-active-border-color: #c0392b !important;
}

/* 数字输入框样式 */
:deep(.el-input-number) {
  background-color: #3d566e !important; /* 深蓝灰输入框背景 */
  border: 1px solid #4a6278 !important; /* 深蓝灰边框 */
  border-radius: 4px !important;
}

:deep(.el-input-number__decrease),
:deep(.el-input-number__increase) {
  background-color: #4a6278 !important; /* 按钮背景 */
  border: none !important;
  color: white !important;
}
</style>