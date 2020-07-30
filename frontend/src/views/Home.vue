<template>
  <div class="content max-w-xl mx-auto">
    <h2>We make exploring Twitter's disinformation archives possible.</h2>
    <p>Twitter periodically releases archives of state-sponsored disinformation that it has identified and removed from its platform. While these archives are useful, they are not released in a format that is accessible to analysis by the general public. This site changes that.</p>
    <p>We've assembled {{stats.total_tweets.toLocaleString()}} tweets from {{stats.archives.length.toLocaleString()}} Twitter disinformation archives into an easily searchable database. All of these Tweets are connected to government-backed organizations, and annotated with the Twitter archive they came from.</p>
    <p>
      We accessed and compiled these Tweets from the Information Operations section of the
      <a
        href="https://transparency.twitter.com/en/information-operations.html"
      >Twitter Transparency Report</a>. The source code for this site is open source and available on GitHub.
    </p>

    <h3>Usage instructions</h3>
    <p>To search the database, enter your query into the search box at the top of this page; your search will be performed automatically after a few seconds. For more fine-grained control, click "Advanced search options" to access the filter menu, where you are able to further refine your search by date, like count, languages, archives, retweets, and followers.</p>

    <h3>Database details</h3>
    <p>Our database contains the tweets from the following Twitter disinformation archives:</p>
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
      <article class="card ~neutral !low" v-for="archive in stats.archives" :key="archive.name">
        <p class="label">{{archiveName(archive.name)}}</p>
        <p>{{archive.tweets.toLocaleString()}} tweets</p>
      </article>
    </div>
    <p>Please note that some information in the database has been anonymized by Twitter to protect the privacy of smaller accounts. As Twitter explains:</p>
    <blockquote>
      For accounts with fewer than 5,000 followers, we have hashed certain identifying fields (such as user ID and screen name) in the publicly-available version of the datasets.
      <cite>From Twitter's <a href="https://transparency.twitter.com/en/information-operations.html">Information Operations Report</a></cite>
    </blockquote>

    <h3>Disclaimer</h3>
    <p>All of these Tweets were released by Twitter; Politiwatch doesn't endorse or support the content of the tweets themselves. We make no guarantees about the completeness or accuracy of the materials on this site.</p>

    <h3>About us</h3>
    <p>
      This project is an experimental
      <a href="https://politiwatch.org">Politiwatch</a> project led by Alexandra Salzman. If you have questions, please contact Politiwatch at
      <a
        href="mailto:secure@politiwatch.org"
      >secure@politiwatch.org</a>.
    </p>
  </div>
</template>

<script>
import archiveNames from "../assets/archives";

export default {
  name: "Home",
  components: {},
  data() {
    return {
      searchParameters: {
        query: ""
      },
      stats: JSON.parse(localStorage.getItem("stats"))
    };
  },
  methods: {
    redirect() {
      let query = encodeURI(this.searchParameters.query);
      this.$router.push(`/search?query=${query}`);
    },
    archiveName(archive) {
      return (archiveNames[archive] || { name: "Unknown Archive" }).name;
    }
  }
};
</script>
