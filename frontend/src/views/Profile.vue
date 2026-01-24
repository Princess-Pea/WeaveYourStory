<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <h2>👤 个人中心</h2>
      
      <div class="profile-section">
        <h3>📋 我的作品管理</h3>
        
        <div class="actions">
          <el-button type="primary" @click="saveCurrentGame">💾 保存当前游戏</el-button>
          <el-button type="success" @click="exportGameConfig">📤 导出游戏配置</el-button>
          <el-button type="danger" @click="clearAllGames">🗑️ 清空所有游戏</el-button>
        </div>
        
        <div class="games-list">
          <el-table 
            :data="gamesList" 
            style="width: 100%"
            :row-class-name="tableRowClassName"
          >
            <el-table-column prop="id" label="ID" width="100" />
            <el-table-column prop="name" label="游戏名称" width="200" />
            <el-table-column prop="createTime" label="创建时间" width="180" />
            <el-table-column prop="lastModified" label="最后修改" width="180" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag 
                  :type="getStatusType(row.status)"
                  disable-transitions
                >
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button 
                  size="small" 
                  @click="loadGame(row)"
                >
                  加载
                </el-button>
                <el-button 
                  size="small" 
                  type="primary"
                  @click="editGame(row)"
                >
                  编辑
                </el-button>
                <el-button 
                  size="small" 
                  type="danger"
                  @click="deleteGame(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { saveProject, getProjectList, deleteProject } from '@/api/projects'
import { useAuth } from '@/stores/auth'

const router = useRouter()

// 游戏列表
const gamesList = ref([])

// 初始化
onMounted(() => {
  loadGamesList()
})

// 加载游戏列表
async function loadGamesList() {
  try {
    // 检查认证状态
    const { userInfo, getToken } = useAuth();
    const token = getToken();
    
    if (!token || userInfo.value?.is_guest) {
      // 如果未登录或为游客，尝试从localStorage加载
      const savedGames = localStorage.getItem('games_list');
      if (savedGames) {
        try {
          gamesList.value = JSON.parse(savedGames);
          ElMessage.info('已加载本地游戏列表');
        } catch (error) {
          console.error('加载本地游戏列表失败:', error);
          gamesList.value = [];
        }
      } else {
        // 默认展示一些示例数据
        gamesList.value = [
          {
            id: 'game_1',
            name: '新手村冒险',
            createTime: '2023-10-01 10:30:00',
            lastModified: '2023-10-01 15:45:00',
            status: 'completed'
          },
          {
            id: 'game_2',
            name: '森林探险记',
            createTime: '2023-10-02 14:20:00',
            lastModified: '2023-10-02 18:30:00',
            status: 'in_progress'
          },
          {
            id: 'game_3',
            name: '神秘洞穴之谜',
            createTime: '2023-10-03 09:15:00',
            lastModified: '2023-10-03 09:15:00',
            status: 'draft'
          }
        ];
      }
      return;
    }
    
    // 已登录用户，从后端获取项目列表
    const response = await getProjectList();
    
    if (response.code === 200) {
      // 将后端返回的项目数据格式化为表格所需格式
      gamesList.value = response.data.projects.map(project => ({
        id: project.project_id,
        name: project.title,
        createTime: project.created_at,
        lastModified: project.updated_at,
        status: project.status
      }));
      
      // 同步到localStorage以备不时之需
      localStorage.setItem('games_list', JSON.stringify(gamesList.value));
    } else {
      throw new Error(response.msg || '获取游戏列表失败');
    }
  } catch (error) {
    console.error('加载游戏列表失败:', error);
    
    // 尝试从localStorage加载备份数据
    const savedGames = localStorage.getItem('games_list');
    if (savedGames) {
      try {
        gamesList.value = JSON.parse(savedGames);
        ElMessage.warning('已从本地加载备份数据');
      } catch (parseError) {
        console.error('解析本地游戏列表失败:', parseError);
        gamesList.value = [];
      }
    } else {
      gamesList.value = [];
    }
  }
}

// 保存当前游戏
async function saveCurrentGame() {
  try {
    // 检查是否为游客模式
    const { userInfo } = useAuth();
    if (userInfo.value?.is_guest) {
      ElMessage.warning('游客模式不支持保存功能，请注册登录后使用');
      return;
    }
    
    // 获取当前编辑的游戏数据（从localStorage或其他来源）
    const currentGameId = localStorage.getItem('currentGameId');
    if (!currentGameId) {
      ElMessage.warning('没有检测到当前正在编辑的游戏');
      return;
    }
    
    const currentGameData = localStorage.getItem(`game_${currentGameId}`);
    if (!currentGameData) {
      ElMessage.warning('未找到当前游戏数据');
      return;
    }
    
    const gameDataObj = JSON.parse(currentGameData);
    
    // 构造项目数据
    const projectData = {
      title: gameDataObj.gameName || '未命名游戏',
      game_data: gameDataObj,
      status: 'published'  // 保存当前游戏通常意味着发布
    };
    
    // 调用后端API保存项目
    const response = await saveProject(projectData);
    
    if (response.code === 200) {
      // 更新本地游戏列表
      const gameEntry = {
        id: response.data.project_id,
        name: gameDataObj.gameName || '未命名游戏',
        createTime: new Date().toLocaleString(),
        lastModified: new Date().toLocaleString(),
        status: 'published'
      };
      
      // 检查是否已存在于列表中
      const existingIndex = gamesList.value.findIndex(game => game.id === response.data.project_id);
      if (existingIndex >= 0) {
        // 更新现有游戏
        gamesList.value[existingIndex] = gameEntry;
      } else {
        // 添加新游戏到列表
        gamesList.value.unshift(gameEntry);
      }
      
      // 保存列表到localStorage
      localStorage.setItem('games_list', JSON.stringify(gamesList.value));
      
      ElMessage.success('当前游戏已保存！');
    } else {
      throw new Error(response.msg || '保存失败');
    }
  } catch (error) {
    console.error('保存当前游戏失败:', error);
    
    // 检查是否为游客模式限制
    if (error.response?.data?.code === 403 && error.response.data.data?.guest_mode) {
      ElMessage.warning('游客模式不支持保存功能，请注册登录后使用');
    } else {
      ElMessage.error(error.message || '保存失败，请重试');
    }
  }
}

// 导出游戏配置
function exportGameConfig() {
  // 创建一个包含游戏配置的JSON对象
  const gameConfig = {
    games: gamesList.value,
    exportTime: new Date().toISOString(),
    version: '1.0'
  }
  
  // 创建并下载文件
  const dataStr = JSON.stringify(gameConfig, null, 2)
  const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
  
  const exportFileDefaultName = 'game_config.json'
  
  const linkElement = document.createElement('a')
  linkElement.setAttribute('href', dataUri)
  linkElement.setAttribute('download', exportFileDefaultName)
  linkElement.click()
  
  ElMessage.success('游戏配置已导出')
}

// 清空所有游戏
async function clearAllGames() {
  try {
    await ElMessageBox.confirm(
      '此操作将永久删除所有游戏数据，是否继续？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // 清空localStorage中的游戏数据
    localStorage.removeItem('games_list')
    gamesList.value = []
    ElMessage.success('所有游戏已清空')
  } catch (error) {
    // 用户取消操作
  }
}

// 加载游戏
function loadGame(game) {
  ElMessage.success(`已加载游戏: ${game.name}`)
  // 这里可以实现加载游戏的逻辑
}

// 编辑游戏
function editGame(game) {
  router.push(`/visual-editor?gameId=${game.id}`)
}

// 删除游戏
async function deleteGame(game) {
  try {
    await ElMessageBox.confirm(
      `确定要删除游戏 "${game.name}" 吗？`,
      '删除游戏',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // 检查是否为游客模式
    const { userInfo } = useAuth();
    if (userInfo.value?.is_guest) {
      ElMessage.warning('游客模式不支持删除功能，请注册登录后使用');
      return;
    }
    
    // 如果有有效的认证，尝试从后端删除项目
    const response = await deleteProject(game.id);
    if (response.code === 200) {
      // 从列表中删除该游戏
      const index = gamesList.value.findIndex(item => item.id === game.id);
      if (index !== -1) {
        gamesList.value.splice(index, 1);
        
        // 更新localStorage
        localStorage.setItem('games_list', JSON.stringify(gamesList.value));
        
        ElMessage.success('游戏已删除');
      }
    } else {
      throw new Error(response.msg || '删除失败');
    }
  } catch (error) {
    if (error === 'cancel') {
      // 用户取消操作
      return;
    }
    
    console.error('删除游戏失败:', error);
    
    // 检查是否为游客模式限制
    if (error.response?.data?.code === 403 && error.response.data.data?.guest_mode) {
      ElMessage.warning('游客模式不支持删除功能，请注册登录后使用');
    } else {
      // 降级到本地删除
      const index = gamesList.value.findIndex(item => item.id === game.id);
      if (index !== -1) {
        gamesList.value.splice(index, 1);
        localStorage.setItem('games_list', JSON.stringify(gamesList.value));
        ElMessage.success('游戏已从本地删除');
      }
      ElMessage.error(error.message || '删除失败，请重试');
    }
  }
}

// 获取状态类型
function getStatusType(status) {
  switch(status) {
    case 'completed': return 'success'
    case 'in_progress': return 'warning'
    case 'draft': return 'info'
    case 'failed': return 'danger'
    default: return 'info'
  }
}

// 获取状态文本
function getStatusText(status) {
  switch(status) {
    case 'completed': return '已完成'
    case 'in_progress': return '进行中'
    case 'draft': return '草稿'
    case 'failed': return '失败'
    default: return '未知'
  }
}

// 表格行样式
function tableRowClassName({ row, rowIndex }) {
  if (row.status === 'completed') {
    return 'success-row'
  } else if (row.status === 'failed') {
    return 'error-row'
  }
  return ''
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
  background-color: #020817; /* 新的深蓝灰色背景 */
  min-height: calc(100vh - 100px);
}

.profile-card {
  max-width: 1200px;
  margin: 0 auto;
  background-color: #383F59 !important; /* 功能块色 */
  border: 1px solid #E9A33B !important; /* 高亮边框 */
  transition: all 0.3s;
}

.profile-card:hover {
  box-shadow: 0 0 20px #E9A33B; /* 氛围荧光效果 */
}

.profile-card h2 {
  color: white;
  text-align: center;
  margin-bottom: 30px;
}

.profile-section {
  margin-bottom: 30px;
}

.profile-section h3 {
  color: white;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #E9A33B; /* 高亮分割线 */
}

.actions {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.games-list {
  margin-top: 20px;
}

/* 表格样式 */
:deep(.el-table) {
  background-color: #383F59 !important; /* 功能块色表格背景 */
  border: 1px solid #E9A33B !important; /* 高亮边框 */
}

:deep(.el-table th),
:deep(.el-table td) {
  background-color: #383F59 !important; /* 功能块色单元格背景 */
  color: #ecf0f1 !important; /* 浅灰色文字 */
  border-color: #E9A33B !important; /* 高亮边框 */
}

:deep(.el-table__header tr),
:deep(.el-table__body tr) {
  background-color: #383F59 !important; /* 功能块色行背景 */
}

:deep(.el-table__body tr:nth-child(even)) {
  background-color: #405a70 !important; /* 功能块色偶数行背景 */
}

:deep(.el-table__body tr:hover > td) {
  background-color: #E9A33B !important; /* 悬停行背景 */
  color: black !important;
}

/* 成功行样式 */
:deep(.el-table .success-row) {
  background-color: #2ecc71 !important; /* 绿色成功行 */
  color: white !important;
}

/* 错误行样式 */
:deep(.el-table .error-row) {
  background-color: #e74c3c !important; /* 红色错误行 */
  color: white !important;
}

/* 标签样式 */
:deep(.el-tag) {
  border: none;
}

/* 按钮样式 */
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

:deep(.el-button--success) {
  --el-button-bg-color: #383F59 !important; /* 功能块色 */
  --el-button-border-color: #383F59 !important;
  --el-button-hover-bg-color: #E9A33B !important; /* 悬停高亮色 */
  --el-button-hover-border-color: #E9A33B !important;
  --el-button-active-bg-color: #E9A33B !important;
  --el-button-active-border-color: #E9A33B !important;
  transition: all 0.3s !important;
}

:deep(.el-button--success):hover {
  box-shadow: 0 0 15px #E9A33B !important; /* 氛围荧光效果 */
}

:deep(.el-button--danger) {
  --el-button-bg-color: #383F59 !important; /* 功能块色 */
  --el-button-border-color: #383F59 !important;
  --el-button-hover-bg-color: #E9A33B !important; /* 悬停高亮色 */
  --el-button-hover-border-color: #E9A33B !important;
  --el-button-active-bg-color: #E9A33B !important;
  --el-button-active-border-color: #E9A33B !important;
  transition: all 0.3s !important;
}

:deep(.el-button--danger):hover {
  box-shadow: 0 0 15px #E9A33B !important; /* 氛围荧光效果 */
}

:deep(.el-button--warning) {
  --el-button-bg-color: #383F59 !important; /* 功能块色 */
  --el-button-border-color: #383F59 !important;
  --el-button-hover-bg-color: #E9A33B !important; /* 悬停高亮色 */
  --el-button-hover-border-color: #E9A33B !important;
  --el-button-active-bg-color: #E9A33B !important;
  --el-button-active-border-color: #E9A33B !important;
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
</style>