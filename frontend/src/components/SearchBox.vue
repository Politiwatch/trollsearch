<template>
  <section>
    <div class="card ~neutral !low content">
      <input
        class="input text-2xl"
        type="search"
        v-model="query"
        v-on:input="update"
        placeholder="Search for something..."
        autofocus="autofocus"
      />
      <p class="label">Likes</p>
      <div class="flex justify-between items-center">
        <input class="flex-grow input" v-model="minLikes" v-on:input="update" type="number" placeholder="Min likes" />
        <span class="px-2">to</span>
        <input class="flex-grow input" v-model="maxLikes" v-on:input="update" type="number" placeholder="Max likes" />
      </div>
      <p class="label">Retweets</p>
      <div class="flex justify-between items-center">
        <input class="flex-grow input" v-model="minRetweets" v-on:input="update" type="number" placeholder="Min retweets" />
        <span class="px-2">to</span>
        <input class="flex-grow input" v-model="maxRetweets" v-on:input="update" type="number" placeholder="Max retweets" />
      </div>
      <p class="label">Followers</p>
      <div class="flex justify-between items-center">
        <input class="flex-grow input" v-model="minFollowers" v-on:input="update" type="number" placeholder="Min followers" />
        <span class="px-2">to</span>
        <input class="flex-grow input" v-model="maxFollowers" v-on:input="update" type="number" placeholder="Max followers" />
      </div>
    </div>
  </section>
</template>

<script>
import debounce from "debounce";

let encodeSearchUriParameters = (values) => {
  let builtParams = [];
  for (let key of Object.keys(values)) {
    if (values[key] != undefined && values[key] != null && values[key] != "") {
      builtParams.push(`${encodeURI(key)}=${encodeURI(values[key])}`);
    }
  }
  console.log(builtParams);
  return builtParams.join("&");
};

export default {
  name: "SearchBox",
  props: ["value"],
  data() {
    return {
      query: this.$route.query.query,
      minLikes: this.$route.query.min_likes,
      maxLikes: this.$route.query.max_likes,
      minRetweets: this.$route.query.min_retweets,
      maxRetweets: this.$route.query.max_retweets,
      minFollowers: this.$route.query.min_followers,
      maxFollowers: this.$route.query.max_followers,
    };
  },
  methods: {
    performSearch: function() {
      let builtParams = encodeSearchUriParameters({
        query: this.query,
        min_likes: this.minLikes,
        max_likes: this.maxLikes,
        min_retweets: this.minRetweets,
        max_retweets: this.maxRetweets,
        min_followers: this.minFollowers,
        max_followers: this.maxFollowers,
      });
      if (builtParams.trim().length == 0) {
        this.$router.push("/", {
          force: true,
        });
      } else {
        this.$router.push(`/search?${builtParams}`, {
          force: true,
        });
      }
    },
    update: debounce(function() {
      this.performSearch();
    }, 300),
  },
};
</script>
