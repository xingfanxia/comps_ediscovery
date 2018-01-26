<template>

  <div class="field is-grouped" id="home-searchbar">
    <select v-model="selected">
      <option v-for="option in options" v-bind:value="option.value">
        {{ option.text }}
      </option>
    </select>
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
      inputText: '',
      selected: '',
      options: [
        {text: 'Date', value: '/Date:'},
        {text: 'From', value: '/From:'},
        {text: 'To', value: '/To:'},
        {text: 'Subject', value: '/Subject:'},
        {text: 'Message Contents', value: '/Message_Contents:'},
        {text: 'ID', value: '/ID:'}
      ]
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
  },

  watch: {
    selected (newValue) {
      this.inputText = this.inputText + this.selected
    }
  }
}
</script>

<style scoped>

</style>
