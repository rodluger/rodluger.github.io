/*
	Visualize by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
*/

$(function() {

	// Vars.
		var	$window = $(window),
			$body = $('body'),
			$wrapper = $('#wrapper');
    var cachedWidth = $(window).width();
  
  // Show caption detail?
  var i;
  details = document.getElementsByClassName('caption-detail');
  for (i = details.length - 1; i >= 0; i--) {
    if ($(window).width() <= 700)
      details[i].style.display = 'none';
    else
      details[i].style.display = 'inline';
  }
  
	// Breakpoints.
		skel.breakpoints({
			xlarge:	'(max-width: 1680px)',
			large:	'(max-width: 1280px)',
			medium:	'(max-width: 980px)',
			small:	'(max-width: 736px)',
			xsmall:	'(max-width: 480px)'
		});

	// Disable animations/transitions until everything's loaded.
		$body.addClass('is-loading');

		$window.on('load', function() {
			$body.removeClass('is-loading');
		});
  
  // Fontawesome labels
  $("a").hover(function(){
      if (this.id.startsWith('icon-')) {
        label = document.getElementById('label-'.concat(this.id));
        label.style.visibility = 'visible';
      }
    }, function(){
      if (this.id.startsWith('icon-')) {
        label = document.getElementById('label-'.concat(this.id));
        label.style.visibility = 'hidden';
      }
  });
  
  // Smooth anchor scrolling
  $(function() {
    $('a[href*="#"]:not([href="#"])').click(function() {
      if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
        if (target.length) {
          $('html, body').animate({
            scrollTop: target.offset().top
          }, 1000);
          return false;
        }
      }
    });
  });
  
  // Window resizing actions
  $window.on('resize', function() {
    
    // Hide thumbnail details when window is too small
    var i;
    details = document.getElementsByClassName('caption-detail');
    for (i = details.length - 1; i >= 0; i--) {
      if ($(window).width() <= 700)
        details[i].style.display = 'none';
      else
        details[i].style.display = 'inline';
    }
  });
  
});