<template>
  <div>
    <nav class="py-8 section ~urge !high w-full px-8">
      <div class="max-w-3xl mx-auto">
        <div class="text-center">
        <h2 class="tracking-wide uppercase heading">
          <router-link to="/">Twitter Disinformation Archives</router-link>
        </h2>
        <p class="supra">
          By <a href="https://politiwatch.org">Politiwatch</a>
        </p>
        </div>
        <div class="mt-8 mb-4">
          <SearchBox />
        </div>
      </div>
    </nav>
    <section class="container max-w-3xl min-h-screen py-12 mx-auto lg:my-30">
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
  </div>
</template>

<script>
import { getStats } from "./api";
import SearchBox from "@/components/SearchBox.vue";

export default {
  name: "App",
  components: {
    SearchBox
  },
  data() {
    return {
      loading: true,
      error: false
    };
  },
  methods: {
    loadInitialData() {
      getStats(
        result => {
          let stats = {
            archiveNames: result["archives"].map(x => x.name),
            ...result
          };
          localStorage.setItem("stats", JSON.stringify(stats));
          this.stats = stats;
          this.loading = false;
        },
        error => {
          console.error(error);
          this.loading = false;
          this.error = true;
        }
      );
    }
  },
  created() {
    this.loadInitialData();
  }
};
</script>
