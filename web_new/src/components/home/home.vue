<template>

  <section class="section" id="home-section">
    <div class="container">
      <h1 class="title has-text-centered"><span>Explore</span></h1>
      <h1 class="title has-text-centered">the Enron Dataset</h1>
      <date-picker></date-picker>
      <search-bar></search-bar>
    </div>

    <div class="content" id="download">
      <div class="columns">
        <div class="column is-6-desktop is-offset-3-desktop is-10-tablet is-offset-1-tablet is-10-mobile is-offset-1-mobile">
          <p>Example Query 1</p>
          <p><i>Emails with recipient email address containing 'monika'</i></p>
          <pre><code class="bash">/To:'Monika'</code></pre>

          <p>Example Query 2</p>
          <p><i>Emails from 'david.allan@enron.com' with 'lunch' in message contents</i></p>
          <pre><code class="bash">/From:'david.allan@enron.com' /Message_Contents:'lunch' </code></pre>

          <p>Example Query 3</p>
          <p><i>Emails from 'monika.causholli@enron.com' to 'david.allan@enron.com"</i></p>
          <pre><code class="bash">/To:'david.allan@enron.com' /From:'monika.causholli@enron.com'</code></pre>
        </div>
      </div>

    </div>
  </section>
</template>

<script>
import SearchBar from './searchBar.vue'
import Datepicker from './datepicker.vue'
export default {

  components: {
    'search-bar': SearchBar,
    'date-picker': Datepicker
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

div#download {
  margin-top: 2rem;
}

#download p {
  margin-top: 1rem;
}

</style>
