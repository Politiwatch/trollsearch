<template>
  <section class="card ~neutral !low my-4">
    <p v-html="data.tweet_text"></p>
    <p>{{data.retweet_count}} retweets</p>
    <p>{{data.like_count}} likes</p>
    <p>{{data.follower_count}} followers</p>
    <p>{{data.tweet_time}}</p>
  </section>
</template>

<script>
export default {
  props: ["data"],
  name: "Tweet"
};
</script>
