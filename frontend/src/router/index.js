import { createRouter, createWebHistory } from 'vue-router'
import ManuscriptInput from '../views/ManuscriptInput.vue'
import GenerationProgress from '../views/GenerationProgress.vue'
import PixelPreview from '../views/PixelPreview.vue'

const routes = [
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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router