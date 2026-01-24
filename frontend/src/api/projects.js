/**
 * 项目和草稿管理相关 API
 * 对接后端 Flask 项目管理接口
 */
import request from '@/utils/request'

/**
 * 保存草稿（新建或更新）
 * @param {object} data - 草稿数据
 * @param {string} [data.draft_id] - 草稿ID（更新时传入，新建时不传）
 * @param {string} data.title - 草稿标题
 * @param {object} data.manuscript - 原稿数据
 * @returns {Promise}
 */
export function saveDraft(data) {
  return request({
    url: '/api/v1/projects/drafts',
    method: 'post',
    data
  })
}

/**
 * 获取草稿列表
 * @returns {Promise}
 */
export function getDraftList() {
  return request({
    url: '/api/v1/projects/drafts',
    method: 'get'
  })
}

/**
 * 获取草稿详情
 * @param {string} draftId - 草稿ID
 * @returns {Promise}
 */
export function getDraftDetail(draftId) {
  return request({
    url: `/api/v1/projects/drafts/${draftId}`,
    method: 'get'
  })
}

/**
 * 删除草稿
 * @param {string} draftId - 草稿ID
 * @returns {Promise}
 */
export function deleteDraft(draftId) {
  return request({
    url: `/api/v1/projects/drafts/${draftId}`,
    method: 'delete'
  })
}

/**
 * 保存项目（新建或更新）
 * @param {object} data - 项目数据
 * @param {string} [data.project_id] - 项目ID（更新时传入，新建时不传）
 * @param {string} data.title - 项目标题
 * @param {object} data.game_data - 游戏数据
 * @param {string} data.status - 项目状态（draft/editing/published）
 * @returns {Promise}
 */
export function saveProject(data) {
  return request({
    url: '/api/v1/projects/',
    method: 'post',
    data
  })
}

/**
 * 获取项目列表
 * @param {string} [status] - 状态过滤（可选）
 * @returns {Promise}
 */
export function getProjectList(status) {
  let url = '/api/v1/projects/'
  if (status) {
    url += `?status=${status}`
  }
  return request({
    url,
    method: 'get'
  })
}

/**
 * 获取项目详情
 * @param {string} projectId - 项目ID
 * @returns {Promise}
 */
export function getProjectDetail(projectId) {
  return request({
    url: `/api/v1/projects/${projectId}`,
    method: 'get'
  })
}

/**
 * 删除项目
 * @param {string} projectId - 项目ID
 * @returns {Promise}
 */
export function deleteProject(projectId) {
  return request({
    url: `/api/v1/projects/${projectId}`,
    method: 'delete'
  })
}

/**
 * 更新项目状态
 * @param {string} projectId - 项目ID
 * @param {string} status - 新状态
 * @returns {Promise}
 */
export function updateProjectStatus(projectId, status) {
  return request({
    url: `/api/v1/projects/${projectId}/status`,
    method: 'put',
    data: { status }
  })
}
