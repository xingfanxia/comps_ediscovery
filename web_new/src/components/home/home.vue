<template>

  <section class="section" id="home-section">
    <div class="container">
      <h1 class="title has-text-centered"><span>Lunch at Enron:</span></h1>
      <h1 class="title has-text-centered">The Emails</h1>
      <search-bar></search-bar>
    </div>

    <div class="content" id="download">
      <div class="columns">
        <div class="exquery column is-6-desktop is-offset-3-desktop is-10-tablet is-offset-1-tablet is-10-mobile is-offset-1-mobile">
          <p><span>Getting Started</span></p>
          <p><i>Filter by Subject and Message Contents &emsp;&emsp;</i></p>
          <a class="button explore" href="/result?Subject=lunch&Message_Contents=lunch">Explore >></a>
          <pre><code class="bash">/Subject:'lunch' /Message_Contents:'lunch' </code></pre>

          <p><i>Filter by Subject and Person &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;</i></p>
          <a class="button explore" href="/result?Subject=lunch&From=susan.scott%40enron.com">Explore >></a>
          <pre><code class="bash">/Subject:'lunch' /From:'susan.scott@enron.com'</code></pre>
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
  color: #0B5091;
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

.exquery span {
  color: #0B5091;
  font-size: 45px;
  text-align: center;
}

.exquery p {
    font-size: 20px;
    display: inline-block;
}

.explore {
    display: inline-block;
    margin-top: 10px;
    color: #fff;
    background-color: #0B5091;
    border-color: #0B5091;
    border-radius: 4px;
}

div#download {
  margin-top: 2rem;
}

#download p {
  margin-top: 1rem;
}

</style>
