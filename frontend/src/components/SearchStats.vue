<template>
  <section>
    <div class="grid grid-cols-3 gap-3">
      <div>
        <p class="label text-center mb-2 font-semibold">Languages</p>
        <pie-chart
          :chart-data="languageChartData"
          :options="{ legend: { display: false } }"
        />
      </div>
      <div>
        <p class="label text-center mb-2 font-semibold">Archives</p>
        <pie-chart
          :chart-data="archiveChartData"
          :options="{ legend: { display: false } }"
        />
      </div>
      <div>
        <p class="label text-center mb-2 font-semibold">Hashtags</p>
        <pie-chart
          :chart-data="hashtagChartData"
          :options="{ legend: { display: false } }"
        />
      </div>
    </div>
  </section>
</template>

<script>
import PieChart from "./PieChart";
import languageNames from "../assets/languages";
import archiveNames from "../assets/archives";
import palette from "google-palette";

export default {
  components: {
    PieChart
  },
  data() {
    return {
      languageChartData: this.dictToChartData(
        this.languages,
        i => (languageNames[i] || { name: "Unknown" }).name
      ),
      archiveChartData: this.dictToChartData(
        this.archives,
        i => (archiveNames[i] || { name: "Unknown" }).name
      ),
      hashtagChartData: this.dictToChartData(this.hashtags, i =>
        i.startsWith("#") ? i : "#" + i
      )
    };
  },
  methods: {
    dictToChartData(dict, labelTransform) {
      let labels = Object.keys(dict).map(labelTransform || (i => i));
      let values = Object.values(dict);
      let colors = (palette("tol-rainbow", labels.length) || []).map(
        hex => "#" + hex
      );
      return {
        datasets: [
          {
            data: values,
            backgroundColor: colors
          }
        ],
        labels: labels
      };
    }
  },
  props: ["archives", "languages", "hashtags", "total"],
  name: "SearchStats"
};
</script>
