/*
	Visualize by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
*/

$(function() {

	// Vars.
	var	$window = $(window), $body = $('body');
  
  // Show caption detail?
  details = document.getElementsByClassName('caption-detail');
  for (var i = details.length - 1; i >= 0; i--) {
    if ($(window).width() <= 700)
      details[i].style.display = 'none';
    else
      details[i].style.display = 'inline';
  }
  
  // Show thumbnail description?
  description = document.getElementsByClassName('thumb-description-text');
  for (var i = description.length - 1; i >= 0; i--) {
    if ($(window).width() <= 700)
      description[i].style.display = 'none';
    else
      description[i].style.display = 'block';
  }
  
  // Show thumbnail mini description?
  description = document.getElementsByClassName('thumb-description-mini');
  for (var i = description.length - 1; i >= 0; i--) {
    if ($(window).width() <= 700)
      description[i].style.display = 'block';
    else
      description[i].style.display = 'none';
  }
  
  // Show thumbnail icons?
  icons = document.getElementsByClassName('thumb-description-icons');
  for (var i = icons.length - 1; i >= 0; i--) {
    if ($(window).width() <= 700)
      icons[i].style.display = 'none';
    else
      icons[i].style.display = 'block';
  }

  // Window resizing actions
  $window.on('resize', function() {
    
    // Hide thumbnail details when window is too small
    details = document.getElementsByClassName('caption-detail');
    for (var i = details.length - 1; i >= 0; i--) {
      if ($(window).width() <= 700)
        details[i].style.display = 'none';
      else
        details[i].style.display = 'inline';
    }
    
    // Hide thumbnail description when window is too small
    description = document.getElementsByClassName('thumb-description-text');
    for (var i = description.length - 1; i >= 0; i--) {
      if ($(window).width() <= 700)
        description[i].style.display = 'none';
      else
        description[i].style.display = 'block';
    }
    
    // Show thumbnail mini description when window is too small
    description = document.getElementsByClassName('thumb-description-mini');
    for (var i = description.length - 1; i >= 0; i--) {
      if ($(window).width() <= 700)
        description[i].style.display = 'block';
      else
        description[i].style.display = 'none';
    }
    
    // Hide thumbnail icons when window is too small
    icons = document.getElementsByClassName('thumb-description-icons');
    for (var i = icons.length - 1; i >= 0; i--) {
      if ($(window).width() <= 700)
        icons[i].style.display = 'none';
      else
        icons[i].style.display = 'block';
    }
    
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
  
  // Thumbnail descriptions
  $(".thumb").hover(
    
    // On enter
    function(){ 
      document.getElementById(this.id.concat('-description')).style.display = 'block';
    }, 
  
    // On leave
    function(){
      document.getElementById(this.id.concat('-description')).style.display = 'none';
    }
  
  );
      
});