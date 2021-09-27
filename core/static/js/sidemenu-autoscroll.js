var scrollapp = new Vue({
  el: "#vue-sidemenu",

  data() {
    return {
      windowPosition: 0,
      menuItems: [],
      headings: [],
      firstHeadingPosition: null,
      lastHeadingPosition: null,
    }
  },

  mounted() {
    this.getHeadings()

    this.menuItems = this.$el.querySelectorAll('a')
    this.makeMenuItemActive(this.menuItems[0])
    this.menuItems.forEach(menuItem => menuItem.addEventListener('click', this.onMenuItemClick))

    window.addEventListener("scroll", this.onScroll)

    // Update the position once when the page is fully loaded 
    document.onreadystatechange = () => { 
      if (document.readyState == "complete") {
        this.updatePosition(window.pageYOffset)
      } 
    }
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.onScroll)
  },
  methods: {
    getHeadings() {
      this.headings = document.querySelectorAll("article h2")
      this.firstHeading = this.headings[0]
      this.lastHeading = this.headings[this.headings.length - 1]
    },
    onScroll() {
      this.updatePosition(window.top.scrollY)
    },
    updatePosition(position) {
      if (position <= this.firstHeading.offsetTop) {
        this.setCurrentMenuItem(this.firstHeading.id)
      } else if (position >= this.lastHeading.offsetTop) {
        this.setCurrentMenuItem(this.lastHeading.id)
      } else {
        for (var h of this.headings) {
          if ((position >= h.offsetTop) && (position < (h.offsetTop + h.offsetHeight))) {
            this.setCurrentMenuItem(h.id)
          }
        }  
      }
    },
    onMenuItemClick(click) {
      var targetId = click.target.href.split("#")[1]
      this.setCurrentMenuItem(targetId)
    },
    makeMenuItemActive(menuItem) {
      menuItem.setAttribute("aria-current", "page")

      var parentLi = menuItem.parentElement
      parentLi.className += " fr-sidemenu__item--active"
    },
    makeMenuItemInactive(menuItem) {
      menuItem.removeAttribute("aria-current")

      var parentLi = menuItem.parentElement
      parentLi.className = "fr-sidemenu__item"
    },
    setCurrentMenuItem(itemId){
      for (var i of this.menuItems) {
        var urlFragment = i.href.split("#")[1]
        if (urlFragment == itemId) {
          this.makeMenuItemActive(i)
        }
        else {
          this.makeMenuItemInactive(i)
        }
      }
    }
  }
})