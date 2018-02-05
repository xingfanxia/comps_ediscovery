<template>
  <div>
    <app-header></app-header>
    <transition name="pageload" mode="out-in">
      <router-view></router-view>
    </transition>
    <app-footer></app-footer>
  </div>
</template>

<script>

import Header from './components/home/header.vue'
import Footer from './components/home/footer.vue'

export default {
  components: {
    'app-header': Header,
    'app-footer': Footer
  }
}

</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.pageload-enter-active, .pageload-leave-active {
  transition: opacity .5s ease;
}
.pageload-enter, .pageload-leave-to {
  opacity: 0;
}

</style>
