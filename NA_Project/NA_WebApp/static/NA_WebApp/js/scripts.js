(function($){

	"use strict";
	  
	$(document).ready(function () {
		socialchef.init();
	});
	
	var socialchef = {
	
		init: function () {
			//CUSTOM FORM ELEMENTS
			$(' input[type=radio],input[type=checkbox],input[type=file]').uniform();
			
			//MOBILE MENU
			$('.main-nav').slicknav({
				prependTo:'.head .wrap',
				allowParentLinks : true,
				label:''
			});
			
			//SCROLL TO TOP BUTTON
			$('.scroll-to-top').click(function () {
				$('body,html').animate({
					scrollTop: 0
				}, 800);
				return false;
			});
			
			//MY PROFILE TABS 
			$('.tab-content').hide().first().show();
			$('.tabs li:first').addClass("active");

			$('.tabs a').on('click', function (e) {
				e.preventDefault();
				$(this).closest('li').addClass("active").siblings().removeClass("active");
				$($(this).attr('href')).show().siblings('.tab-content').hide();
			});

			var hash = $.trim( window.location.hash );
			if (hash) $('.tab-nav a[href$="'+hash+'"]').trigger('click');
			
			//ALERTS
			$('.close').on('click', function (e) {
				e.preventDefault();
				$(this).closest('.alert').hide(400);
			});
			

			
			//PRELOADER
			$('.preloader').fadeOut();
		},
	}

})(jQuery);