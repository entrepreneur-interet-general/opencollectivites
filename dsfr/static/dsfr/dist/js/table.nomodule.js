/*! DSFR v1.1.0 | SPDX-License-Identifier: MIT | License-Filename: LICENCE.md | restricted use (see terms and conditions) */

(function () {
  'use strict';

  var namespace = 'dsfr';

  var api = window[namespace] || { core: {} };
  window[namespace] = api;

  var TABLE_SELECTOR = api.core.ns.selector('table');
  var TABLE_NOSCROLL_SELECTOR = api.core.ns('table--no-scroll');
  var LEFT = 'left';
  var RIGHT = 'right';
  var SHADOW_CLASS = api.core.ns('table--shadow');
  var SHADOW_LEFT_CLASS = api.core.ns('table--shadow-left');
  var SHADOW_RIGHT_CLASS = api.core.ns('table--shadow-right');
  var SCROLL_OFFSET = 1; // valeur en px du scroll avant laquelle le shadow s'active ou se desactive

  var Table = function Table (table) {
    this.init(table);
  };

  Table.prototype.init = function init (table) {
    this.table = table;
    this.table.setAttribute(api.core.ns.attr('js-table'), 'true'); // TODO: code provisoire en attendant la refacto du JS dynamique
    this.tableElem = this.table.querySelector('table');
    this.tableContent = this.tableElem.querySelector('tbody');
    this.isScrollable = this.tableContent.offsetWidth > this.tableElem.offsetWidth;
    this.caption = this.tableElem.querySelector('caption');
    this.captionHeight = 0;
    var scrolling = this.change.bind(this);
    this.tableElem.addEventListener('scroll', scrolling);
  };

  Table.prototype.change = function change () {
    var newScroll = this.tableContent.offsetWidth > this.tableElem.offsetWidth;
    var firstTimeScrollable = this.tableElem.offsetWidth > this.table.offsetWidth;
    if (newScroll || firstTimeScrollable) {
      if (!this.table.classList.contains(TABLE_NOSCROLL_SELECTOR)) { this.scroll(); }
    } else {
      if (newScroll !== this.isScrollable) { this.delete(); }
    }
    this.isScrollable = newScroll;
    firstTimeScrollable = false;
    var captionSize = this.caption.getBoundingClientRect();
    this.table.style.setProperty('--table-offset', captionSize.height + 'px');
  };

  Table.prototype.delete = function delete$1 () {
    api.core.removeClass(this.table, SHADOW_RIGHT_CLASS);
    api.core.removeClass(this.table, SHADOW_LEFT_CLASS);
    api.core.removeClass(this.table, SHADOW_CLASS);
    if (this.caption) {
      this.tableElem.style.marginTop = '';
      this.caption.style.top = '';
      this.tableElem.style.marginBottom = '';
      this.caption.style.bottom = '';
    }
  };

  Table.prototype.scroll = function scroll () {
    api.core.addClass(this.table, SHADOW_CLASS);
    this.setShadowPosition();
  };

  /* affiche les blocs shadow en fonction de la position du scroll, en ajoutant la classe visible */
  Table.prototype.setShadowPosition = function setShadowPosition () {
    var tableScrollLeft = this.getScrollPosition(LEFT);
    var tableScrollRight = this.getScrollPosition(RIGHT);

    // on inverse en cas de lecture droite - gauche
    if (document.documentElement.getAttribute('dir') === 'rtl') {
      this.setShadowVisibility(RIGHT, tableScrollLeft);
      this.setShadowVisibility(LEFT, tableScrollRight);
    } else {
      this.setShadowVisibility(LEFT, tableScrollLeft);
      this.setShadowVisibility(RIGHT, tableScrollRight);
    }
  };

  /* Donne le nombre de pixels scrollés honrizontalement dans un element scrollable */
  Table.prototype.getScrollPosition = function getScrollPosition (side) {
    var inverter = 1;
    // on inverse en cas de lecture droite - gauche pour que la valeur de scroll soit toujours positive
    if (document.documentElement.getAttribute('dir') === 'rtl') {
      inverter = -1;
    }
    switch (side) {
      case LEFT:
        return this.tableElem.scrollLeft * inverter;
      case RIGHT:
        return this.tableContent.offsetWidth - this.tableElem.offsetWidth - this.tableElem.scrollLeft * inverter;
      default:
        return false;
    }
  };

  /* ajoute la classe fr-table--shadow-right ou fr-table--shadow-right sur fr-table
   en fonction d'une valeur de scroll et du sens (right, left) */
  Table.prototype.setShadowVisibility = function setShadowVisibility (side, scrollPosition) {
    // si on a pas scroll, ou qu'on scroll jusqu'au bout
    if (scrollPosition <= SCROLL_OFFSET) {
      if (side === LEFT) { api.core.removeClass(this.table, SHADOW_LEFT_CLASS); }
      else if (side === RIGHT) { api.core.removeClass(this.table, SHADOW_RIGHT_CLASS); }
    } else {
      if (side === LEFT) { api.core.addClass(this.table, SHADOW_LEFT_CLASS); }
      else if (side === RIGHT) { api.core.addClass(this.table, SHADOW_RIGHT_CLASS); }
    }
  };

  api.Table = Table;

  var tables = [];

  var change = function () {
    for (var i = 0; i < tables.length; i++) { tables[i].change(); }
  };

  var build = function () {
    var tableNodes = document.querySelectorAll(TABLE_SELECTOR);
    for (var i = 0; i < tableNodes.length; i++) { tables.push(new Table(tableNodes[i])); }

    window.addEventListener('resize', change);
    window.addEventListener('orientationchange', change);
    change();
  };

  /* eslint-disable no-new */

  new api.core.Initializer(TABLE_SELECTOR, [build]);

}());
//# sourceMappingURL=table.nomodule.js.map
