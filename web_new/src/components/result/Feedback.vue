<template>
  <section id="feedback">
    <!-- <div id="greyscreen">
    </div> -->
    <loading :active.sync="visible" :can-cancel="true"></loading>
    <div id="buttons">
      <button class="ui basic button" @click="learn()">Run Incremental Learning</button>
    </div>

  </section>
</template>

<script>

import axios from 'axios'
import loading from 'vue-loading-overlay'

export default {
  data() {
     return {
      visible: false
    }
  },

  components: {
    'loading': loading
  },
  methods: {
    learn: function () {
      var vm = this
      alert('Incremental learning starts, please wait patiently!')
      vm.visible = true
      axios.get('http://127.0.0.1:5000/dbtest')
        .then(function (response) {
          vm.visble = false
          if (response.data['status_code'] === 500) {
            alert(response.data['message'])
          } else {
            console.log(response.data['message'])
            window.location.reload()
            alert('Incremental Learning Finishes!')
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}

</script>

<style scoped>
#greyscreen {
  background-color: gray;
  position:absolute;
  width: 1000px;
  height: 1000px;
  z-index: 99;
  top: -800px;
  left: 0px;
}
</style>
