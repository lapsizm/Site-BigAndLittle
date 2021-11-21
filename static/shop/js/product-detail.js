
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
