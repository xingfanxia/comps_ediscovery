// CustomActions.vue
<template>
  <div class="custom-actions">
    <button class="ui basic button" @click="feedback(rowData, 1, 0);"><i class="check icon" v-bind:class="{ CActive: isCActive }"></i></button>
    <button class="ui basic button" @click="feedback(rowData, 0, 1);"><i class="x icon" v-bind:class="{ XActive: isXActive }"></i></button>
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
    feedback: function (rowData, relevant, flag) {
      var vm = this;

      axios.post('http://127.0.0.1:5000/feedback', {
        'ID': rowData.ID,
        'Relevant': relevant
      })
        .then(function (response) {
          console.log(response.data['message'])
          if (flag === 0) {
            vm.isCActive = !vm.isCActive
          } else {
            vm.isXActive = !vm.isXActive
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    itemAction: function (rowData, rowIndex) {
      console.log(rowData, rowIndex)
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
