<template>

  <div class="field is-grouped" id="home-searchbar">
    <select v-model="selected">
      <option v-for="(option, index) in options" :value="option.value" :key='index'>
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
        {text: 'Date', value: '/Date:\'\''},
        {text: 'From', value: '/From:\'\''},
        {text: 'To', value: '/To:\'\''},
        {text: 'Subject', value: '/Subject:\'\''},
        {text: 'Message Contents', value: '/Message_Contents:\'\''},
        {text: 'ID', value: '/ID:\'\''}
      ]
    }
  },

  methods: {
    formatSearchUrl: function (inputText) {
      if (inputText.length === 0) {
        return '/result?input=' + inputText
      } else {
        var dict = {}
        var reFields = /(\/.*?:)/g
        var reValues = /'(.*?)'/g
        var filters = inputText.match(reFields)
        var values = inputText.match(reValues)
        for (var i = 0; i < filters.length; i++) {
          var filterTrimmed = filters[i].substr(1).slice(0, -1)
          var valueTrimmed = values[i].substr(1).slice(0, -1)
          dict[filterTrimmed] = valueTrimmed
        }
        console.log(dict)
        return '/result?' + $.param(dict)
      }
    }
  },

  watch: {
    selected (newValue) {
      if (this.inputText.length === 0) {
        if (this.inputText.indexOf(this.selected) === -1) {
          this.inputText = this.inputText + this.selected
        } else {
          alert('this field has already added')
        }
      } else {
        if (this.inputText.indexOf(this.selected) === -1) {
          this.inputText = this.inputText + ' ' + this.selected
        } else {
          alert('this field has already added')
        }
      }
    }
  }

}
</script>

<style scoped>

</style>
