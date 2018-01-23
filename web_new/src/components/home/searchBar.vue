<template>

  <div class="field is-grouped" id="home-searchbar">
    <p class="control is-expanded">
      <input class="input" type="text" v-model="inputText">
    </p>
    <p class="control">
      <a class="button is-info" :href="formatSearchUrl(inputText)" target="_blank">Search</a>
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
      if (inputText.length === 0) {
        return '/result?input=' + inputText
      } else {
        var fields = inputText.split(' ')
        var reFields = /(\/.*?:)/g
        var dict = {}
        console.log(fields)
        fields.forEach(function (query) {
          var filterCat = query.match(reFields)[0]
          filterCat = filterCat.substr(1, filterCat.length - 2)
          var filterVal = query.substr(filterCat.length + 2, query.length - 1)
          console.log(filterCat, filterVal)
          dict[filterCat] = filterVal
        })
        var queryString = $.param(dict)
        return '/result?' + queryString
      }
    }
  }
}
</script>

<style scoped>

</style>
