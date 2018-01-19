<template>

  <section class="section" id="home-section">
    <div class="container">
      <h1 class="title has-text-centered"><span>Put</span> Your Inquery</h1>
      <h2 class="subtitle has-text-centered">
        Search for whatever you want in whatever format you want
      </h2>
      <search-bar></search-bar>
    </div>

    <div class="content" id="download">
      <p class="has-text-centered">Here are some example queries</p>
      <div class="columns">
        <div class="column is-6-desktop is-offset-3-desktop is-10-tablet is-offset-1-tablet is-10-mobile is-offset-1-mobile">
          <p>Example Queries 1</p>
          <pre v-highlightjs><code class="bash">key term sort by :category</code></pre>
          <p>Example Queries 2</p>
          <pre v-highlightjs><code class="bash">key term sort by :confidence</code></pre>
          <p>Example Queries 3</p>
          <pre v-highlightjs><code class="bash">key term sort by :relevance</code></pre>
        </div>
      </div>

    </div>
  </section>
</template>

<script>
import SearchBar from './searchBar.vue'
export default {

  components: {
    'search-bar': SearchBar
  }

}

</script>

<style scoped>

.container h1 {
  font-size: 6rem;
}

.container span {
  color: darkcyan;
  /*font-size: 5.5rem;*/
}

.container h2 {
  /*font-size: 1.2rem;*/
}

section#home-section {
  min-height: 400px;
}

div#home-searchbar {
  margin: 0 4rem;
}

#home-searchbar input {
  height: 3rem;
}
#home-searchbar a.button {
  height: 3rem;
  width: 8rem;
}

div#download {
  margin-top: 2rem;
}

#download p {
  margin-top: 1rem;
}

</style>
