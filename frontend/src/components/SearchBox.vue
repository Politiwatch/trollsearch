<template>
  <section>
    <div class="card ~neutral !low">
      <div>
        <p class="mb-1 label">Search</p>
        <input
          class="text-2xl input"
          type="search"
          v-model="query"
          @input="update"
          placeholder="Search for something..."
          autofocus="autofocus"
        />
      </div>
      <details class="mt-2">
        <summary class="cursor-pointer">Advanced search options</summary>
        <div class="grid grid-cols-1 gap-6 mt-1">
          <div>
            <p class="mb-1 label">Time range</p>
            <DatePicker v-model="timeRange" mode="range" @input="update"></DatePicker>
          </div>
          <div>
            <p class="mb-1 label">Languages</p>
            <multiselect
              v-model="languages"
              :options="stats.languages"
              @input="update"
              :multiple="true"
              :custom-label="languageName"
              placeholder="Select languages to include"
            ></multiselect>
          </div>
          <div>
            <p class="mb-1 label">Archive</p>
            <multiselect
              v-model="archives"
              :options="stats.archiveNames"
              @input="update"
              :multiple="true"
              :custom-label="archiveName"
              placeholder="Select archives to include"
            ></multiselect>
          </div>
          <div>
            <p class="mb-1 label">Likes</p>
            <div class="flex items-center justify-between">
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
            <p class="mb-1 label">Retweets</p>
            <div class="flex items-center justify-between">
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
            <p class="mb-1 label">Followers</p>
            <div class="flex items-center justify-between">
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
      </details>
    </div>
  </section>
</template>

<script>
import debounce from "debounce";
import DatePicker from "v-calendar/lib/components/date-picker.umd";
import Multiselect from "vue-multiselect";
import languageNames from "../assets/languages";
import archiveNames from "../assets/archives";

let encodeSearchUriParameters = values => {
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
    Multiselect
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
      archives: this.$route.query.archive || [],
      timeRange: {
        start: new Date(this.$route.query.min_time),
        end: new Date(this.$route.query.max_time)
      },
      stats: JSON.parse(localStorage.getItem("stats"))
    };
  },
  methods: {
    languageName: function(langCode) {
      return (languageNames[langCode] || { name: "Unknown" }).name;
    },
    archiveName: function(archiveCode) {
      console.log(archiveCode);
      return (archiveNames[archiveCode] || { name: "Unknown" }).name;
    },
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
        archive: this.archives,
        min_time: this.timeRange === null ? null : this.timeRange.start,
        max_time: this.timeRange === null ? null : this.timeRange.end
      });
      if (builtParams.trim().length == 0) {
        this.$router.push("/", {
          force: true
        });
      } else {
        this.$router.push(`/search?${builtParams}`, {
          force: true
        });
      }
    },
    update: debounce(function() {
      this.performSearch();
    }, 300)
  }
};
</script>
