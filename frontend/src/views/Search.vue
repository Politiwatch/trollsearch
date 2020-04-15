<template>
  <section class="search md:flex">
    <aside
      class="md:w-1/3 mb-4 overflow-y-auto pr-4 py-8 pl-1 md:sticky top-0 h-auto self-start"
    >
      <SearchBox />
    </aside>
    <main class="md:w-2/3 md:pl-12">
      <div v-if="loading">
        <p>Please wait... loading...</p>
      </div>
      <div v-if="!loading">
        <p>There are {{ total.toLocaleString() }} total results.</p>
        <Tweet v-for="tweet in results" :key="tweet.tweetid" :data="tweet" />
        <button @click="loadMore" v-if="results.length < total">
          Load more...
        </button>
        <p v-if="results.length >= total">No more tweets to display.</p>
      </div>
    </main>
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
      let params = {
        page: this.page,
      };
      for (let key of Object.keys(this.$route.query)) {
        params[key] = this.$route.query[key];
      }
      performQuery(
        params,
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
