<template>
  <section class="card ~neutral !low my-4 relative">
    <div class="flex justify-between">
      <p @mouseenter="userDetail = true" @mouseleave="userDetail = false">
        <span v-if="data.user_display_name === data.userid" class="">
          @{{data.user_display_name.slice(0, 8)}}<span v-if="userDetail">&hellip; </span>
          <span
            v-if="userDetail"
            title="To preserve privacy, Twitter account names are anonymized."
            >(anonymized)</span
          >
        </span>
        <span v-if="data.user_display_name !== data.userid" class="">
          @{{ data.user_screen_name }}
        </span>
        <span v-if="userDetail">
          &bull; {{ data.follower_count.toLocaleString() }} followers
        </span>
      </p>
    </div>
    <p
      v-html="data.tweet_text"
      class="mt-2 mb-4 text-lg text-gray-900"
    ></p>
    <div class="flex text-gray-600">
      <p class="mr-6">
        <span :title="data.tweet_time">{{
          data.tweet_time.split(" ")[0]
        }}</span>
      </p>
      <p class="mr-6">
        <span class="icon">
          <font-awesome-icon icon="comment" class="text-gray-600" size="sm" />
        </span>
        {{ data.reply_count }}
      </p>
      <p class="mr-6">
        <span class="icon">
          <font-awesome-icon icon="retweet" class="text-gray-600" size="sm" />
        </span>
        {{ data.retweet_count }}
      </p>
      <p class="mr-6">
        <span class="icon">
          <font-awesome-icon icon="heart" class="text-gray-600" size="sm" />
        </span>
        {{ data.like_count }}
      </p>
    </div>
  </section>
</template>

<script>
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faRetweet,
  faHeart,
  faComment
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

export default {
  props: ["data"],
  name: "Tweet",
  components: { FontAwesomeIcon },
  data() {
    return {
      userDetail: false
    };
  },
  created() {
    library.add(faRetweet, faHeart, faComment);
  }
};
</script>
