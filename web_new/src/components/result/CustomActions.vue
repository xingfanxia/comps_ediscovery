// CustomActions.vue
<template>
  <div class="custom-actions">
    <button class="ui basic button" @click="feedback(rowData, 1)"><i class="check icon"></i></button>
    <button class="ui basic button" @click="feedback(rowData, 0)"><i class="x icon"></i></button>
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
  methods: {
    feedback: function (rowData, relevant) {
      axios.post('http://127.0.0.1:5000/feedback', {
        'ID': rowData.ID,
        'Relevant': relevant
      })
        .then(function (response) {
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
</style>
