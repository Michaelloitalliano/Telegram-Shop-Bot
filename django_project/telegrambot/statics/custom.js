(function (jQuery) {
    "use strict";
    // Parallax Backgrounds
    jQuery.stellar({
        horizontalScrolling: false,
        scrollProperty: 'scroll',
        positionProperty: 'position'
    });
    // BG Color & Image
    jQuery('section,div').each(function(){
        var bg_color = jQuery(this).attr("data-color");
        if(bg_color){
            jQuery(this).css("background-color", "" + bg_color + "");
        }
        var url = jQuery(this).attr("data-image");
        if(url){
            jQuery(this).css("background-image", "url(" + url + ")");
        }
    });
    // Site preloader -- also uncomment the div in the header and the css style for #preloader
    jQuery(window).load(function(){
        jQuery('#preloader').fadeOut(
            'slow',
            function(){
                jQuery(this).remove();
            });
    });
    // Animated Progress Bar
    jQuery('.progress-bars').waypoint(function() {
            jQuery('.progress').each(function(){
                jQuery(this).find('.progress-bar').animate({
                    width:jQuery(this).attr('data-percent')
                },200);
            });},
        {
            offset: '100%',
            triggerOnce: true
        });
    // WOW
    new WOW().init();
    // init CubePortfolio
    if (jQuery('#js-grid-mosaic').length > 0){
        var portfolioSpace = jQuery('#js-grid-mosaic').attr('data-columnspace');
        var portfoliocol = jQuery('#js-grid-mosaic').attr('data-gallerycolumns');
        jQuery('#js-grid-mosaic').cubeportfolio({
            filters: '#js-filters-mosaic',
            layoutMode: 'mosaic',
            sortToPreventGaps: true,
            mediaQueries: [{
                width: 1500,
                cols: parseInt(portfoliocol, 10)
            }, {
                width: 1100,
                cols: parseInt(portfoliocol, 10)
            }, {
                width: 800,
                cols: 3
            }, {
                width: 480,
                cols: 2
            }, {
                width: 320,
                cols: 1
            }],
            defaultFilter: '*',
            animationType: 'quicksand',
            gapHorizontal: parseInt(portfolioSpace, 10),
            gapVertical: parseInt(portfolioSpace, 10),
            gridAdjustment: 'responsive',
            caption: 'zoom',
            displayType: 'sequentially',
            displayTypeSpeed: 100,

            // lightbox
            lightboxDelegate: '.cbp-lightbox',
            lightboxGallery: true,
            lightboxTitleSrc: 'data-title',
            lightboxCounter: '<div class="cbp-popup-lightbox-counter">{{current}} of {{total}}</div>'
        });
    }

    // Team Members
    if (jQuery('#js-grid-slider-team').length > 0){
        jQuery('#js-grid-slider-team').cubeportfolio({
            layoutMode: 'slider',
            drag: true,
            auto: false,
            autoTimeout: 5000,
            autoPauseOnHover: true,
            showNavigation: true,
            showPagination: false,
            rewindNav: true,
            scrollByPage: true,
            gridAdjustment: 'responsive',
            mediaQueries: [{
                width: 1500,
                cols: 4,
            }, {
                width: 1100,
                cols: 4,
            }, {
                width: 800,
                cols: 3,
            }, {
                width: 480,
                cols: 2,
                options: {
                    gapVertical: 20,
                }
            }, {
                width: 320,
                cols: 1,
                options: {
                    gapVertical: 20,
                }
            }],
            gapHorizontal: 0,
            gapVertical: 25,
            caption: '',
            displayType: 'fadeIn',
            displayTypeSpeed: 400,
        });
    }

    // Testimonials
    if (jQuery('#js-grid-slider-testimonials').length > 0){
        jQuery('#js-grid-slider-testimonials').cubeportfolio({
            layoutMode: 'slider',
            drag: true,
            auto: false,
            autoTimeout: 5000,
            autoPauseOnHover: true,
            showNavigation: true,
            showPagination: false,
            rewindNav: true,
            scrollByPage: false,
            gridAdjustment: 'responsive',
            mediaQueries: [{
                width: 0,
                cols: 1,
            }],
            gapHorizontal: 0,
            gapVertical: 0,
            caption: '',
            displayType: 'default',
        });
    }
    // Team Carousel
    var carousel_selector = jQuery('#team-xcarousel');
    carousel_selector.carousel({
        interval: false
    });
    var first_pickup = jQuery('ul.pickup li:first-child').find('img').attr('src');
    jQuery('.controls-holder .control-img').css('background','url('+first_pickup+') no-repeat');
    var pickup_li = jQuery('ul.pickup li');
    var cal_lnt;
    var lnt = pickup_li.length;
    var dvd_lnt = Math.ceil(lnt/2);
    cal_lnt = lnt-dvd_lnt;
    jQuery('.controls-holder .lefto ul').html(jQuery('ul.pickup li:lt('+dvd_lnt+')'));
    jQuery('.controls-holder .righto ul').html(pickup_li.slice(-cal_lnt));
    carousel_selector.on('slid.bs.carousel', function () {
        var pickup_img = jQuery(this).find('.item.active').attr('data-pickup-img');
        jQuery('.controls-holder .control-img').fadeTo('slow', 0.1, function(){
            jQuery(this).css('background', 'url(' + pickup_img + ') no-repeat');
        }).delay(100).fadeTo('slow', 1);
    });
    jQuery('.controls-holder .lefto ul li, .controls-holder .righto ul li').on('click',function(){
        var data_slide_index = parseInt(jQuery(this).attr('data-slide-index'), 10);
        jQuery('#team-xcarousel').carousel(data_slide_index);
    });
    // Flat Testimonials
    jQuery('.testimonials-flat').each(function(){
        var wiDth = jQuery(this).width();
        var new_wiDth = wiDth-300;
        jQuery(this).find('.flat-carousel').css('width',new_wiDth+'px');
    });
    jQuery('#carousel-testimonials').carousel({
        interval: false
    });
    jQuery('.flat-control li').on('click',function(){
        jQuery('.flat-control li').removeClass('active');
        jQuery(this).addClass('active');
    });
    // Video Popup
    jQuery('#vidModal').on('hide.bs.modal', function (e) {
        var video = jQuery(this).find('iframe').attr("src");
        jQuery(this).find('iframe').attr("src","");
        jQuery(this).find('iframe').attr("src",video);
    });
    // Side Menu
    jQuery('.menu-selector').on('click',function(e){
        e.preventDefault();
        jQuery('.cbp-spmenu').addClass('active');
        jQuery(this).hide();
    });
    jQuery('.cbp-spmenu h4').on('click',function(e){
        e.preventDefault();
        jQuery('.cbp-spmenu').removeClass('active');
        jQuery('.menu-selector').show();
    });
    // On Click Scroll
    var bodyOffset = jQuery('body').attr('data-body-offset');
    if(bodyOffset == ''){
        bodyOffset = 0;
    }
    jQuery(document).on("click", ".menu-item a", function(){
        var ths = jQuery(this);
        if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
            var target = jQuery(this.hash);
            target = target.length ? target : jQuery('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                jQuery('.navo li').removeClass('active');
                ths.parent().addClass('active');
                //console.log(ths.prev('li'));
                jQuery('html,body').animate({
                    scrollTop: target.offset().top - bodyOffset
                }, 1000,'easeInOutExpo');
                return false;
            }
        }
    });
    // On Scroll Add/Remove Nav Class
    jQuery(window).scroll(function () {
        if (jQuery(this).scrollTop() > 200) {
            jQuery('.navigation-bar.cyan-nav').addClass("navbar-fixed");
        } else {
            jQuery('.navigation-bar.cyan-nav').removeClass("navbar-fixed");
        }
    });
})(jQuery);