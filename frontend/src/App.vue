<template>
  <div id="app">
    <el-container>
      <el-header v-if="$route.path !== '/' && $route.path !== '/login' && $route.path !== '/register'">
        <div class="header-content">
          <router-link to="/" class="app-title-link">
            <h1 class="app-title">PixelForge</h1>
          </router-link>
          <nav class="navigation">
            <router-link to="/">首页</router-link>
            <router-link to="/manuscript-input">原稿输入</router-link>
            <router-link to="/visual-editor">可视化编辑</router-link>
            <router-link to="/pixel-preview">像素风预览</router-link>
            <router-link to="/profile">个人中心</router-link>
          </nav>
          
          <!-- 用户状态展示区域 -->
          <div class="user-section">
            <!-- 未登录状态 -->
            <div v-if="!isLoggedIn" class="auth-buttons">
              <router-link to="/login" class="auth-link">登录</router-link>
              <span class="divider">/</span>
              <router-link to="/register" class="auth-link">注册</router-link>
            </div>
            
            <!-- 已登录状态 -->
            <el-dropdown v-else trigger="click" @command="handleCommand">
              <span class="user-info">
                <el-icon class="user-icon"><User /></el-icon>
                <span class="username">{{ userInfo?.username }}</span>
                <el-tag v-if="userInfo?.is_guest" type="warning" size="small" class="guest-tag">游客</el-tag>
                <el-icon class="arrow-icon"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile" :disabled="userInfo?.is_guest">
                    <el-icon><User /></el-icon>
                    个人中心
                    <el-tag v-if="userInfo?.is_guest" type="info" size="small" style="margin-left: 8px;">需登录</el-tag>
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userInfo?.is_guest" command="register" divided>
                    <el-icon><Edit /></el-icon>
                    注册账号保存数据
                  </el-dropdown-item>
                  <el-dropdown-item command="logout" divided>
                    <el-icon><SwitchButton /></el-icon>
                    {{ userInfo?.is_guest ? '退出游客模式' : '退出登录' }}
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      <el-main :class="{ 'no-header': $route.path === '/' || $route.path === '/login' || $route.path === '/register' }">
        <router-view />
      </el-main>
      <el-footer v-if="$route.path !== '/login' && $route.path !== '/register'">
        <p>Powered by PixelForge - 设计属于你的像素冒险世界</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, ArrowDown, SwitchButton, Edit } from '@element-plus/icons-vue'
import { useAuth } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const { isLoggedIn, userInfo, clearAuth } = useAuth()

/**
 * 处理下拉菜单命令
 */
const handleCommand = (command) => {
  if (command === 'profile') {
    // 游客无法访问个人中心
    if (userInfo.value?.is_guest) {
      ElMessage.warning('游客模式不支持此功能，请注册登录后使用')
      return
    }
    router.push('/profile')
  } else if (command === 'register') {
    // 跳转到注册页
    router.push('/register')
  } else if (command === 'logout') {
    handleLogout()
  }
}

/**
 * 处理退出登录
 */
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 清除认证信息
    clearAuth()
    
    ElMessage.success('已退出登录')
    
    // 跳转到首页
    router.push('/')
  } catch {
    // 用户取消
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  background-color: #020817; /* 新的深蓝灰色背景 */
}

.el-header {
  background-color: #383F59; /* 功能块色 */
  color: #fff;
  display: flex;
  align-items: center;
  height: 60px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 20px;
}

.no-header {
  padding: 0 !important;
}

.app-title-link {
  text-decoration: none;
  color: inherit;
}

.app-title {
  font-family: 'Times New Roman', Times, serif; /* 使用Times New Roman字体 */
  font-size: 1.5rem;
  margin: 0;
  color: white;
  transition: all 0.3s;
  padding: 8px 16px;
  border-radius: 4px;
  border: 2px solid transparent;
}

.app-title:hover {
  background-color: #383F59; /* 功能块色 */
  text-decoration: underline;
  border: 2px solid #E9A33B; /* 悬停高亮色 */
  box-shadow: 0 0 10px #E9A33B; /* 氛围荧光效果 */
}

.navigation {
  display: flex;
  gap: 20px;
  flex: 1;
  justify-content: center;
}

.navigation a {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.3s;
  border: 2px solid transparent; /* 初始透明边框，为悬停效果预留空间 */
}

.navigation a.router-link-exact-active,
.navigation a:hover {
  background-color: #383F59; /* 功能块色 */
  text-decoration: underline;
  border: 2px solid #E9A33B; /* 悬停高亮色 */
  box-shadow: 0 0 10px #E9A33B; /* 氛围荧光效果 */
}

.el-footer {
  background-color: #383F59; /* 功能块色 */
  color: #fff;
  text-align: center;
  line-height: 60px;
}

/* 全局滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #020817;
}

::-webkit-scrollbar-thumb {
  background: #383F59;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #E9A33B;
}

/* 用户状态展示区域 */
.user-section {
  display: flex;
  align-items: center;
  min-width: 150px;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
}

.auth-link {
  color: white;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 4px;
  transition: all 0.3s;
  border: 1px solid transparent;
}

.auth-link:hover {
  background-color: #383F59;
  border: 1px solid #E9A33B;
  box-shadow: 0 0 8px rgba(233, 163, 59, 0.3);
}

.divider {
  color: rgba(255, 255, 255, 0.5);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s;
  border: 1px solid transparent;
  color: white;
}

.user-info:hover {
  background-color: #383F59;
  border: 1px solid #E9A33B;
  box-shadow: 0 0 8px rgba(233, 163, 59, 0.3);
}

.user-icon,
.arrow-icon {
  font-size: 16px;
}

.username {
  font-size: 14px;
  font-weight: 500;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.guest-tag {
  margin-left: 8px;
  font-size: 12px;
}
</style>