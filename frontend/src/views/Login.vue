<template>
  <div class="login-container">
    <!-- 像素风装饰网格背景 -->
    <div class="grid-background"></div>
    
    <!-- 登录表单卡片 -->
    <div class="login-card">
      <h2 class="login-title">欢迎回到 PixelForge</h2>
      <p class="login-subtitle">登录您的账号，继续创作像素冒险</p>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <!-- 用户名输入框 -->
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <!-- 密码输入框 -->
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
            clearable
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <!-- 登录按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="login-button"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '立即登录' }}
          </el-button>
        </el-form-item>
        
        <!-- 注册链接 -->
        <div class="register-link">
          <span>还没有账号？</span>
          <router-link to="/register">立即注册</router-link>
        </div>
        
        <!-- 游客模式提示 -->
        <div class="guest-mode">
          <el-divider>或</el-divider>
          <el-button
            type="info"
            size="large"
            plain
            class="guest-button"
            @click="handleGuestLogin"
          >
            游客模式体验（数据不保存）
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login, guestLogin } from '@/api/auth'
import { useAuth } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const { setAuth } = useAuth()

// 表单引用
const loginFormRef = ref(null)

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ]
}

// 加载状态
const loading = ref(false)

/**
 * 处理登录
 */
const handleLogin = async () => {
  // 验证表单
  const valid = await loginFormRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true

  try {
    // 调用登录 API
    const response = await login({
      username: loginForm.username,
      password: loginForm.password
    })

    // 检查响应状态
    if (response.code === 200 && response.data) {
      // 存储 Token 和用户信息
      setAuth(response.data.token, {
        user_id: response.data.user_id,
        username: response.data.username
      })

      ElMessage.success('登录成功！')

      // 跳转到目标页面或首页
      const redirectPath = route.query.redirect || '/manuscript-input'
      router.push(redirectPath)
    } else {
      ElMessage.error(response.msg || '登录失败，请重试')
    }
  } catch (error) {
    console.error('登录失败:', error)
    // 错误已在 axios 拦截器中处理
  } finally {
    loading.value = false
  }
}

/**
 * 处理游客登录
 */
const handleGuestLogin = async () => {
  loading.value = true

  try {
    // 调用游客登录 API
    const response = await guestLogin()

    // 检查响应状态
    if (response.code === 200 && response.data) {
      // 存储 Token 和用户信息
      setAuth(response.data.token, {
        user_id: response.data.user_id,
        username: response.data.username,
        is_guest: true
      })

      ElMessage.success('欢迎使用游客模式！')

      // 跳转到目标页面或首页
      const redirectPath = route.query.redirect || '/manuscript-input'
      router.push(redirectPath)
    } else {
      ElMessage.error(response.msg || '游客登录失败，请重试')
    }
  } catch (error) {
    console.error('游客登录失败:', error)
    // 错误已在 axios 拦截器中处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #020817;
  overflow: hidden;
}

/* 像素风网格背景 */
.grid-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(56, 63, 89, 0.3) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56, 63, 89, 0.3) 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.5;
  pointer-events: none;
}

/* 登录卡片 */
.login-card {
  position: relative;
  width: 420px;
  padding: 40px;
  background-color: rgba(56, 63, 89, 0.9);
  border: 2px solid #E9A33B;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(233, 163, 59, 0.3);
  z-index: 1;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-title {
  font-family: 'Times New Roman', Times, serif;
  font-size: 28px;
  color: #E9A33B;
  text-align: center;
  margin: 0 0 10px 0;
}

.login-subtitle {
  color: #ffffff;
  text-align: center;
  margin: 0 0 30px 0;
  font-size: 14px;
  opacity: 0.8;
}

.login-form {
  margin-top: 20px;
}

.login-button {
  width: 100%;
  background-color: #E9A33B;
  border-color: #E9A33B;
  font-size: 16px;
  font-weight: bold;
  transition: all 0.3s;
}

.login-button:hover {
  background-color: #d89327;
  border-color: #d89327;
  box-shadow: 0 0 15px rgba(233, 163, 59, 0.5);
}

.register-link {
  text-align: center;
  color: #ffffff;
  font-size: 14px;
  margin-top: 20px;
}

.register-link a {
  color: #E9A33B;
  text-decoration: none;
  margin-left: 8px;
  font-weight: bold;
  transition: all 0.3s;
}

.register-link a:hover {
  text-decoration: underline;
  color: #d89327;
}

/* 游客模式 */
.guest-mode {
  margin-top: 30px;
}

.guest-button {
  width: 100%;
  border-color: rgba(233, 163, 59, 0.5);
  color: rgba(233, 163, 59, 0.8);
  transition: all 0.3s;
}

.guest-button:hover {
  border-color: #E9A33B;
  color: #E9A33B;
  background-color: rgba(233, 163, 59, 0.1);
}

:deep(.el-divider__text) {
  background-color: rgba(56, 63, 89, 0.9);
  color: rgba(255, 255, 255, 0.5);
}

/* Element Plus 组件样式覆盖 */
:deep(.el-input__wrapper) {
  background-color: rgba(2, 8, 23, 0.5);
  border: 1px solid rgba(233, 163, 59, 0.3);
  box-shadow: none;
}

:deep(.el-input__wrapper:hover) {
  border-color: rgba(233, 163, 59, 0.6);
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #E9A33B;
  box-shadow: 0 0 8px rgba(233, 163, 59, 0.3);
}

:deep(.el-input__inner) {
  color: #ffffff;
}

:deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.5);
}
</style>
