<template>
  <div @click="onClick" id="overCon">
    <div class="inline field" id="msgCon">
      <label>Email Content:</label>
      <hr>
      <pre>{{rowData['Message_Contents']}}</pre>
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

<style scoped>

pre {
 white-space: pre-wrap;       /* css-3 */
 white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
 white-space: -pre-wrap;      /* Opera 4-6 */
 white-space: -o-pre-wrap;    /* Opera 7 */
 word-wrap: break-word;       /* Internet Explorer 5.5+ */
}

#msgCon {
  border: 1px solid #ccc;
  display: block;
  font-size: 15px;
  padding: 5px;
  text-transform: uppercase;
  background-color: #BABABA;
  /*color: #abb2c0;*/
}

hr {
  margin-top: 0.1rem;
  margin-bottom: 0.5rem;
}

</style>
