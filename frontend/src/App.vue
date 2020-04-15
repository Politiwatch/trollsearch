<template>
  <section class="container min-h-screen mx-auto max-w-2xl lg:my-30 py-12">
    <router-view v-if="!loading && !error" />

    <article class="card ~critical !high content max-w-lg mx-auto" v-if="error">
      <h3>An error occured</h3>
      <p>
        Something went wrong while trying to load the page. Try again, or check
        the console for details.
      </p>
    </article>

    <span class="loading" v-if="loading" title="Loading..."></span>
  </section>
</template>

<script>
import {getStats} from "./api";

export default {
  name: "App",
  data() {
    return {
      loading: true,
      error: false,
    };
  },
  methods: {
    loadInitialData() {
      getStats(
        result => {
          localStorage.setItem("stats", JSON.stringify(result));
          this.stats = result;
          this.loading = false;
        },
        error => {
          console.error(error);
          this.loading = false;
          this.error = true;
        }
      );
    },
  },
  created() {
    this.loadInitialData();
  },
};
</script>
