/**
 * Axios 实例配置与拦截器
 * 负责自动注入 Token 和处理 401 响应
 */
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuth } from '@/stores/auth'
import router from '@/router'

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * 请求拦截器
 * 自动在请求头中注入 Authorization Token
 */
request.interceptors.request.use(
  (config) => {
    const { getToken } = useAuth()
    const token = getToken()
    
    // 如果存在 token，则注入到请求头
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    console.error('请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 * 统一处理响应错误，特别是 401 未授权错误
 */
request.interceptors.response.use(
  (response) => {
    // 直接返回 data 部分
    return response.data
  },
  (error) => {
    // 处理网络错误
    if (!error.response) {
      ElMessage.error('网络连接失败，请检查您的网络设置')
      return Promise.reject(error)
    }

    const { status, data } = error.response

    // 处理 401 未授权错误（Token 过期或无效）
    if (status === 401) {
      const { clearAuth } = useAuth()
      
      // 清除本地认证信息
      clearAuth()
      
      // 提示用户重新登录
      ElMessage.warning('登录已过期，请重新登录')
      
      // 跳转到登录页
      router.push({
        path: '/login',
        query: { redirect: router.currentRoute.value.fullPath }
      })
      
      return Promise.reject(new Error('未授权访问'))
    }

    // 处理其他错误
    const errorMessage = data?.msg || data?.message || '请求失败，请稍后重试'
    ElMessage.error(errorMessage)
    
    return Promise.reject(error)
  }
)

export default request
