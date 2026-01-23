<template>
  <div class="manuscript-input-container">
    <h2>📝 结构化原稿输入</h2>
    <p>请按照模板填写游戏原稿，系统将根据您的输入生成像素风冒险游戏</p>

    <!-- 表单 -->
    <el-form 
      :model="form" 
      :rules="rules" 
      ref="formRef"
      label-position="top"
      class="manuscript-form"
    >
      <!-- 剧情核心模块 -->
      <el-card class="module-card">
        <template #header>
          <div class="card-header">
            <span>🎭 剧情核心</span>
          </div>
        </template>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="剧情名称" prop="storyTitle">
              <el-input 
                v-model="form.storyTitle" 
                placeholder="请输入剧情名称"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="情感基调" prop="emotionalTone">
              <el-select 
                v-model="form.emotionalTone" 
                placeholder="请选择情感基调"
                style="width: 100%"
              >
                <el-option 
                  v-for="tone in emotionalTones" 
                  :key="tone.value" 
                  :label="tone.label" 
                  :value="tone.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="故事大纲" prop="storyOutline">
          <el-input 
            v-model="form.storyOutline" 
            type="textarea" 
            :rows="4"
            placeholder="请描述故事的主要情节、转折点和发展方向"
          />
        </el-form-item>
        <el-form-item label="游戏背景" prop="gameBackground">
          <el-input 
            v-model="form.gameBackground" 
            type="textarea" 
            :rows="3"
            placeholder="请描述游戏的像素风场景，如'乡村小镇'、'赛博朋克小巷'等"
          />
        </el-form-item>
      </el-card>

      <!-- 任务线设计模块 -->
      <el-card class="module-card">
        <template #header>
          <div class="card-header">
            <span>🎯 任务线设计</span>
            <el-button 
              type="primary" 
              size="small" 
              @click="addMission"
            >
              + 添加任务
            </el-button>
          </div>
        </template>
        <div 
          v-for="(mission, index) in form.missions" 
          :key="index"
          class="mission-item"
        >
          <el-divider>
            任务 {{ index + 1 }}
            <el-button 
              type="danger" 
              size="small" 
              @click="removeMission(index)"
            >
              删除
            </el-button>
          </el-divider>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item 
                :prop="`missions.${index}.name`"
                :rules="{ required: true, message: '请输入任务名称', trigger: 'blur' }"
              >
                <template #label>
                  任务名称 <span class="required">*</span>
                </template>
                <el-input 
                  v-model="mission.name" 
                  placeholder="请输入任务名称"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item 
                :prop="`missions.${index}.triggerCondition`"
                :rules="{ required: true, message: '请输入触发条件', trigger: 'blur' }"
              >
                <template #label>
                  触发条件 <span class="required">*</span>
                </template>
                <el-input 
                  v-model="mission.triggerCondition" 
                  placeholder="如：到达村庄、与NPC对话"
                />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item 
                :prop="`missions.${index}.completionCondition`"
                :rules="{ required: true, message: '请输入完成条件', trigger: 'blur' }"
              >
                <template #label>
                  完成条件 <span class="required">*</span>
                </template>
                <el-input 
                  v-model="mission.completionCondition" 
                  placeholder="如：找到钥匙、击败敌人"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item 
                :prop="`missions.${index}.storyProgression`"
                :rules="{ required: true, message: '请输入剧情推进点', trigger: 'blur' }"
              >
                <template #label>
                  剧情推进点 <span class="required">*</span>
                </template>
                <el-input 
                  v-model="mission.storyProgression" 
                  placeholder="如：开启新区域、解锁新角色"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
      </el-card>

      <!-- 核心人物模块 -->
      <el-card class="module-card">
        <template #header>
          <div class="card-header">
            <span>👥 核心人物</span>
            <el-button 
              type="primary" 
              size="small" 
              @click="addCharacter"
            >
              + 添加角色
            </el-button>
          </div>
        </template>
        <div 
          v-for="(character, index) in form.characters" 
          :key="index"
          class="character-item"
        >
          <el-divider>
            角色 {{ index + 1 }}
            <el-button 
              type="danger" 
              size="small" 
              @click="removeCharacter(index)"
            >
              删除
            </el-button>
          </el-divider>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item 
                :prop="`characters.${index}.name`"
                :rules="{ required: true, message: '请输入角色姓名', trigger: 'blur' }"
              >
                <template #label>
                  姓名 <span class="required">*</span>
                </template>
                <el-input 
                  v-model="character.name" 
                  placeholder="请输入角色姓名"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item 
                :prop="`characters.${index}.personality`"
                :rules="{ required: true, message: '请输入角色性格', trigger: 'blur' }"
              >
                <template #label>
                  性格 <span class="required">*</span>
                </template>
                <el-input 
                  v-model="character.personality" 
                  placeholder="如：活泼开朗、沉默寡言"
                />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item 
                :prop="`characters.${index}.appearance`"
                :rules="{ required: true, message: '请输入形象设定', trigger: 'blur' }"
              >
                <template #label>
                  形象设定 <span class="required">*</span>
                </template>
                <el-input 
                  v-model="character.appearance" 
                  placeholder="如：短发女孩、黑猫NPC"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item 
                :prop="`characters.${index}.speechStyle`"
                :rules="{ required: true, message: '请输入台词风格', trigger: 'blur' }"
              >
                <template #label>
                  台词风格 <span class="required">*</span>
                </template>
                <el-input 
                  v-model="character.speechStyle" 
                  placeholder="如：古风、现代、幽默"
                />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item 
            :prop="`characters.${index}.relationships`"
            :rules="{ required: true, message: '请输入人物关系', trigger: 'blur' }"
          >
            <template #label>
              人物关系 <span class="required">*</span>
            </template>
            <el-input 
              v-model="character.relationships" 
              type="textarea" 
              :rows="2"
              placeholder="描述与其他角色的关系"
            />
          </el-form-item>
        </div>
      </el-card>

      <!-- 操作按钮 -->
      <div class="form-actions">
        <el-button 
          type="warning" 
          @click="saveDraft"
        >
          💾 暂存原稿
        </el-button>
        <el-button 
          type="primary" 
          @click="submitToAI"
          :loading="submitting"
        >
          🤖 提交AI生成
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import request from '../utils/request'

const router = useRouter()

// 表单数据
const form = reactive({
  storyTitle: '',
  emotionalTone: '',
  storyOutline: '',
  gameBackground: '',
  missions: [],
  characters: []
})

// 情感基调选项
const emotionalTones = [
  { label: '治愈', value: 'healing' },
  { label: '悲伤', value: 'sadness' },
  { label: '温暖', value: 'warm' },
  { label: '悬疑', value: 'suspense' },
  { label: '欢乐', value: 'joyful' },
  { label: '紧张', value: 'tense' },
  { label: '浪漫', value: 'romantic' },
  { label: '冒险', value: 'adventure' }
]

// 表单验证规则
const rules = {
  storyTitle: [
    { required: true, message: '请输入剧情名称', trigger: 'blur' }
  ],
  emotionalTone: [
    { required: true, message: '请选择情感基调', trigger: 'change' }
  ],
  storyOutline: [
    { required: true, message: '请输入故事大纲', trigger: 'blur' }
  ],
  gameBackground: [
    { required: true, message: '请输入游戏背景', trigger: 'blur' }
  ]
}

const formRef = ref(null)
const submitting = ref(false)

// 添加任务
const addMission = () => {
  form.missions.push({
    name: '',
    triggerCondition: '',
    completionCondition: '',
    storyProgression: ''
  })
}

// 删除任务
const removeMission = (index) => {
  if (form.missions.length <= 1) {
    ElMessage.warning('至少需要一个任务')
    return
  }
  form.missions.splice(index, 1)
}

// 添加角色
const addCharacter = () => {
  form.characters.push({
    name: '',
    personality: '',
    appearance: '',
    speechStyle: '',
    relationships: ''
  })
}

// 删除角色
const removeCharacter = (index) => {
  if (form.characters.length <= 1) {
    ElMessage.warning('至少需要一个角色')
    return
  }
  form.characters.splice(index, 1)
}

// 暂存原稿
const saveDraft = async () => {
  try {
    // 暂存逻辑 - 这里可以调用保存接口或本地存储
    localStorage.setItem('manuscriptDraft', JSON.stringify(form))
    ElMessage.success('原稿已暂存')
  } catch (error) {
    ElMessage.error('暂存失败')
  }
}

// 提交AI生成
const submitToAI = async () => {
  // 验证表单
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    ElMessage.error('请填写完整信息后再提交')
    return
  }

  // 检查任务和角色是否至少有一个
  if (form.missions.length === 0) {
    ElMessage.error('请至少添加一个任务')
    return
  }
  if (form.characters.length === 0) {
    ElMessage.error('请至少添加一个角色')
    return
  }

  submitting.value = true

  try {
    // 将表单数据转换为结构化JSON
    const manuscriptData = {
      storyTitle: form.storyTitle,
      emotionalTone: form.emotionalTone,
      storyOutline: form.storyOutline,
      gameBackground: form.gameBackground,
      missions: form.missions,
      characters: form.characters
    }

    // 调用后端AI提交接口
    const response = await request.post('/ai/game/submit', {
      content: JSON.stringify(manuscriptData), // 将结构化原稿数据作为content
      context: { gameId: 'new' }, // 新建游戏ID
      params: { 
        style: "像素风", 
        emotion: form.emotionalTone 
      }
    })

    // 成功后跳转到AI生成中页面，携带taskId
    if (response.code === 200) {
      router.push(`/generation-progress?taskId=${response.data.taskId}`)
      ElMessage.success('已提交AI生成，请稍候...')
    } else {
      throw new Error(response.msg || '提交失败')
    }
  } catch (error) {
    console.error('提交AI生成失败:', error)
    ElMessage.error(error.message || '提交失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 初始化时尝试加载暂存的草稿
const loadDraft = () => {
  const draft = localStorage.getItem('manuscriptDraft')
  if (draft) {
    try {
      const parsed = JSON.parse(draft)
      Object.assign(form, parsed)
      ElMessage.info('已加载暂存的原稿')
    } catch (error) {
      console.error('加载暂存草稿失败:', error)
    }
  }
}

// 页面加载时尝试加载暂存的草稿
loadDraft()
</script>

<style scoped>
.manuscript-input-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.module-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.required {
  color: var(--el-color-danger);
}

.mission-item,
.character-item {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  background-color: #fafafa;
}

.form-actions {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

:deep(.el-form-item__label) {
  font-weight: bold;
}
</style>