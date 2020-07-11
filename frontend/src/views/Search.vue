<template>
  <section class="search md:flex">
    <main class="md:w-2/3 md:pl-12">
      <div v-if="loading">
        <p>Please wait... loading...</p>
      </div>
      <div v-if="!loading">
        <p class="pt-8 pb-4">There are {{ total.toLocaleString() }} total results.</p>
        <Tweet v-for="tweet in results" :key="tweet.tweetid" :data="tweet" />
        <button @click="loadMore" v-if="results.length < total">
          Load more...
        </button>
        <p v-if="results.length >= total">No more tweets to display.</p>
      </div>
    </main>
    <aside
      class="top-0 self-start h-auto py-8 pl-1 pr-4 mb-4 overflow-y-auto md:w-1/3 md:sticky"
    >
      <hr class="h-6 sep">
      <SearchStats :languages="languages" :hashtags="hashtags" :archives="archives" :total="total" />
    </aside>
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
    SearchStats,
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
        page: 0
      };
    },
    search() {
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
        this.hashtags = resp.hashtags;
        this.total = resp.total;
        this.loading = false;
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
