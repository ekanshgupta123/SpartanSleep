/*  ---------------------------------------------------
    Template Name: Sona
    Description: Sona Hotel Html Template
    Author: Colorlib
    Author URI: https://colorlib.com
    Version: 1.0
    Created: Colorlib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Offcanvas Menu
    $(".canvas-open").on('click', function () {
        $(".offcanvas-menu-wrapper").addClass("show-offcanvas-menu-wrapper");
        $(".offcanvas-menu-overlay").addClass("active");
    });

    $(".canvas-close, .offcanvas-menu-overlay").on('click', function () {
        $(".offcanvas-menu-wrapper").removeClass("show-offcanvas-menu-wrapper");
        $(".offcanvas-menu-overlay").removeClass("active");
    });

    // Search model
    $('.search-switch').on('click', function () {
        $('.search-model').fadeIn(400);
    });

    $('.search-close-switch').on('click', function () {
        $('.search-model').fadeOut(400, function () {
            $('#search-input').val('');
        });
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
        Hero Slider
    --------------------*/
   $(".hero-slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: true,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        mouseDrag: false
    });

    /*------------------------
		Testimonial Slider
    ----------------------- */
    $(".testimonial-slider").owlCarousel({
        items: 1,
        dots: false,
        autoplay: true,
        loop: true,
        smartSpeed: 1200,
        nav: true,
        navText: ["<i class='arrow_left'></i>", "<i class='arrow_right'></i>"]
    });

    /*------------------
        Magnific Popup
    --------------------*/
    $('.video-popup').magnificPopup({
        type: 'iframe'
    });

    /*------------------
		Date Picker
	--------------------*/
    $(".date-input").datepicker({
        minDate: 0,
        dateFormat: 'dd MM, yy'
    });

    /*------------------
		Nice Select
	--------------------*/
    $("select").niceSelect();

    /*------------------
        Plus Minus Button for Guest selection (index.html)
    ------------------*/
    document.addEventListener('DOMContentLoaded', function () {
        const guestInput = document.getElementById('guest');
        const guestIncreaseButton = document.getElementById('guest-increase');
        const guestDecreaseButton = document.getElementById('guest-decrease');
        const form = document.querySelector('form');
    
        // Function to update the guest count and button states
        function updateGuestCount() {
            const guestCount = parseInt(guestInput.value);
    
            // Disable the minus button when the guest count is 1
            guestDecreaseButton.disabled = guestCount === 1;
    
            // You can use the guestCount value as needed in your code
        }
    
        // Initialize guest count
        updateGuestCount();
    
        // Increase button click
        guestIncreaseButton.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent form submission
            guestInput.value = parseInt(guestInput.value) + 1;
            updateGuestCount();
        });
    
        // Decrease button click
        guestDecreaseButton.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent form submission
            const guestCount = parseInt(guestInput.value);
            if (guestCount > 1) {
                guestInput.value = guestCount - 1;
                updateGuestCount();
            }
        });
    
        // Form submission
        form.addEventListener('submit', function (e) {
            // Prevent the default form submission
            e.preventDefault();
    
            // Handle form submission here, e.g., update URL or make an AJAX request
            // You can also manually trigger the form submission if needed
            // form.submit();
        });
    
        // Input field change
        guestInput.addEventListener('change', updateGuestCount);
    });

    /*------------------
        Event listener for hotel-card-book-now-button (index.html)
    --------------------*/
    document.querySelectorAll('.hotel-card-book-now-button').forEach(function(button) {
        button.addEventListener('click', function() {
            var hotelId = this.getAttribute('data-hotel-id');
            var cityCode = this.getAttribute('data-city-code');
            var checkIn = this.getAttribute('data-check-in');
            var checkOut = this.getAttribute('data-check-out');
            var guests = this.getAttribute('data-guests');
            var rooms = this.getAttribute('data-rooms');
            var hotelName = this.getAttribute('data-hotel-name');
            var countryCode = this.getAttribute('data-country-code');
            var distance = this.getAttribute('data-distance');
    
            var payNowBtn = document.getElementById('payNowBtn');
            var payLaterBtn = document.getElementById('payLaterBtn');
    
            payNowBtn.setAttribute('data-hotel-id', hotelId);
            payNowBtn.setAttribute('data-city-code', cityCode);
            payNowBtn.setAttribute('data-check-in', checkIn);
            payNowBtn.setAttribute('data-check-out', checkOut);
            payNowBtn.setAttribute('data-guests', guests);
            payNowBtn.setAttribute('data-rooms', rooms);
            payNowBtn.setAttribute('data-hotel-name', hotelName);
            payNowBtn.setAttribute('data-country-code', countryCode);
            payNowBtn.setAttribute('data-distance', distance);
    
            payLaterBtn.setAttribute('data-hotel-id', hotelId);
            payLaterBtn.setAttribute('data-city-code', cityCode);
            payLaterBtn.setAttribute('data-check-in', checkIn);
            payLaterBtn.setAttribute('data-check-out', checkOut);
            payLaterBtn.setAttribute('data-guests', guests);
            payLaterBtn.setAttribute('data-rooms', rooms);
            payLaterBtn.setAttribute('data-hotel-name', hotelName);
            payLaterBtn.setAttribute('data-country-code', countryCode);
            payLaterBtn.setAttribute('data-distance', distance);
        });
    });

})(jQuery);