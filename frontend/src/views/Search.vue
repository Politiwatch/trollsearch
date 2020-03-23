<template>
  <section class="search">
    <h1 class="font-sans">Search results</h1>
    <SearchBox />
    <hr />
    <div v-if="loading">
      <p>Please wait... loading...</p>
    </div>
    <div v-if="!loading">
      <p>There are {{ total }} total results.</p>
      <Tweet v-for="tweet in results" :key="tweet.tweetid" :data="tweet" />
      <button @click="loadMore" v-if="results.length < total">Load more...</button>
      <p v-if="results.length >= total">No more tweets to display.</p>
    </div>
  </section>
</template>

<script>
import SearchBox from "@/components/SearchBox.vue";
import Tweet from "@/components/Tweet.vue";
import performQuery from "@/api.js";

export default {
  name: "Search",
  components: {
    SearchBox,
    Tweet
  },
  data() {
    return this.defaults();
  },
  methods: {
    defaults() {
      return {
        results: [],
        total: null,
        loading: true,
        page: 0
      };
    },
    search() {
      performQuery(
        {
          query: this.$route.query.query,
          page: this.page
        },
        resp => {
          this.results.push(...resp.results);
          this.total = resp.total;
          this.loading = false;
        }
      );
    },
    loadMore() {
      this.page++;
      this.search();
    }
  },
  created() {
    this.search();
  },
  watch: {
    "$route.query": function() {
      let defaults = this.defaults();
      Object.keys(defaults).forEach(key => {
        this[key] = defaults[key];
      });
      this.search();
    }
  }
};
</script>
