// CustomActions.vue
<template>
  <div class="custom-actions">
    <scale-loader :loading="loading" :color="color" :size="size"></scale-loader>
    <button class="ui basic button" @click="feedback(rowData, 1);"><i class="check icon" v-bind:class="{ CActive: isCActive }"></i></button>
    <button class="ui basic button" @click="feedback(rowData, 0);"><i class="x icon" v-bind:class="{ XActive: isXActive }"></i></button>
  </div>
</template>

<script>

import axios from 'axios'
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'

export default {
  components: {
    ScaleLoader
  },

  props: {
    rowData: {
      type: Object,
      required: true
    },
    rowIndex: {
      type: Number
    }
  },

  data () {
    return {
      isCActive: false,
      isXActive: false,
      loading: false,
      color: '#0B5091',
      size: '20px'
    }
  },

  methods: {
    feedback: function (rowData, flag) {
      var vm = this
      var relevant = -1

      if (flag === rowData.Relevant) {
        relevant = -1
      } else {
        relevant = flag
      }
      vm.loading = true
      axios.post('http://127.0.0.1:5000/feedback', {
        'ID': rowData.ID,
        'Relevant': relevant
      })
        .then(function (response) {
          vm.loading = false
          console.log(response.data['message'])
          if (relevant === 1) {
            vm.isXActive = false
            vm.isCActive = true
          } else if (relevant === 0) {
            vm.isXActive = true
            vm.isCActive = false
          } else {
            vm.isXActive = false
            vm.isCActive = false
          }
          rowData.Relevant = relevant
        })
        .catch(function (error) {
          vm.loading = false
          console.log(error)
        })
    },
    itemAction: function (rowData, rowIndex) {
      console.log(rowData, rowIndex)
    }
  },

  watch: {
    rowData: function (newVal, oldVal) {
      // console.log(newVal, oldVal)
      console.log(newVal.Relevant)
      var relevancyCheck = parseFloat(newVal.Relevant)
      if ((relevancyCheck === -1) || (relevancyCheck < 1 && relevancyCheck > 0)) {
        console.log('unmarked')
        this.isCActive = false
        this.isXActive = false
        // $('.check').removeClass('CActive')
        // $('.x').removeClass('XActive')
      } else if (relevancyCheck === 1) {
        console.log('checked')
        this.isCActive = true
        this.isXActive = false
        // $('.check').addClass('CActive')
        // $('.x').removeClass('XActive')
      } else if (relevancyCheck === 0) {
        console.log('x ed')
        this.isXActive = true
        this.isCActive = false
        // $('.check').removeClass('CActive')
        // $('.x').addClass('XActive')
      }
      this.$forceUpdate()
    }
  }
}
</script>

<style>
  .custom-actions button.ui.button {
    padding: 8px 8px;
  }

  .custom-actions button.ui.button > i.icon {
    margin: auto !important;
  }

  i {
    color: rgba(0, 0, 0, 0.1);
  }

  .CActive {
    color: rgba(0, 0, 0, 1);
  }

  .XActive {
    color: rgba(0, 0, 0, 1);
  }
</style>
