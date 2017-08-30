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

// Slick
$(document).ready(function(){
  $('.carousel').slick({
    dots: true,
    centerMode: true,
    infinite: true,
    centerPadding: '80px',
    slidesToShow: 3,
    prevArrow:"<button type='button' class='slick-prev' style='top:45%; left:-5%;'>Previous</button>",
    nextArrow:"<button type='button' class='slick-next' style='top:45%; right:-5%;'>Next</button>",
    responsive: [
    {
      breakpoint: 768,
      settings: {
        arrows: false,
        centerMode: true,
        centerPadding: '40px',
        slidesToShow: 3
      }
    },
    {
      breakpoint: 480,
      settings: {
        arrows: false,
        centerMode: true,
        centerPadding: '40px',
        slidesToShow: 1
      }
    }
  ]
  });
});

// On before slide change
$('.carousel').on('afterChange', function(event, slick, newSlide){
  
  // Reset all opacities
  elements = document.getElementsByClassName('carousel-image');
  for (var i = elements.length - 1; i >= 0; i--) {
    elements[i].style.opacity = 0.5;
  }
  
  // Make all popouts invisible
  popouts = document.getElementsByClassName('popout');
  for (var i = popouts.length - 1; i >= 0; i--) {
    popouts[i].style.display = 'none';
  }
  
  // Make current element/popout visible
  if (newSlide < 10) {
    document.getElementById('elem0'.concat(newSlide)).style.opacity = 1;
    document.getElementById('popout0'.concat(newSlide)).style.display = 'block';
  } else {
    document.getElementById('elem'.concat(newSlide)).style.opacity = 1;
    document.getElementById('popout'.concat(newSlide)).style.display = 'block';
  }
  
});