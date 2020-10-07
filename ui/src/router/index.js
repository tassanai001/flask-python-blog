import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/create-blog', component: 'CreateBlog' },
  { path: '/update-blog/:id', component: 'UpdateBlog' },
  { path: '/:title/:id', component: 'Detail' },
  {
    path: '*',
    name: 'Not Found',
    component: 'NotFound'
  }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
  routes,
  mode: 'history'
})
