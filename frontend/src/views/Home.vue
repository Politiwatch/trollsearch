<template>
  <div class="align-middle">
    <h1 class="font-sans">Twitter Disinformation Archive</h1>
    <SearchBox />
    {{ searchParameters }}
  </div>
</template>

<script>
import SearchBox from "@/components/SearchBox.vue";

export default {
  name: "Home",
  components: {
    SearchBox
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
