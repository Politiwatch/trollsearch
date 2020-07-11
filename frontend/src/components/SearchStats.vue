<template>
  <section>
    <p>{{languages}}</p>
    <hr class="h-6 sep" />
    <pie-chart :chart-data="languageChartData" />
  </section>
</template>

<script>
import PieChart from "./PieChart";

export default {
  components: {
    PieChart
  },
  data() {
    return {
      languageChartData: this.dictToChartData(this.props.languages),
    };
  },
  methods: {
    dictToChartData(dict) {
      return {
        datasets: [
          {
            data: Object.values(dict)
          }
        ],
        labels: [Object.keys(dict)]
      };
    }
  },
  props: ["archives", "languages", "hashtags", "total"],
  name: "SearchStats"
};
</script>
