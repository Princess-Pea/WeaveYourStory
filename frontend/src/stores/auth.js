/**
 * 用户认证状态管理
 * 使用 Vue3 Composition API 实现轻量级状态管理
 */
import { reactive, computed } from 'vue'

// 全局认证状态
const authState = reactive({
  token: localStorage.getItem('token') || null,
  userInfo: JSON.parse(localStorage.getItem('userInfo') || 'null')
})

/**
 * 用户认证状态管理 Hook
 */
export function useAuth() {
  // 计算属性：是否已登录
  const isLoggedIn = computed(() => !!authState.token)

  /**
   * 设置登录信息
   * @param {string} token - JWT Token
   * @param {object} userInfo - 用户信息（包含username、user_id、email）
   */
  const setAuth = (token, userInfo) => {
    authState.token = token
    authState.userInfo = userInfo
    
    // 持久化到 localStorage
    localStorage.setItem('token', token)
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
  }

  /**
   * 清除登录信息（退出登录）
   */
  const clearAuth = () => {
    authState.token = null
    authState.userInfo = null
    
    // 清除 localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  /**
   * 获取当前 Token
   * @returns {string|null}
   */
  const getToken = () => authState.token

  /**
   * 获取当前用户信息
   * @returns {object|null}
   */
  const getUserInfo = () => authState.userInfo

  return {
    isLoggedIn,
    token: computed(() => authState.token),
    userInfo: computed(() => authState.userInfo),
    setAuth,
    clearAuth,
    getToken,
    getUserInfo
  }
}
