/**
 * 用户认证相关 API
 * 对接后端 Flask 认证接口
 */
import request from '@/utils/request'

/**
 * 用户注册
 * @param {object} data - 注册信息
 * @param {string} data.username - 用户名
 * @param {string} data.password - 密码
 * @param {string} [data.email] - 邮箱（可选）
 * @returns {Promise}
 */
export function register(data) {
  return request({
    url: '/api/v1/auth/register',
    method: 'post',
    data
  })
}

/**
 * 用户登录
 * @param {object} data - 登录信息
 * @param {string} data.username - 用户名
 * @param {string} data.password - 密码
 * @returns {Promise}
 */
export function login(data) {
  return request({
    url: '/api/v1/auth/login',
    method: 'post',
    data
  })
}

/**
 * 获取当前用户信息
 * @returns {Promise}
 */
export function getUserInfo() {
  return request({
    url: '/api/v1/auth/user',
    method: 'get'
  })
}

/**
 * 刷新 Token
 * @param {string} token - 当前的 Token
 * @returns {Promise}
 */
export function refreshToken(token) {
  return request({
    url: '/api/v1/auth/refresh',
    method: 'post',
    data: { token }
  })
}

/**
 * 游客登录
 * @returns {Promise}
 */
export function guestLogin() {
  return request({
    url: '/api/v1/auth/guest',
    method: 'post'
  })
}
