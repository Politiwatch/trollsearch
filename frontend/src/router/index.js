import Vue from "vue";
import VueRouter from "vue-router";
import Search from "../views/Search.vue";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    meta: {
      title: "Twitter Disinformation Archive"
    },
    component: Home
  },
  {
    path: "/search",
    name: "Search",
    meta: {
      title: "Search Results | Twitter Disinformation Archive"
    },
    component: Search
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title;
  next();
});

export default router;
