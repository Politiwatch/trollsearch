<template>
  <section class="search md:flex">
    <div v-if="loading">
      <p>Please wait... loading...</p>
    </div>
    <div v-if="!loading">
      <p class="pb-8 text-center">There are {{ total.toLocaleString() }} total results.</p>
      <SearchStats :languages="languages" :hashtags="hashtags" :archives="archives" :total="total" />
      <hr class="h-8 sep" />
      <Tweet v-for="tweet in results" :key="tweet.tweetid" :data="tweet" />
      <button @click="loadMore" v-if="results.length < total" class="button ~urge" :class="{ loading: searching }">Load more...</button>
      <p v-if="results.length >= total">No more tweets to display.</p>
    </div>
  </section>
</template>

<script>
import SearchStats from "@/components/SearchStats.vue";
import Tweet from "@/components/Tweet.vue";
import performQuery from "@/api.js";

export default {
  name: "Search",
  components: {
    Tweet,
    SearchStats
  },
  data() {
    return this.defaults();
  },
  methods: {
    defaults() {
      return {
        results: [],
        total: null,
        archives: {},
        languages: {},
        hashtags: {},
        loading: true,
        searching: true,
        page: 0
      };
    },
    search() {
      this.searching = true;
      let params = {
        page: this.page
      };
      for (let key of Object.keys(this.$route.query)) {
        params[key] = this.$route.query[key];
      }
      performQuery(params, resp => {
        this.results.push(...resp.results);
        this.archives = resp.archives;
        this.languages = resp.languages;
        console.log(resp.languages);
        this.hashtags = resp.hashtags;
        this.total = resp.total;
        this.loading = false;
        this.searching = false;
      });
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
