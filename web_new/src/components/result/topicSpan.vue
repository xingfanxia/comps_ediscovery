<template>
  <span id='topicIdx'> {{ topic }} </span>
  <div id='tooltip'>
  	{{ topic }}
  </div>
</template>

<script>

import axios from 'axios'

export default {

  // data () {
  // 	return {
  // 		topic,
  // 		importance:
  // 	}
  // },

  props: {
    topic: {
      type: String,
      required: true
    },
    importance: {
      type: Number
    }
  },

  methods: {
  }
}

</script>

<style scoped>

#tooltip {
  border: 1px solid #ccc;
  display: none;
  font-size: 15px;
  margin-top: 10px;
  padding: 5px;
  text-transform: uppercase;
  background-color: #f5f5f5;
}

#topicIdx:hover #tooltip {
	display: block;
}
</style>
