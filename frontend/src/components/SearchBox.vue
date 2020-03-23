<template>
  <section>
    <div class="pt-2 relative mx-auto text-gray-600">
      <input
        class="border-2 border-gray-200 h-10 px-5 rounded-lg text-sm font-sans focus:outline-none w-full"
        type="search"
        v-model="query"
        v-on:input="update"
        placeholder="Search for something..."
        autofocus="autofocus"
      />
    </div>
  </section>
</template>

<script>
import debounce from "debounce";

export default {
  name: "SearchBox",
  props: ["value"],
  data() {
    return {
      query: this.$route.query.query
    };
  },
  methods: {
    update: debounce(function() {
      if (this.query.trim().length == 0) {
        this.$router.push("/", {
          force: true,
        });
      } else {
        let query = encodeURI(this.query);
        this.$router.push(`/search?query=${query}`, {
          force: true,
        });
      }
    }, 300)
  }
};
</script>
