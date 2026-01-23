import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ManuscriptInput from '../views/ManuscriptInput.vue'
import GenerationProgress from '../views/GenerationProgress.vue'
import PixelPreview from '../views/PixelPreview.vue'
import VisualEditor from '../views/VisualEditor.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/home',
    name: 'HomePage',
    component: Home
  },
  {
    path: '/manuscript-input',
    name: 'ManuscriptInput',
    component: ManuscriptInput
  },
  {
    path: '/generation-progress',
    name: 'GenerationProgress',
    component: GenerationProgress
  },
  {
    path: '/pixel-preview',
    name: 'PixelPreview',
    component: PixelPreview
  },
  {
    path: '/visual-editor',
    name: 'VisualEditor',
    component: VisualEditor
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router