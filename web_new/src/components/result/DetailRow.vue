<template>
  <div @click="onClick" id="overCon">
    <div class="row">
      <div class="inline field col-lg-8" id="msgCon">
        <label>Email Content:</label>
        <hr>
        <div class="code" v-html="spanMessage"></div>
      </div>
      <div class="col-lg-4 metaInfo inline field" id="msgCon">
       <label>Topic Metadata:</label>
        <hr>
        <mytable :apiUrl="apiUrl" :fields="fields"></mytable>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import Vuetable from 'vuetable-2/src/components/Vuetable'

export default {

  components: {
    'mytable': Vuetable
  },

  data () {
    return {
      spanMessage: this.rowData['Message_Contents'].replace(/&/g, '&amp;')
                                                   .replace(/</g, '&lt;')
                                                   .replace(/>/g, '&gt;')
                                                   .replace(/"/g, '&quot;')
                                                   .replace(/'/g, '&#039;'),
      // topicMeta: '',
      apiUrl: 'http://127.0.0.1:5000/topic_table',
      fields: ['topic', 'terms']
    }
  },

  mounted: function () {
    // this.topicMeta = 'some meta data'
    axios.get('http://127.0.0.1:5000/topics')
      .then(response => {
        console.log(response)
        this.topicMeta = response.data['0']
        for (var key in response.data) {
          // check if the property/key is defined in the object itself, not in parent
          if (response.data.hasOwnProperty(key)) {
            var word = key
            var wordRegex = new RegExp('\\b' + word + '\\b', 'gi')
            var topic = response.data[key][1]
            var wordSpan = '<span class=topic_' + topic + ' title="topic   ' + topic + '">' + word + '</span>'
            this.spanMessage = this.spanMessage.replace(wordRegex, wordSpan)
            console.log(this.spanMessage)
          }
        }
      })
    // axios.get('http://127.0.0.1:5000/span_data/' + this.rowData['ID'])
    //   .then(response => {
    //     for (var key in response.data) {
    //       console.log(key)
    //       // check if the property/key is defined in the object itself, not in parent
    //       if (response.data.hasOwnProperty(key)) {
    //           var word = key
    //           var wordRegex = new RegExp('\\b' + word + '\\b', 'gi')
    //           var topic = response.data[key][1]
    //           var wordSpan = '<span class=topic_' + topic + ' title="topic ' + topic + '">' + word + '</span>'
    //           this.spanMessage = this.spanMessage.replace(wordRegex, wordSpan)
    //         }
    //       }
    //   })
  },

  updated: function () {
    axios.get('http://127.0.0.1:5000/pred_meta/' + this.rowData['ID'])
      .then(response => {
        for (var key in response.data) {
          if (response.data.hasOwnProperty(key)) {
            var alpha = response.data[key]
            console.log(alpha)
            if (alpha < 0) {
              $('.topic_' + key).css('background-color', 'rgba(255, 0, 0, ' + Math.abs(alpha) * 10 + ')')
            } else {
              $('.topic_' + key).css('background-color', 'rgba(0, 255, 0, ' + Math.abs(alpha) * 10 + ')')
            }
            $('.topic_' + key).css('border-radius', '5px').css('padding', '1px')
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
    },
    showTooltip (key) {
      console.log(key)
    },
    hideTooltip () {
      console.log('yolo')
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
  border: 2px solid #ccc;
  display: block;
  font-size: 15px;
  padding: 5px;
  height: 100%;
  /*text-transform: uppercase;*/
  /*color: #abb2c0;*/
}

hr {
  margin-top: 0.1rem;
  margin-bottom: 0.5rem;
}

</style>
