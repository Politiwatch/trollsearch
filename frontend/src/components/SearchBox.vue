<template>
  <section>
    <div class="grid grid-cols-1 gap-6 card ~neutral !low">
      <div>
        <input
          class="input text-2xl"
          type="search"
          v-model="query"
          @input="update"
          placeholder="Search for something..."
          autofocus="autofocus"
        />
      </div>
      <div>
        <p class="label">Time range</p>
        <DatePicker v-model="timeRange" mode="range" @input="update">
        </DatePicker>
      </div>
      <div>
        <p class="label">Languages</p>
        <multiselect
          v-model="languages"
          :options="stats.languages"
          @input="update"
          :multiple="true"
          placeholder="Select languages to include"
        >
        </multiselect>
      </div>
      <div>
        <p class="label">Likes</p>
        <div class="flex justify-between items-center">
          <input
            class="flex-grow input"
            v-model="minLikes"
            v-on:input="update"
            type="number"
            placeholder="Min likes"
          />
          <span class="px-2">to</span>
          <input
            class="flex-grow input"
            v-model="maxLikes"
            v-on:input="update"
            type="number"
            placeholder="Max likes"
          />
        </div>
      </div>
      <div>
        <p class="label">Retweets</p>
        <div class="flex justify-between items-center">
          <input
            class="flex-grow input"
            v-model="minRetweets"
            v-on:input="update"
            type="number"
            placeholder="Min retweets"
          />
          <span class="px-2">to</span>
          <input
            class="flex-grow input"
            v-model="maxRetweets"
            v-on:input="update"
            type="number"
            placeholder="Max retweets"
          />
        </div>
      </div>
      <div>
        <p class="label">Followers</p>
        <div class="flex justify-between items-center">
          <input
            class="flex-grow input"
            v-model="minFollowers"
            v-on:input="update"
            type="number"
            placeholder="Min followers"
          />
          <span class="px-2">to</span>
          <input
            class="flex-grow input"
            v-model="maxFollowers"
            v-on:input="update"
            type="number"
            placeholder="Max followers"
          />
        </div>
      </div>
    </div>
    {{ stats }}
  </section>
</template>

<script>
import debounce from "debounce";
import DatePicker from "v-calendar/lib/components/date-picker.umd";
import Multiselect from "vue-multiselect";

let encodeSearchUriParameters = (values) => {
  let builtParams = [];
  for (let key of Object.keys(values)) {
    if (values[key] != undefined && values[key] != null && values[key] != "") {
      let stringVal = null;
      if (values[key] instanceof Date) {
        if (!isNaN(values[key])) {
          stringVal = values[key].toUTCString();
        }
      } else if (values[key] instanceof Array) {
        for (let val of values[key]) {
          let newParam = {};
          newParam[key] = val;
          builtParams.push(encodeSearchUriParameters(newParam));
        }
      } else {
        stringVal = values[key].toString();
      }
      if (stringVal !== null) {
        builtParams.push(
          `${encodeURIComponent(key)}=${encodeURIComponent(stringVal)}`
        );
      }
    }
  }
  return builtParams.join("&");
};

export default {
  name: "SearchBox",
  components: {
    DatePicker,
    Multiselect,
  },
  data() {
    return {
      query: this.$route.query.query,
      minLikes: this.$route.query.min_likes,
      maxLikes: this.$route.query.max_likes,
      minRetweets: this.$route.query.min_retweets,
      maxRetweets: this.$route.query.max_retweets,
      minFollowers: this.$route.query.min_followers,
      maxFollowers: this.$route.query.max_followers,
      languages: this.$route.query.language || [],
      timeRange: {
        start: new Date(this.$route.query.min_time),
        end: new Date(this.$route.query.max_time),
      },
      stats: JSON.parse(localStorage.getItem("stats")),
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
        language: this.languages,
        min_time: this.timeRange === null ? null : this.timeRange.start,
        max_time: this.timeRange === null ? null : this.timeRange.end,
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
