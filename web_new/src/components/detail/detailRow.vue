<template>
  <div @click="onClick">
    <div class="inline field">
      <label>Email Content: </label>
      <span>{{rowData.Date}}</span>
    </div>
  </div>
</template>

<script>

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
    onClick (event) {
      console.log('my-detail-row: on-click', event.target)
    }
  }
}

</script>
