<template>
	<section id="result">
		<search-bar></search-bar>
	</section>
</template>

<script>

  import SearchBar from '../home/searchBar.vue'
  // import SearchFilter from './filter.vue'
  // import SearchList from './list.vue'

  export default {

    components: {
      'search-bar': SearchBar
      // 'search-filter': SearchFilter,
      // 'search-list': SearchList
    },

    data() {
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
