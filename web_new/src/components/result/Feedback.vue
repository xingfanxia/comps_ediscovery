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
          if (response.data['status_code'] === 500) {
            alert(response.data['message'])
          } else {
            console.log(response.data['message'])
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}

</script>
