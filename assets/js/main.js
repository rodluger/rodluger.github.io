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

	// Poptrox.
		$window.on('load', function() {
      
      /*
			$('.thumbnails').poptrox({
				onPopupClose: function() { $body.removeClass('is-covered'); },
				onPopupOpen: function() { $body.addClass('is-covered'); },
				baseZIndex: 10001,
				useBodyOverflow: false,
				usePopupEasyClose: true,
				overlayColor: '#000000',
				overlayOpacity: 0.75,
				popupLoaderText: '',
				fadeSpeed: 500,
				usePopupDefaultStyling: false,
				windowMargin: (skel.breakpoint('small').active ? 5 : 50)
			});
			*/
			
			$('.popicon').poptrox({
				onPopupClose: function() { $body.removeClass('is-covered'); },
				onPopupOpen: function() { $body.addClass('is-covered'); },
				baseZIndex: 10001,
				useBodyOverflow: false,
				usePopupEasyClose: true,
				overlayColor: '#000000',
				overlayOpacity: 0.75,
				popupLoaderText: '',
				fadeSpeed: 500,
				usePopupDefaultStyling: false,
				windowMargin: (skel.breakpoint('small').active ? 5 : 50)
			});

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
  
  // Show/hide About/Presentations text
  /*
  $("a").click(function(){
      if (this.id == 'icon-about') {
        var about = document.getElementById('about');
        if (about.clientHeight) {
          about.style.height = 0;
        } else {
          var wrapper = document.querySelector('.about-wrapper');
          about.style.height = wrapper.clientHeight + "px";
        }
      }
  });
  */
  
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
    
    // If the window actually resized, reset thumbnail locations
    var newWidth = $(window).width();
    if(newWidth !== cachedWidth){
      ResetMove();
      cachedWidth = newWidth;
    }

    // Hide thumbnail details when window is too small
    var i;
    details = document.getElementsByClassName('caption-detail');
    for (i = details.length - 1; i >= 0; i--) {
      if ($(window).width() <= 800)
        details[i].style.display = 'none';
      else
        details[i].style.display = 'inline';
    }
  });
  
});

function EmToPx(parentElement, ems){
  parentElement = parentElement || document.body;
  var div = document.createElement('div');
  div.style.width = "1000em";
  parentElement.appendChild(div);
  var pixels = div.offsetWidth / 1000;
  parentElement.removeChild(div);
  return Math.round(ems * pixels);
}

function ResetMove(){
  
  // Reset columns
  document.getElementById("column0").style.top = '0px';
  document.getElementById("column1").style.top = '0px';
  document.getElementById("column2").style.top = '0px';

  // Hide all popouts and return opacity to 1
  for (i = 0; i < 2; i++) {
    for (j = 0; j < 3; j++) {
      document.getElementById('elem' + i + j + 'popout').style.display = 'none';
      document.getElementById('elem' + i + j).style.opacity = 1;
      document.getElementById('elem' + i + j).filter = 'alpha(opacity=1)';
    }
  } 
  
  // Reset center elements
  document.getElementById('elem01').style.left = '0px';
  document.getElementById('elem11').style.top = '0px';
   
}

function Move(row,col){
  
  // Constants
  var endBottom = document.getElementById("elem10").offsetTop;
  var endLeft = -document.getElementById("elem10").offsetWidth - EmToPx(document.getElementById("elem10"), 1.5);
  var endCenterBottom = endBottom - document.getElementById("elem01").offsetHeight;
  var sgn = 5;
  var readyFade1 = 0;
  var readyMoveLeftRight1 = 0;
  var readyMoveUpDown = 0;
  var readyMoveLeftRight2 = 0;
  var readyFade2 = 0;
  
  // Which columns will we move?
  if (col == 0) {
    var colA = document.getElementById("column1");   
    var colB = document.getElementById("column2");
    var colC = document.getElementById("column0");
  } else if (col == 1) {
    var colA = document.getElementById("column0");   
    var colB = document.getElementById("column2");
    var colC = document.getElementById("column1");
  } else {
    var colA = document.getElementById("column0");   
    var colB = document.getElementById("column1");
    var colC = document.getElementById("column2");
  }
  
  // The center elements
  var centertop = document.getElementById('elem01');
  var centercenter = document.getElementById('elem11');
  var centerbot = document.getElementById('elem21');
  
  // The popout element
  var popout = document.getElementById('elem' + row + col + 'popout');
  popout.style.height = document.getElementById("elem00").offsetHeight - EmToPx(document.getElementById("elem00"), 1.5) + 'px';
  
  // Activate/disactivate? TODO
  var status;
  if (popout.style.display == 'block')
    status = 'reset';
  else
    status = 'activate';

  // Figure out endpoints
  if (colA.offsetTop == 0){
    var endA = endBottom;
    var sgnA = sgn;
    var posA = 0;
  } else {
    if (popout.style.display == 'block'){
      var endA = 0;
      var sgnA = -sgn;
      var posA = endBottom;
    } else {
      var endA = endBottom;
      var sgnA = 0;
      var posA = endBottom;
    }
  }
  if (colB.offsetTop == 0){
    var endB = endBottom;
    var sgnB = sgn;
    var posB = 0;
  } else {
    if (popout.style.display == 'block'){
      var endB = 0;
      var sgnB = -sgn;
      var posB = endBottom;
    } else {
      var endB = endBottom;
      var sgnB = 0;
      var posB = endBottom;
    }
  }
  if (colC.offsetTop == 0){
    var endC = 0;
    var sgnC = 0;
    var posC = 0;
  } else {
    var endC = 0;
    var sgnC = -sgn;
    var posC = colC.offsetTop;
  }
  
  // Hide all other popouts
  for (i = 0; i < 2; i++) {
    for (j = 0; j < 3; j++) {
      if ((i != row) || (j != col)) {
        document.getElementById('elem' + i + j + 'popout').style.display = 'none';
      }
    }
  } 
  
  // Ensure opacities are set
  for (i = 0; i < 2; i++) {
    for (j = 0; j < 3; j++) {
      if (document.getElementById('elem' + i + j).style.opacity == '')
        document.getElementById('elem' + i + j).style.opacity = 1;
    }
  }
  
  // Animate the dimming
  var dim = 1;
  var timer0 = setInterval(function () {
    if (dim == 0){
      //alert('clear');
      clearInterval(timer0);
    } else {
        dim = 0;
        for (i = 0; i < 2; i++) {
          for (j = 0; j < 3; j++) {
            var elem = document.getElementById('elem' + i + j);
            if (status == 'reset') {
              if (elem.style.opacity < 1.) {                
                elem.style.opacity = parseFloat(elem.style.opacity) + 0.01;
                dim = 1;
              }
            } else {
              if ((i == row) && (j == col) && (elem.style.opacity < 1)) {
                // This element was just selected and must be brightened
                elem.style.opacity = parseFloat(elem.style.opacity) + 0.01;
                dim = 1;
              } else if (((i != row) || (j != col)) && (elem.style.opacity > 0.5)) {
                // This element must be dimmed
                elem.style.opacity = parseFloat(elem.style.opacity) - 0.01;
                dim = 1;
              }
            }
            elem.filter = 'alpha(opacity=' + elem.style.opacity * 100 + ")";
          }
        }
    }
  }, 1);
  
  // Fade out this pop-up if it's open
  if (popout.style.display == 'block') {
    var op = 1.;
    popout.style.opacity = op;
    popout.style.filter = 'alpha(opacity=' + op * 100 + ")";
    var timer1 = setInterval(function () {
      if (op <= 0.){
        clearInterval(timer1);
        popout.style.display = 'none';
        // Do we need to slide the center-top element back?
        if ((centertop.style.left != '0px') && (centertop.style.left != '')) {
          readyMoveLeftRight1 = 1;
        } else {
          readyMoveUpDown = 1;
        }
      } else {
        popout.style.opacity = op;
        popout.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= 0.01;
      }
    }, 1);
  } else {
    if ((centertop.style.left != '0px') && (centertop.style.left != '')){
      readyMoveLeftRight1 = 1;
    } else {
      readyMoveUpDown = 1;
    }
  }

  // Slide center elements back to its original location if necessary
  if ((centertop.style.left != '0px') && (centertop.style.left != '')) {
    
    // Center-top
    sgnE = sgn;
    posE = endLeft;
    endE = 0;
    var timer2a = setInterval(function () {
      if ((sgnE * posE >= sgnE * endE)) {
        // We have reached the end
        centertop.style.left = endE + 'px';
        clearInterval(timer2a);
        readyMoveUpDown += 0.5;
      } else {
        // Let's move the element
        if (readyMoveLeftRight1) {
          posE+=sgnE;
          centertop.style.left = posE + 'px';
        }  
      }
    }, 1);
    
    // Center-bottom
    sgnD = -sgn / 2;
    posD = endCenterBottom;
    endD = 0;
    var timer2b = setInterval(function () {
      if ((sgnD * posD >= sgnD * endD)) {
        // We have reached the end
        centerbot.style.top = endD + 'px';
        clearInterval(timer2b);
        readyMoveUpDown += 0.5;
      } else {
        // Let's move the element
        if (readyMoveLeftRight1) {
          posD+=sgnD;
          centerbot.style.top = posD + 'px';
        }  
      }
    }, 1);
    
  }

  // Animate up-down motion 
  var timer3 = setInterval(function () {
    if ((sgnA * posA >= sgnA * endA) && (sgnB * posB >= sgnB * endB) && (sgnC * posC >= sgnC * endC)) {
      // We have reached the end
      colA.style.top = endA + 'px';
      colB.style.top = endB + 'px';
      colC.style.top = endC + 'px';
      clearInterval(timer3);
      if (col == 1) {
        readyMoveLeftRight2 = 1;
      } else
        readyFade2 = 1;
    } else {
      // Let's move the columns
      if (readyMoveUpDown == 1) {
        posA+=sgnA; 
        colA.style.top = posA + 'px';
        posB+=sgnB; 
        colB.style.top = posB + 'px';
        posC+=sgnC; 
        colC.style.top = posC + 'px';    
      }  
    }
  }, 1);
  
  // Animate sideways motion (center column only)
  if (col == 1) {
    sgnE = -sgnA;
    if (sgnE < 0) {
      // Move left
      posE = 0;
      endE = endLeft;
    } else {
      // Move right
      posE = endLeft;
      endE = 0;
    }
    // Case where column is already lowered
    if (colC.offsetTop != 0) {
      sgnE = -sgn;
      posE = 0;
      endE = endLeft;
    }
    // Case where user clicks on the other element in the center column
    if ((posE == endLeft) && (popout.style.display != 'block')) {
      sgnE = 0;
      posE = endLeft;
      endE = endLeft;  
    }
    var timer4a = setInterval(function () {
      if ((sgnE * posE >= sgnE * endE)) {
        // We have reached the end
        centertop.style.left = endE + 'px';
        clearInterval(timer4a);
        readyFade2 += 0.5;
      } else {
        // Let's move the element
        if (readyMoveLeftRight2) {
          posE+=sgnE; 
          centertop.style.left = posE + 'px';
        }  
      }
    }, 1);
    
    // Center-bottom
    sgnD = sgnA / 2;
    if (sgnD < 0) {
      // Move up
      posD = endCenterBottom;
      endD = 0;
    } else {
      // Move down
      posD = 0;
      endD = endCenterBottom;
    }

    // Case where column is already lowered
    if (colC.offsetTop != 0) {
      sgnD = sgn / 2;
      posD = 0;
      endD = endCenterBottom;
    }
    
    // Case where user clicks on the other element in the center column
    if ((posD == endLeft) && (popout.style.display != 'block')) {
      sgnD = 0;
      posD = endCenterBottom;
      endD = endCenterBottom;  
    }
    
    var timer4b = setInterval(function () {
      if ((sgnD * posD >= sgnD * endD)) {
        // We have reached the end
        centerbot.style.top = endD + 'px';
        clearInterval(timer4b);
        readyFade2 += 0.5;
      } else {
        // Let's move the element
        if (readyMoveLeftRight2) {
          posD+=sgnD;
          centerbot.style.top = posD + 'px';
        }  
      }
    }, 1);
    
  }
  
  // Animate the fading
  if (endA == endBottom) {
    var op = 0.;
    popout.style.opacity = op;
    popout.style.filter = 'alpha(opacity=' + op * 100 + ")";
    var timer5 = setInterval(function () {
      if (op >= 1.){
        clearInterval(timer5);
        op = 1.;
        popout.style.opacity = op;
        popout.style.filter = 'alpha(opacity=' + op * 100 + ")";
      } else {
        if (readyFade2 == 1) {
          popout.style.display = 'block';
          popout.style.opacity = op;
          popout.style.filter = 'alpha(opacity=' + op * 100 + ")";
          op += 0.01;
        }
      }
    }, 1);
  }
    
}