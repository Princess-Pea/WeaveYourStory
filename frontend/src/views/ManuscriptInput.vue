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
                v-model="form.selectedEmotionOption" 
                placeholder="请选择情感基调"
                style="width: 100%"
                @change="handleEmotionChange"
              >
                <el-option 
                  v-for="tone in emotionalTones" 
                  :key="tone.value" 
                  :label="tone.label" 
                  :value="tone.value"
                />
                <el-option 
                  key="custom"
                  label="自定义"
                  value="custom"
                />
              </el-select>
            </el-form-item>
            <!-- 自定义情感基调输入框 -->
            <el-form-item 
              v-if="form.selectedEmotionOption === 'custom'" 
              label="自定义情感基调" 
              prop="customEmotionalTone"
            >
              <el-input 
                v-model="form.customEmotionalTone" 
                placeholder="请输入自定义情感基调（如：神秘、紧张、温馨等）"
              />
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
          type="success" 
          @click="fillWithDefaultTemplate"
        >
          📋 默认模板填充
        </el-button>
        <el-button 
          :type="developerMode ? 'warning' : 'info'" 
          @click="toggleDeveloperMode"
        >
          {{ developerMode ? '开发者模式: ON' : '开发者模式: OFF' }}
        </el-button>
        <el-button 
          type="warning" 
          @click="handleSaveDraft"
        >
          💾 暂存原稿
        </el-button>
        <el-button 
          type="info" 
          @click="handleRestoreDraft"
        >
          🔄 恢复到暂存的原稿
        </el-button>
        <el-button 
          type="primary" 
          @click="submitToAI"
          :loading="submitting"
        >
          🤖 {{ developerMode ? '加载预设数据' : '提交AI生成' }}
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import request from '../utils/request'
import { saveDraft, getDraftDetail, getDraftList } from '@/api/projects'
import { useAuth } from '@/stores/auth'
import { getRandomTemplate } from '@/constants/manuscriptTemplates'
import { getPresetByTemplateId, getRandomPreset } from '@/constants/gamePresets'

const router = useRouter()

// 表单数据
const form = reactive({
  storyTitle: '',
  emotionalTone: '',
  selectedEmotionOption: '',
  customEmotionalTone: '',
  storyOutline: '',
  gameBackground: '',
  missions: [],
  characters: []
})

// 开发者模式状态
const developerMode = ref(false);

// 初始化时检查开发者模式状态
onMounted(() => {
  const savedDeveloperMode = localStorage.getItem('developerMode');
  developerMode.value = savedDeveloperMode === 'true';
});

// 切换开发者模式
const toggleDeveloperMode = () => {
  developerMode.value = !developerMode.value;
  localStorage.setItem('developerMode', developerMode.value.toString());
  
  if (developerMode.value) {
    ElMessage.success('已启用开发者模式');
  } else {
    ElMessage.info('已禁用开发者模式');
  }
};

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
    { 
      validator: (rule, value, callback) => {
        // 如果选择了自定义选项，则不需要验证预设情感基调
        if (form.selectedEmotionOption === 'custom') {
          callback(); // 通过验证
        } else {
          // 否则需要验证预设情感基调是否已选择
          if (!value) {
            callback(new Error('请选择情感基调'));
          } else {
            callback();
          }
        }
      },
      trigger: 'change'
    }
  ],
  customEmotionalTone: [
    { 
      validator: (rule, value, callback) => {
        // 如果选择了自定义选项，则需要验证自定义输入
        if (form.selectedEmotionOption === 'custom') {
          if (!value || value.trim() === '') {
            callback(new Error('请输入自定义情感基调'));
          } else if (value.length < 1 || value.length > 20) {
            callback(new Error('长度在 1 到 20 个字符之间'));
          } else {
            callback();
          }
        } else {
          callback(); // 没有选择自定义，通过验证
        }
      },
      trigger: 'blur'
    }
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

// 使用默认模板填充表单
const fillWithDefaultTemplate = () => {
  const template = getRandomTemplate()
  const templateData = template.data
  
  // 保存模板ID，以便在提交时使用相同的预设
  localStorage.setItem('selectedTemplateId', template.id);
  
  // 填充所有字段
  form.storyTitle = templateData.storyTitle
  form.selectedEmotionOption = templateData.selectedEmotionOption
  form.emotionalTone = templateData.emotionalTone
  form.customEmotionalTone = templateData.customEmotionalTone
  form.storyOutline = templateData.storyOutline
  form.gameBackground = templateData.gameBackground
  form.missions = JSON.parse(JSON.stringify(templateData.missions))
  form.characters = JSON.parse(JSON.stringify(templateData.characters))
  
  // 启用开发者模式，使得提交AI生成时会返回预设游戏数据
  localStorage.setItem('developerMode', 'true')
  
  ElMessage.success(`已填充模板：${template.name} (${template.style})。点击「提交AI生成」便会加载对应的游戏数据。`)
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
    
    // 验证表单 - 检查是否至少填写了一些基本信息
    const hasBasicInfo = form.storyTitle.trim() !== '' || 
                   form.emotionalTone !== '' || 
                   form.selectedEmotionOption !== '' ||
                   form.customEmotionalTone !== '' ||
                   form.storyOutline.trim() !== '' || 
                   form.gameBackground.trim() !== '' ||
                   form.missions.some(mission => mission.name.trim() !== '' || mission.triggerCondition.trim() !== '') ||
                   form.characters.some(character => character.name.trim() !== '');
    
    if (!hasBasicInfo) {
      ElMessage.warning('请至少填写部分原稿信息才能暂存');
      return;
    }
    
    // 构造草稿数据
    const draftData = {
      title: form.storyTitle || '未命名原稿',
      manuscript: {
        storyTitle: form.storyTitle,
        emotionalTone: getFinalEmotionalTone(), // 使用最终的情感基调值
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
      // 持久化到本地存储作为备选
      localStorage.setItem('manuscriptDraft', JSON.stringify(form))
      // 可以选择性地保存草稿ID到本地以便后续访问
      const draftId = response.data.draft?.draft_id || response.data.draft_id;
      if (draftId) {
        localStorage.setItem('currentDraftId', draftId);
      }
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

// 恢复到暂存的原稿
const handleRestoreDraft = async () => {
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
          
          // 处理情感基调的加载
          if (parsed.emotionalTone) {
            // 检查是否是预设的情感基调
            const isPresetEmotion = emotionalTones.some(tone => tone.value === parsed.emotionalTone);
            if (isPresetEmotion) {
              form.selectedEmotionOption = parsed.emotionalTone;
            } else {
              // 如果不是预设选项，说明是自定义情感基调
              form.selectedEmotionOption = 'custom';
              form.customEmotionalTone = parsed.emotionalTone;
            }
          }
          
          ElMessage.success('已恢复本地暂存的原稿');
        } catch (error) {
          console.error('恢复本地暂存草稿失败:', error);
          ElMessage.error('恢复失败：本地数据损坏');
        }
      } else {
        ElMessage.info('没有找到暂存的原稿');
      }
      return;
    }
    
    // 已登录用户，尝试从后端获取最近的草稿
    console.log('开始获取云端草稿列表...');
    const response = await getDraftList();
    console.log('云端草稿列表响应:', response);
    
    if (response.code === 200 && response.data?.drafts?.length > 0) {
      // 获取最新保存的草稿
      const latestDraft = response.data.drafts.reduce((latest, draft) => {
        return new Date(draft.updated_at) > new Date(latest.updated_at) ? draft : latest;
      });
      
      console.log('获取最新草稿详情，ID:', latestDraft.draft_id);
      // 获取详细内容
      const detailResponse = await getDraftDetail(latestDraft.draft_id);
      console.log('草稿详情响应:', detailResponse);
      
      const draftData = detailResponse.data?.draft || detailResponse.data;
      const manuscript = draftData?.manuscript;
      
      if (detailResponse.code === 200 && manuscript) {
        Object.assign(form, manuscript);
        
        // 处理情感基调的加载
        if (manuscript.emotionalTone) {
          // 检查是否是预设的情感基调
          const isPresetEmotion = emotionalTones.some(tone => tone.value === manuscript.emotionalTone);
          if (isPresetEmotion) {
            form.selectedEmotionOption = manuscript.emotionalTone;
          } else {
            // 如果不是预设选项，说明是自定义情感基调
            form.selectedEmotionOption = 'custom';
            form.customEmotionalTone = manuscript.emotionalTone;
          }
        }
        
        ElMessage.success(`已恢复云端草稿: ${draftData.title || '未命名'}`);
      } else {
        throw new Error(detailResponse.msg || '获取草稿详情失败');
      }
    } else {
      // 如果没有云端草稿，尝试从localStorage加载
      const localDraft = localStorage.getItem('manuscriptDraft');
      if (localDraft) {
        try {
          const parsed = JSON.parse(localDraft);
          Object.assign(form, parsed);
          
          // 处理情感基调的加载
          if (parsed.emotionalTone) {
            // 检查是否是预设的情感基调
            const isPresetEmotion = emotionalTones.some(tone => tone.value === parsed.emotionalTone);
            if (isPresetEmotion) {
              form.selectedEmotionOption = parsed.emotionalTone;
            } else {
              // 如果不是预设选项，说明是自定义情感基调
              form.selectedEmotionOption = 'custom';
              form.customEmotionalTone = parsed.emotionalTone;
            }
          }
          
          ElMessage.success('已恢复本地暂存的原稿');
        } catch (error) {
          console.error('恢复本地暂存草稿失败:', error);
          ElMessage.error('恢复失败：本地数据损坏');
        }
      } else {
        ElMessage.info('云端和本地都没有找到暂存的原稿');
      }
    }
  } catch (error) {
    console.error('恢复草稿失败:', error);
    
    // 更详细的错误信息处理
    if (error.response) {
      // 服务器响应了错误状态码
      if (error.response.status === 401) {
        ElMessage.error('认证失败，请重新登录');
      } else {
        ElMessage.error(`恢复失败: ${error.response.data?.msg || error.response.statusText || '未知错误'}`);
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      ElMessage.error('网络连接失败，请检查网络设置');
    } else {
      // 其他错误
      ElMessage.error(error.message || '恢复失败，请检查网络设置');
    }
  }
};

// 处理情感基调选择变化
const handleEmotionChange = (value) => {
  if (value === 'custom') {
    // 当选择自定义时，清空预设情感基调
    form.emotionalTone = '';
  } else {
    // 当选择预设选项时，设置对应的情感基调
    form.emotionalTone = value;
  }
};

// 获取最终的情感基调值
const getFinalEmotionalTone = () => {
  if (form.selectedEmotionOption === 'custom') {
    return form.customEmotionalTone;
  }
  return form.emotionalTone;
};

// 提交AI生成
const submitToAI = async () => {
  // 检查任务和角色是否至少有一个
  if (form.missions.length === 0) {
    ElMessage.error('请至少添加一个任务');
    return;
  }
  if (form.characters.length === 0) {
    ElMessage.error('请至少添加一个角色');
    return;
  }

  submitting.value = true

  try {
    // 将表单数据转换为结构化JSON
    const manuscriptData = {
      storyTitle: form.storyTitle,
      emotionalTone: getFinalEmotionalTone(),
      storyOutline: form.storyOutline,
      gameBackground: form.gameBackground,
      missions: form.missions,
      characters: form.characters
    }

    // ===== 开发者模式处理 =====
    // 检查是否启用了开发者模式（通过使用默认模板填充）
    // 在开发者模式下，直接返回预设游戏数据而不调用真实AI接口
    const isDeveloperMode = localStorage.getItem('developerMode') === 'true'
    
    if (isDeveloperMode) {
      // 获取保存的模板ID，如果不存在则使用随机预设
      const selectedTemplateId = localStorage.getItem('selectedTemplateId');
      let preset;
      
      if (selectedTemplateId) {
        // 尝试根据保存的模板ID获取对应的预设
        preset = getPresetByTemplateId(selectedTemplateId.replace('template_', 'template')) || getRandomPreset();
      } else {
        // 如果没有保存的模板ID，则使用随机预设
        preset = getRandomPreset();
      }
      
      const gameData = preset.gameData
      
      // 将游戏数据保存到localStorage以供可视化编辑器使用
      localStorage.setItem(`game_${gameData.gameId}`, JSON.stringify(gameData))
      
      // 显示成功消息
      ElMessage.success(`开发者模式：已加载预设 "${preset.name}" 的游戏数据`)
      
      // 跳转到可视化编辑器
      router.push(`/visual-editor?gameId=${gameData.gameId}`)
      return
    }

    // 调用后端AI提交接口（正常模式）
    const response = await request.post('/api/v1/ai/game/submit', {
      content: JSON.stringify(manuscriptData), // 将结构化原稿数据作为content
      context: { gameId: 'new' }, // 新建游戏ID
      params: { 
        style: "像素风", 
        emotion: getFinalEmotionalTone() 
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
    
    // 检查当前表单是否已经有内容（防止覆盖用户正在编辑的内容）
    const hasUnsavedContent = form.storyTitle.trim() !== '' ||
                           form.emotionalTone !== '' ||
                           form.selectedEmotionOption !== '' ||
                           form.customEmotionalTone !== '' ||
                           form.storyOutline.trim() !== '' ||
                           form.gameBackground.trim() !== '' ||
                           form.missions.some(mission => mission.name.trim() !== '' || mission.triggerCondition.trim() !== '') ||
                           form.characters.some(character => character.name.trim() !== '');
    
    if (hasUnsavedContent) {
      // 如果当前有未保存的内容，不加载历史草稿
      console.log('检测到当前有编辑内容，跳过加载历史草稿');
      return;
    }
    
    if (!token || userInfo.value?.is_guest) {
      // 如果未登录或为游客，尝试从localStorage加载
      const localDraft = localStorage.getItem('manuscriptDraft');
      if (localDraft) {
        try {
          const parsed = JSON.parse(localDraft);
          Object.assign(form, parsed);
          
          // 处理情感基调的加载
          if (parsed.emotionalTone) {
            // 检查是否是预设的情感基调
            const isPresetEmotion = emotionalTones.some(tone => tone.value === parsed.emotionalTone);
            if (isPresetEmotion) {
              form.selectedEmotionOption = parsed.emotionalTone;
            } else {
              // 如果不是预设选项，说明是自定义情感基调
              form.selectedEmotionOption = 'custom';
              form.customEmotionalTone = parsed.emotionalTone;
            }
          }
          
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
      const draftData = detailResponse.data?.draft || detailResponse.data;
      const manuscript = draftData?.manuscript;

      if (detailResponse.code === 200 && manuscript) {
        Object.assign(form, manuscript);
        
        // 处理情感基调的加载
        if (manuscript.emotionalTone) {
          // 检查是否是预设的情感基调
          const isPresetEmotion = emotionalTones.some(tone => tone.value === manuscript.emotionalTone);
          if (isPresetEmotion) {
            form.selectedEmotionOption = manuscript.emotionalTone;
          } else {
            // 如果不是预设选项，说明是自定义情感基调
            form.selectedEmotionOption = 'custom';
            form.customEmotionalTone = manuscript.emotionalTone;
          }
        }
        
        ElMessage.info(`已加载云端草稿: ${draftData.title || '未命名'}`);
      }
    } else {
      // 如果没有云端草稿，尝试从localStorage加载
      const localDraft = localStorage.getItem('manuscriptDraft');
      if (localDraft) {
        try {
          const parsed = JSON.parse(localDraft);
          Object.assign(form, parsed);
          
          // 处理情感基调的加载
          if (parsed.emotionalTone) {
            // 检查是否是预设的情感基调
            const isPresetEmotion = emotionalTones.some(tone => tone.value === parsed.emotionalTone);
            if (isPresetEmotion) {
              form.selectedEmotionOption = parsed.emotionalTone;
            } else {
              // 如果不是预设选项，说明是自定义情感基调
              form.selectedEmotionOption = 'custom';
              form.customEmotionalTone = parsed.emotionalTone;
            }
          }
          
          ElMessage.info('已加载本地暂存的原稿');
        } catch (error) {
          console.error('加载本地暂存草稿失败:', error);
        }
      }
    }
  } catch (error) {
    console.error('加载草稿失败:', error);
    
    // 如果是401错误，说明认证失败，但不再额外提示（已在拦截器中处理）
    if (error.response?.status === 401) {
      console.log('认证失败，已在拦截器中处理');
      return; // 直接返回，不再回退到本地存储
    }
    
    // 其他错误，回退到本地存储
    const localDraft = localStorage.getItem('manuscriptDraft');
    if (localDraft) {
      try {
        const parsed = JSON.parse(localDraft);
        Object.assign(form, parsed);
        
        // 处理情感基调的加载
        if (parsed.emotionalTone) {
          // 检查是否是预设的情感基调
          const isPresetEmotion = emotionalTones.some(tone => tone.value === parsed.emotionalTone);
          if (isPresetEmotion) {
            form.selectedEmotionOption = parsed.emotionalTone;
          } else {
            // 如果不是预设选项，说明是自定义情感基调
            form.selectedEmotionOption = 'custom';
            form.customEmotionalTone = parsed.emotionalTone;
          }
        }
        
        ElMessage.info('已加载本地暂存的原稿');
      } catch (error) {
        console.error('加载本地暂存草稿失败:', error);
      }
    }
  }
};

// 页面加载时尝试加载暂存的草稿
// 临时注释：排查登录后立即显示"登录已过期"问题
// loadDraft();
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