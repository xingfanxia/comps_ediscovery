// CustomActions.vue
<template>
  <div class="custom-actions">
    <button class="ui basic button" @click="feedback(rowData, 1);"><i class="check icon" v-bind:class="{ CActive: isCActive }"></i></button>
    <button class="ui basic button" @click="feedback(rowData, 0);"><i class="x icon" v-bind:class="{ XActive: isXActive }"></i></button>
  </div>
</template>

<script>

import axios from 'axios'

export default {
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
      isXActive: false
    }
  },

  methods: {
    feedback: function (rowData, relevant) {
      var vm = this

      if ((relevant === 0 && vm.isCActive) || (relevant === 1 && vm.isXActive)) {
        alert("Can't select both!")
        return
      }

      axios.post('http://127.0.0.1:5000/feedback', {
        'ID': rowData.ID,
        'Relevant': relevant
      })
        .then(function (response) {
          console.log(response.data['message'])
          if (relevant === 1) {
            vm.isCActive = !vm.isCActive
            rowData.Relevant = 1
          } else {
            vm.isXActive = !vm.isXActive
            rowData.Relevant = 0
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    itemAction: function (rowData, rowIndex) {
      console.log(rowData, rowIndex)
    }
  },

  watch: {
    rowData: function (oldVal, newVal) {
      // console.log(oldVal, newVal)
      console.log(newVal.Relevant)
      var relevancyCheck = parseFloat(newVal.Relevant)
      if ((relevancyCheck === -1) || (relevancyCheck < 1 && relevancyCheck > 0)) {
        console.log('unmarked')
        // this.isCActive = false
        // this.isXActive = false
        $('.check').removeClass('CActive')
        $('.x').removeClass('XActive')
      } else if (relevancyCheck === 1) {
        // this.isCActive = true
        // this.isXActive = false
        $('.check').addClass('CActive')
        $('.x').removeClass('XActive')
      } else if (relevancyCheck === 0) {
        // this.isXActive = true
        // this.isCActive = false
        $('.check').removeClass('CActive')
        $('.x').addClass('XActive')
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
