<template>
  <section class="my-4 font-sans shadow-md bg-white rounded px-4 py-4">
    <p v-html="data.tweet_text"></p>
  </section>
</template>

<script>
export default {
  props: ["data"],
  name: "Tweet"
};
</script>
