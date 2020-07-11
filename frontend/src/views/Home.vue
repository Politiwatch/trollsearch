<template>
  <div class="content">
    <h3>Disinformation runs rampant online. We make exploring it possible.</h3>
  </div>
</template>

<script>
export default {
  name: "Home",
  components: {
  },
  data() {
    return {
      searchParameters: {
        query: ""
      }
    };
  },
  methods: {
    redirect() {
      let query = encodeURI(this.searchParameters.query);
      this.$router.push(`/search?query=${query}`);
    }
  }
};
</script>
