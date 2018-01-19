<template>
  <section id="result">
    <search-bar></search-bar>
      <div class="row" id="result-main">
        <div class="col-lg-8">
          <my-vuetable ref="vuetable" api-url="http://localhost:5000/enron" :fields="['ID','Date', 'From', 'To', 'Subject']"></my-vuetable>
        </div>
        <div class="col-lg-4">
          <p>Email Display Here</p>
        </div>
      </div>
  </section>
</template>

<script>

import MyVuetable from 'vuetable-2/src/components/Vuetable'
import SearchBar from '../home/searchBar.vue'
// import SearchFilter from './filter.vue'
// import RetGrid from './grid.vue'

export default {

  components: {
    'search-bar': SearchBar,
    'my-vuetable': MyVuetable
  },

  data () {
    return {
      queryString: this.$route.query.input
    }
  }

}

</script>

<style scoped>

section#result {
  margin: 2rem 4rem 2rem 2rem;
}

div#result-main {
  margin-top: 3rem;
}

</style>
