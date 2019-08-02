$(document).ready(function() {
    
    /* For the sticky navigation */
    $('.js--section-features').waypoint(function(direction) {
        if (direction == "down") {
            $('nav').addClass('sticky');
        } else {
            $('nav').removeClass('sticky');
        }
    }, {
      offset: '60px;'
    });


    /* Mobile navigation */
    $('.js--nav-icon').click(function() {
        var nav = $('.js--main-nav');
        //var user_nav = $('.js--user-nav')
        var icon = $('.mobile-nav-image');

        nav_var = "/static/images/nav-var.png"
        nav_cross = "/static/images/nav-cross.png"
        
        nav.slideToggle(200);
        
        
        console.log(icon.attr("src"), icon.attr("src").indexOf(nav_var))
        
        if (icon.attr("src").indexOf(nav_var) > -1){
            icon.attr("src", nav_cross)
        } else {
            icon.attr("src", nav_var)
        }

        /*
        if (icon.hasClass('ion-navicon-round')) {
            icon.addClass('ion-close-round');
            icon.removeClass('ion-navicon-round');
        } else {
            icon.addClass('ion-navicon-round');
            icon.removeClass('ion-close-round');
        }        
        */
    });

});