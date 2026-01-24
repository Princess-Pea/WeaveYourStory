<template>
  <div class="register-container">
    <!-- 像素风装饰网格背景 -->
    <div class="grid-background"></div>
    
    <!-- 注册表单卡片 -->
    <div class="register-card">
      <h2 class="register-title">加入 PixelForge</h2>
      <p class="register-subtitle">创建您的账号，开启像素冒险之旅</p>
      
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        class="register-form"
        @submit.prevent="handleRegister"
      >
        <!-- 用户名输入框 -->
        <el-form-item prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名（3-20个字符）"
            size="large"
            prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <!-- 邮箱输入框 -->
        <el-form-item prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="请输入邮箱（可选）"
            size="large"
            prefix-icon="Message"
            clearable
          />
        </el-form-item>
        
        <!-- 密码输入框 -->
        <el-form-item prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码（至少6个字符）"
            size="large"
            prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>
        
        <!-- 确认密码输入框 -->
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
            clearable
            @keyup.enter="handleRegister"
          />
        </el-form-item>
        
        <!-- 注册按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="register-button"
            @click="handleRegister"
          >
            {{ loading ? '注册中...' : '创建账号' }}
          </el-button>
        </el-form-item>
        
        <!-- 登录链接 -->
        <div class="login-link">
          <span>已有账号？</span>
          <router-link to="/login">返回登录</router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '@/api/auth'

const router = useRouter()

// 表单引用
const registerFormRef = ref(null)

// 注册表单数据
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 自定义验证：确认密码
const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 自定义验证：邮箱（可选）
const validateEmail = (rule, value, callback) => {
  if (value === '') {
    callback() // 邮箱可选，为空也通过
  } else {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(value)) {
      callback(new Error('请输入有效的邮箱地址'))
    } else {
      callback()
    }
  }
}

// 表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  email: [
    { validator: validateEmail, trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 加载状态
const loading = ref(false)

/**
 * 处理注册
 */
const handleRegister = async () => {
  // 验证表单
  const valid = await registerFormRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true

  try {
    // 调用注册 API
    const response = await register({
      username: registerForm.username,
      password: registerForm.password,
      email: registerForm.email || undefined
    })

    // 检查响应状态
    if (response.code === 200) {
      ElMessage.success('注册成功！请登录')
      
      // 跳转到登录页
      setTimeout(() => {
        router.push('/login')
      }, 1000)
    } else {
      ElMessage.error(response.msg || '注册失败，请重试')
    }
  } catch (error) {
    console.error('注册失败:', error)
    // 错误已在 axios 拦截器中处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
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

/* 注册卡片 */
.register-card {
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

.register-title {
  font-family: 'Times New Roman', Times, serif;
  font-size: 28px;
  color: #E9A33B;
  text-align: center;
  margin: 0 0 10px 0;
}

.register-subtitle {
  color: #ffffff;
  text-align: center;
  margin: 0 0 30px 0;
  font-size: 14px;
  opacity: 0.8;
}

.register-form {
  margin-top: 20px;
}

.register-button {
  width: 100%;
  background-color: #E9A33B;
  border-color: #E9A33B;
  font-size: 16px;
  font-weight: bold;
  transition: all 0.3s;
}

.register-button:hover {
  background-color: #d89327;
  border-color: #d89327;
  box-shadow: 0 0 15px rgba(233, 163, 59, 0.5);
}

.login-link {
  text-align: center;
  color: #ffffff;
  font-size: 14px;
  margin-top: 20px;
}

.login-link a {
  color: #E9A33B;
  text-decoration: none;
  margin-left: 8px;
  font-weight: bold;
  transition: all 0.3s;
}

.login-link a:hover {
  text-decoration: underline;
  color: #d89327;
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
