<template>

  <div class="field is-grouped" id="home-searchbar">
    <p class="control is-expanded">
      <input class="input" type="text" v-model="inputText">
    </p>
    <p class="control">
      <a class="button is-info" :href="formatSearchUrl(inputText)">Search</a>
    </p>
  </div>

</template>

<script>
export default {
  data () {
    return {
      inputText: ''
    }
  },

  methods: {
    formatSearchUrl: function (inputText) {
      return '/result?input=' + inputText
    }
  }
}
</script>

<style scoped>

</style>
