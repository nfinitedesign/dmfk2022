/*
	Photon by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$header = $('#header'),
		$nav = $('#nav-main'),
		$navPanel = $('#navPanel'),
		$navPanelToggle;

// Breakpoints.
	breakpoints({
		xlarge:   [ '1141px',  '1680px' ],
		large:    [ '981px',   '1140px' ],
		medium:   [ '737px',   '980px'  ],
		small:    [ '481px',   '736px'  ],
		xsmall:   [ '321px',   '480px'  ],
		xxsmall:  [ null,      '320px'  ]
	});

// Play initial animations on page load.
	$window.on('load', function() {
		window.setTimeout(function() {
			$body.removeClass('is-preload');
		}, 100);
	});

// Scrolly.
	$('.scrolly').scrolly();


// Nav Panel.

// Toggle.
	$navPanelToggle = $(
		'<a href="#navPanel" id="navPanelToggle">Menu</a>'
	)
	.appendTo($body);

// Change toggle styling once we've scrolled past the header.
	$header.scrollex({
		bottom: '8vh',
		enter: function() {
			$navPanelToggle.removeClass('alt');
			$nav.removeClass('alt');
		},
		leave: function() {
			$navPanelToggle.addClass('alt');
			$nav.addClass('alt');
		}
	});

// Panel.
	$navPanel.panel({
				delay: 500,
				hideOnClick: true,
				hideOnSwipe: true,
				resetScroll: true,
				resetForms: true,
				side: 'right',
				target: $body,
				visibleClass: 'is-navPanel-visible'
			});


// Hack: Disable transitions on WP.
	if (browser.os == 'wp'
	&&	browser.osVersion < 10)
		$navPanel
			.css('transition', 'none');

})(jQuery);