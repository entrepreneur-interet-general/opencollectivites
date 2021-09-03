Vue.component('vue-multiselect', window.VueMultiselect.default);

const openCollectivitesApiCall = new OpenCollectivitesDataService();

var app = new Vue({
  el: '#vue-app',

  data() {
    return {
      options: [],
      defaultList: [],
      places: null,
      singlePlace: null,
      isLoading: false,
      type: pageData.type,
      origin: pageData.slug,
      query: ""
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
      this.query = query;

      if (query.length == 0 && this.isLoading == true) {
        this.isLoading = false;
      } else if (query.length < 3 && !shortnamedCommunes.includes(query)) {
        this.options = this.defaultList;
      } else {
        this.isLoading = true;
        this.options = [];
        openCollectivitesApiCall.listByName(query)
          .then((response) => {

            if (this.origin == "home") {
              console.log("ici")
              this.options = response.data;
            } else {
              this.fillOptionsforComparator(response)
            }
          })
          .catch((e) => {
            console.log("🙅  Service not responding");
            console.log(e);
          });
          this.isLoading = false;
        }
    },

    fillOptionsforComparator(response) {
      const results = response.data;
      for (const r of results) {
        // filtering to get only the needed type
        if (r.type === this.type) {
          // Do not list the current (origin) page in the results
          this.options = r.items.filter((item) => {
            return item.slug !== this.origin;
          });
        }
      }  
    },

    loadResultPageHome() {
      window.location.href = '/' + this.singlePlace.type + '/' + this.singlePlace.slug;
    },


    loadResultPageCompare() {
      let result_url = `/compare/${this.type}/${this.origin}`
      for (const p of this.places) {
        result_url += '/' + p.slug
      }
      window.location.href = result_url;
    },
  },
});