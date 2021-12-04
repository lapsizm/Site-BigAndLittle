function burgerMenu(selector){
	let menu=$(selector);
	let button=$(".menu-open");
	let links= menu.find('.menu-link');
	let overlay = menu.find('.menu-burger_overlay');

	button.on('click',(e)=>{
		e.preventDefault();
		toggleMenu();
	});

	links.on('click',()=>toggleMenu());
	overlay.on('click',()=>toggleMenu());

	function toggleMenu(){
		menu.toggleClass('menu-burger');
	}
}

$(function() {
	burgerMenu('.menu');

	$('.slider').slick({
		slidesToShow: 1,
		slidesToScroll: 1,
		arrows: true,
		fade: true,
		autoplay: true,
		asNavFor: '.slider-nav'
	});

	$('.slider-nav').slick({
		slidesToShow: AnimationTimeline,
		slidesToScroll: 1,
		asNavFor: '.slider',
		dots: false,
		arrows: false,
		focusOnSelect: true
	});
});

