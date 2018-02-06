<template>
  <section id="feedback">
    <div id="buttons">
      <button class="ui basic button" @click="learn()">Run Incremental Learning</button>
    </div>
  </section>
</template>

<script>

import axios from 'axios'

export default {
  methods: {
    learn: function () {
      alert('Incremental learning starts, please wait patiently!')
      axios.get('http://127.0.0.1:5000/dbtest')
        .then(function (response) {
          // REPOPULATE TABLE HERE YA DIG
          alert(response.data['message'])
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}

</script>
