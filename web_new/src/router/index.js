import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import Home from '@/components/home/home.vue'
import Result from '../components/result/home.vue'
// import Detail from '../components/detail/home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/result',
      name: 'result',
      component: Result
    }
    // {
    //   path: '/detail',
    //   name: 'detail',
    //   component: Detail
    // }
  ]
})
