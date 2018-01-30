<template>
  <section id="result">
    <search-bar></search-bar>
      <div class="row" id="result-main">
        <mytable :apiUrl="apiUrl" :fields="fields" :perPage="perPage"></mytable>
      </div>
  </section>
</template>

<script>

import Table from './table.vue'
import SearchBar from '../home/searchBar.vue'
// import SearchFilter from './filter.vue'
// import RetGrid from './grid.vue'

export default {

  components: {
    'search-bar': SearchBar,
    'mytable': Table
  },

  data () {
    return {
      apiUrl: '',
      fields: [],
      perPage: 0
    }
  },

  created: function () {
    this.fields = ['ID', 'Date', 'From', 'To', 'Subject']
    this.perPage = 50
    let query = $.param(this.$route.query)
    let request = 'http://localhost:5000/enron?' + query
    console.log(request)
    this.apiUrl = request
  }
}

</script>

<style scoped>

section#result {
  margin: 2rem 2rem 2rem 2rem;
}

div#result-main {
  margin-top: 3rem;
}

</style>
