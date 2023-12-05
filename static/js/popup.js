jQuery(document).ready(function($){
	//open popup
	$('.cd-popup-trigger').on('click', function(event){
		event.preventDefault();
		$('.cd-popup').addClass('is-visible');
	});
	
	//close popup
	$('.cd-popup').on('click', function(event){
		if( $(event.target).is('.close-trigger') || $(event.target).is('.cd-popup') ) {
			event.preventDefault();
			$(this).removeClass('is-visible');
		}
	});
	//close popup when clicking the esc keyboard button
	$(document).keyup(function(event){
    	if(event.which=='27'){
    		$('.cd-popup').removeClass('is-visible');
	    }
    });
	//open and close the edit user's name field
	$('.show-edit-form').on('click', function(event){
		event.preventDefault();
		if ($('.edit-name').hasClass('edit-name-show')) {
			$('.edit-name').removeClass('edit-name-show');
		} else {
			$('.edit-name').addClass('edit-name-show');
		}
	});
});