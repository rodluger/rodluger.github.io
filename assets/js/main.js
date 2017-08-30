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
    if ($(window).width() <= 800)
      details[i].style.display = 'none';
    else
      details[i].style.display = 'inline';
  }
  
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
    
});