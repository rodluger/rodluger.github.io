

/*-------------------------------------------------------------------------------
  PRE LOADER
-------------------------------------------------------------------------------*/

$(window).load(function() {
  $('.preloader').fadeOut(1000);  // set duration in brackets
});

$(document).ready(function() {
  $('[data-toggle="tooltip"]').tooltip({boundary: 'window'});
});