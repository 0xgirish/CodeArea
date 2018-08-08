jQuery(document).ready(function($){
	// browser window scroll (in pixels) after which the "menu" link is shown
	var offset = 300;

	var navigationContainer = $('#cd-nav'),
		mainNavigation = navigationContainer.find('#cd-main-nav ul');

	//hide or show the "menu" link

	//open or close the menu clicking on the bottom "menu" link
	$('.cd-nav-trigger').on('click', function(){
		$(this).toggleClass('menu-is-open');
		//we need to remove the transitionEnd event handler (we add it when scolling up with the menu open)
		mainNavigation.off('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend').toggleClass('is-visible');

	});

});