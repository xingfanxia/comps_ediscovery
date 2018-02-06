// CustomActions.vue
<template>
  <div class="custom-actions">
    <button class="ui basic button" @click="feedback(rowData, 1); isCActive = !isCActive"><i class="check icon" v-bind:class="{ CActive: isCActive }"></i></button>
    <button class="ui basic button" @click="feedback(rowData, 0); isXActive = !isXActive"><i class="x icon" v-bind:class="{ XActive: isXActive }"></i></button>
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
      axios.post('http://127.0.0.1:5000/feedback', {
        'ID': rowData.ID,
        'Relevant': relevant
      })
        .then(function (response) {
          console.log(response.data['message'])
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
  .CActive {
    color: #99c778;
  }

  .XActive {
    color: #c2333c;
  }
</style>
