Vue.component('vue-multiselect', window.VueMultiselect.default);

const openCollectivitesApiCall = new OpenCollectivitesDataService();

var app = new Vue({
  el: '#vue-app',

  data() {
    return {
      options: [],
      defaultList: [],
      places: null,
      isLoading: false,
      type: pageData.type,
      origin: pageData.slug
    };
  },

  computed: {
    groupName() {
      if (this.type === "commune") {
        return "Communes";
      }
      return "";
    },
  },

  methods: {
    limitText(count) {
      return `et ${count} autres résultats`;
    },

    searchCollectivities(query) {
      query = query.toLowerCase();

      if (query.length == 0 && this.isLoading == true) {
        this.isLoading = false;
      } else if (query.length < 3 && !shortnamedCommunes.includes(query)) {
        this.options = this.defaultList;
      } else {
        this.isLoading = true;
        openCollectivitesApiCall.listByName(query)
          .then((response) => {
            const results = response.data;
            for (const r of results) {
              // filtering to get only the needed type
              if (r.groupName === this.groupName) {
                // Do not list the current (origin) page in the results
                this.options = r.items.filter((item) => {
                  return item.slug !== this.origin;
                });
                this.isLoading = false;
              }
            }
          })
          .catch((e) => {
            console.log("🙅  Service not responding");
            console.log(e);
          });
      }
    },

    loadResultPage() {
      let result_url = `/compare/${this.type}/${this.origin}`
      for (const p of this.places) {
        result_url += '/' + p.slug
      }

      window.location.href = result_url;

    },
  },
});