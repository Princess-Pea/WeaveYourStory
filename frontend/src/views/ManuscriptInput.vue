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
          @click="handleSaveDraft"
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
import { saveDraft, getDraftDetail } from '@/api/projects'
import { useAuth } from '@/stores/auth'

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
const handleSaveDraft = async () => {
  try {
    // 检查认证状态
    const { userInfo, getToken } = useAuth();
    const token = getToken();
    
    if (!token) {
      ElMessage.warning('请先登录再进行保存操作');
      router.push('/login');
      return;
    }
    
    // 检查是否为游客模式
    if (userInfo.value?.is_guest) {
      ElMessage.warning('游客模式不支持保存功能，请注册登录后使用');
      return;
    }
    
    // 验证表单
    const valid = await formRef.value.validateField(['storyTitle', 'emotionalTone', 'storyOutline', 'gameBackground']).catch(() => true)
    if (!valid) {
      ElMessage.warning('请先填写基本的原稿信息')
      return
    }
    
    // 构造草稿数据
    const draftData = {
      title: form.storyTitle || '未命名原稿',
      manuscript: {
        storyTitle: form.storyTitle,
        emotionalTone: form.emotionalTone,
        storyOutline: form.storyOutline,
        gameBackground: form.gameBackground,
        missions: form.missions,
        characters: form.characters
      }
    }
    
    // 调用后端API保存草稿
    const response = await saveDraft(draftData)
    
    if (response.code === 200) {
      ElMessage.success('原稿已暂存')
      // 可以选择性地保存草稿ID到本地以便后续访问
      localStorage.setItem('currentDraftId', response.data.draft_id)
    } else {
      throw new Error(response.msg || '暂存失败')
    }
  } catch (error) {
    console.error('暂存原稿失败:', error)
    
    // 如果是网络错误，已经在拦截器中处理过了
    if (!error.response) {
      // 错误已在全局拦截器中处理，这里不做额外处理
      return;
    }
    
    // 检查是否为游客模式限制
    if (error.response?.data?.code === 403 && error.response.data.data?.guest_mode) {
      ElMessage.warning('游客模式不支持保存功能，请注册登录后使用')
    } else {
      // 其他错误已在拦截器中处理
      console.log('错误已在全局拦截器中处理')
    }
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
const loadDraft = async () => {
  try {
    // 检查认证状态
    const { userInfo, getToken } = useAuth();
    const token = getToken();
    
    if (!token || userInfo.value?.is_guest) {
      // 如果未登录或为游客，尝试从localStorage加载
      const localDraft = localStorage.getItem('manuscriptDraft');
      if (localDraft) {
        try {
          const parsed = JSON.parse(localDraft);
          Object.assign(form, parsed);
          ElMessage.info('已加载本地暂存的原稿');
        } catch (error) {
          console.error('加载本地暂存草稿失败:', error);
        }
      }
      return;
    }
    
    // 已登录用户，尝试从后端获取最近的草稿
    const response = await getDraftList();
    
    if (response.code === 200 && response.data.drafts.length > 0) {
      // 获取最新保存的草稿
      const latestDraft = response.data.drafts.reduce((latest, draft) => {
        return new Date(draft.updated_at) > new Date(latest.updated_at) ? draft : latest;
      });
      
      // 获取详细内容
      const detailResponse = await getDraftDetail(latestDraft.draft_id);
      if (detailResponse.code === 200 && detailResponse.data.manuscript) {
        Object.assign(form, detailResponse.data.manuscript);
        ElMessage.info(`已加载云端草稿: ${detailResponse.data.title}`);
      }
    } else {
      // 如果没有云端草稿，尝试从localStorage加载
      const localDraft = localStorage.getItem('manuscriptDraft');
      if (localDraft) {
        try {
          const parsed = JSON.parse(localDraft);
          Object.assign(form, parsed);
          ElMessage.info('已加载本地暂存的原稿');
        } catch (error) {
          console.error('加载本地暂存草稿失败:', error);
        }
      }
    }
  } catch (error) {
    console.error('加载草稿失败:', error);
    
    // 回退到本地存储
    const localDraft = localStorage.getItem('manuscriptDraft');
    if (localDraft) {
      try {
        const parsed = JSON.parse(localDraft);
        Object.assign(form, parsed);
        ElMessage.info('已加载本地暂存的原稿');
      } catch (error) {
        console.error('加载本地暂存草稿失败:', error);
      }
    }
  }
};

// 页面加载时尝试加载暂存的草稿
loadDraft();
</script>

<style scoped>
.manuscript-input-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #020817; /* 新的深蓝灰色背景 */
  border-radius: 10px;
  color: #ecf0f1; /* 浅灰色文字 */
}

.module-card {
  margin-bottom: 20px;
  background-color: #383F59; /* 功能块色 */
  border: 1px solid #383F59; /* 功能块色边框 */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.required {
  color: #E9A33B; /* 高亮色作为星号颜色 */
}

.mission-item,
.character-item {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #383F59; /* 功能块色边框 */
  border-radius: 4px;
  background-color: #383F59; /* 功能块色背景 */
  color: white;
}

.form-actions {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

:deep(.el-form-item__label) {
  font-weight: bold;
  color: #ecf0f1 !important; /* 浅灰色标签文字 */
}

:deep(.el-input__wrapper),
:deep(.el-textarea__inner),
:deep(.el-select__wrapper) {
  background-color: #383F59 !important; /* 功能块色输入框背景 */
  border: 1px solid #383F59 !important; /* 功能块色边框 */
  color: white !important; /* 白色输入文字 */
  transition: all 0.3s !important;
}

:deep(.el-input__wrapper):hover,
:deep(.el-textarea__inner):hover,
:deep(.el-select__wrapper):hover {
  border: 1px solid #E9A33B !important; /* 悬停高亮色 */
  box-shadow: 0 0 10px #E9A33B !important; /* 氛围荧光效果 */
}

:deep(.el-input__inner),
:deep(.el-textarea__inner) {
  color: white !important;
}

:deep(.el-card__header) {
  background-color: #383F59 !important; /* 功能块色卡片头部 */
  color: white !important;
  border-bottom: 1px solid #383F59 !important;
}

:deep(.el-divider__text) {
  background-color: #020817 !important; /* 深蓝灰色分割线文字背景 */
  color: #ecf0f1 !important; /* 浅灰色文字 */
}

:deep(.el-divider__content) {
  background-color: #020817 !important; /* 深蓝灰色分割线内容背景 */
  color: #ecf0f1 !important; /* 浅灰色文字 */
}

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

:deep(.el-button--warning) {
  --el-button-bg-color: #E9A33B !important; /* 高亮色 */
  --el-button-border-color: #E9A33B !important;
  --el-button-hover-bg-color: #383F59 !important; /* 功能块色 */
  --el-button-hover-border-color: #383F59 !important;
  --el-button-active-bg-color: #383F59 !important;
  --el-button-active-border-color: #383F59 !important;
  color: black !important;
  transition: all 0.3s !important;
}

:deep(.el-button--warning):hover {
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

h2 {
  color: white;
  text-align: center;
}

p {
  color: #bdc3c7; /* 浅灰色描述文字 */
  text-align: center;
  margin-bottom: 30px;
}
</style>