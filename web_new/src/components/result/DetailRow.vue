<template>
  <div @click="onClick" id="overCon">
    <div class="inline field" id="msgCon">
      <label>Email Content:</label>
      <hr>
      <div class="code" v-html="spanMessage"></div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'

export default {

  data () {
    return {
      spanMessage: this.rowData['Message_Contents']
    }
  },

  mounted: function () {
    axios.get('http://127.0.0.1:5000/topics')
      .then(response => {
        for (var key in response.data) {
          // check if the property/key is defined in the object itself, not in parent
          if (response.data.hasOwnProperty(key)) {
            var wordList = response.data[key]
            for (var i in wordList) {
              var word = wordList[i]
              var wordRegex = new RegExp('\\b' + word + '\\b', 'gi')
              var wordSpan = '<span class=topic_' + key + ' title="topic ' + key + '">' + word + '</span>'
              this.spanMessage = this.spanMessage.replace(wordRegex, wordSpan)
            }
          }
        }
      })
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

  methods: {
    onClick (event) {
      console.log('my-detail-row: on-click', event.target)
    }
  }
}

</script>

<style scoped>

.code {
  font-family: monospace;
  white-space: pre-wrap;      /* css-3 */
}

#msgCon {
  border: 1px solid #ccc;
  display: block;
  font-size: 15px;
  padding: 5px;
  /*text-transform: uppercase;*/
  /*color: #abb2c0;*/
}

hr {
  margin-top: 0.1rem;
  margin-bottom: 0.5rem;
}

span {
  background-color: yellow;
}

</style>
