import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import ManuscriptInput from '../views/ManuscriptInput.vue'
import GenerationProgress from '../views/GenerationProgress.vue'
import PixelPreview from '../views/PixelPreview.vue'
import VisualEditor from '../views/VisualEditor.vue'
import GamePreview from '../views/GamePreview.vue'
import Profile from '../views/Profile.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: false }
  },
  {
    path: '/home',
    name: 'HomePage',
    component: Home,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/manuscript-input',
    name: 'ManuscriptInput',
    component: ManuscriptInput,
    meta: { requiresAuth: true }
  },
  {
    path: '/generation-progress',
    name: 'GenerationProgress',
    component: GenerationProgress,
    meta: { requiresAuth: true }
  },
  {
    path: '/pixel-preview',
    name: 'PixelPreview',
    component: GamePreview,
    meta: { requiresAuth: true }
  },
  {
    path: '/visual-editor',
    name: 'VisualEditor',
    component: VisualEditor,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/game-preview',
    name: 'GamePreview',
    component: GamePreview,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/**
 * 全局路由守卫
 * 拦截需要权限的页面，未登录用户重定向至登录页
 */
router.beforeEach((to, from, next) => {
  const { isLoggedIn } = useAuth()
  
  // 检查目标路由是否需要登录权限
  if (to.meta.requiresAuth && !isLoggedIn.value) {
    // 未登录，提示并跳转到登录页
    ElMessage.warning('请先登录')
    next({
      path: '/login',
      query: { redirect: to.fullPath } // 保存目标路径，登录后跳转
    })
  } else if ((to.path === '/login' || to.path === '/register') && isLoggedIn.value) {
    // 已登录用户访问登录/注册页，重定向到首页
    next('/')
  } else {
    // 放行
    next()
  }
})

export default router