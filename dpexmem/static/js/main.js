$(document).ready(function() {
	// Burger Menu JS
	$(".burger-menu").click(function() {
        // Sidebar JS
        $(".fixed-sidebar").toggleClass("active");
        // Mobile Burger Menu JS
        $(".hamburger-menu").toggleClass("active");
        // Body JS
    });
	// Mobile Sidebar Dropdown JS
	$(".mob-menu-listing > li > a").click(function(e) {
		$(".mob-menu-listing > li > a").parent().removeClass("active");
		$(this).parent().addClass("active");
		$(".mob-menu-listing > li > ul").slideUp(), $(this).next().is(":visible") || $(this).next().slideDown()
	});
});