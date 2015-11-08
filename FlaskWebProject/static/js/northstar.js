/**
 * North Star - Main Script
 * @author Brian Yang
 */

/*jslint browser: true, devel: true, plusplus: true*/
/*global $, jQuery*/

/* Question navigation */
$(document).ready(function () {
    "use strict";
    
    var total, question = 0;
    total = $('.question').length;
    
    $('.question:eq(' + question + ')').addClass('current');
    
    /**
     * Move onto the next question
     */
    function nextQuestion() {

        $('.question:eq(' + question + ')').removeClass('current');


        question++;

        while (question < total - 1 && !$('.question:eq(' + question + ')').is(':visible')) {
            question++;
        }

        if (question < total && $('.question:eq(' + question + ')').is(':visible')) {
            $.scrollTo('.question:eq(' + question + ') p', 500, {offset: -$(window).height() / 2});
            
            $('.question:eq(' + question + ')').addClass('current');
        } else {
            $.scrollTo('#submit', 500);
        }
        
    }

    $( "#startdatepicker" ).datepicker({"dateFormat": "yy-mm-dd"});
    $( "#enddatepicker" ).datepicker({"dateFormat": "yy-mm-dd"});

    /**
     * Move onto next question by enter key 
     */
    $('.input-field').keypress(function (e) {
        if (e.which === 13) {
            console.log("Next question");
            nextQuestion();
        }
    });
    
    $('.radio').on('change', function () {
        console.log("Next question");
        nextQuestion();
    });
    
    $('.slider').each(function () {
        $(this).slider({
            range: "min",
            min: 1,
            max: 5,
            value: 1,
            slide: function (event, ui) {
                $(ui.handle).parent().next().val(ui.value).change();
            }
        });
    });

    $('.slider-label').click(function () {
        $(this).toggleClass('label-selected');

        if ($(this).hasClass('label-selected')) {

            // reset slider to 1
            $(this).next().slider('value', 1);
            $(this).next().next().val(1).change();
            $(this).next().fadeIn();
        } else {
            $(this).next().fadeOut();

            // not selected anymore so set value to 1
            $(this).next().next().val(0).change();
        }
    });
    
    $('.dest-slider-result').change(function () {
        
        var extraQuestion = $('.area-question');
        extraQuestion.attr('style', '');
        $('.dest-slider-result').each(function (index, value) {
            
            if ($(value).val() > 0) {
                console.log(extraQuestion[index]);
                $(extraQuestion[index]).css('display', 'block');
            }
        });
    
    });

    $('.continue').click(function () {
        nextQuestion();
    });

    $('#main-form').submit(function (e) {
        $('.loader').fadeIn(100);

        e.preventDefault();


        $(this).serialize();



        $.post( "/submit", $(this).serialize())
            .done(function( data ) {
                $.scrollTo('#intro', 1000);

                displayData(data, function() {
                    $('#main-form').fadeOut();
                    $('#results').fadeIn();
                    $('.loader').fadeOut(500);
                });


            });
    });
});

var flights = [];
var uniqueFlights = {};
var offset = 0;

function displayData(data, callback) {

    var results = data.result;
    $.each(results, function(index, value) {
        var flight = {
            origin: value[0],
            destination: value[1],
            time: value[2],
            date: value[3],
            fare: value[4]
        };
        flights.push(flight);
    });

    $.each(flights, function(index, value) {
        $('#results-table').append(
            $('<tr>')
                .append($('<td>').html(value.destination))
                .append($('<td>').html(value.time))
                .append($('<td>').html(value.date))
                .append($('<td>').html(value.fare))
        );
    });





    if (callback)
        callback();
}

/* Facebook integration */
$(document).ready(function() {
    $.ajaxSetup({ cache: true });
    $.getScript('//connect.facebook.net/en_US/sdk.js', function(){
        FB.init({
            appId: '1655950804685867',
            cookie     : true,  // enable cookies to allow the server to access the session
            xfbml      : true,  // parse social plugins on this page
            version: 'v2.4' // or v2.0, v2.1, v2.2, v2.3
        });
        FB.getLoginStatus(function(response) {
            statusChangeCallback(response);
        });
    });

});

function checkLoginState() {
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
    });
}

function testAPI() {
    FB.api('/me?fields=id,name,birthday,relationship_status,hometown', function(response) {
        $('.fb_iframe_widget').fadeOut();

        // populate the hidden form fields
        if (response.birthday) {

            var age = calculateAge(response.birthday);;
            $('input[name="age"]').val(age);
            $('label[for="age"]').fadeIn().append(age);
        }

        if (response.hometown) {

            $('input[name="hometown"]').val(response.hometown.name);
            $('label[for="hometown"]').fadeIn().append(response.hometown.name);
        }

        if (response.relationship_status) {
            $('input[name="relationship"]').val(response.relationship_status);
            $('label[for="relationship"]').fadeIn().append(response.relationship_status);
        }


        $('#status').html('Thanks for logging in, ' + response.name + '! The following information will be used to further personalize your results: ');
    });
}

function statusChangeCallback(response) {

    if (response.status === 'connected') {
        // Logged into your app and Facebook.
        testAPI();
    } else if (response.status === 'not_authorized') {
        // The person is logged into Facebook, but not your app.
        $('#status').html('Please log in for greater personalization.');
    } else {
        // The person is not logged into Facebook, so we're not sure if
        // they are logged into this app or not.
        $('#status').html('Please log into Facebook for greater personalization.');
    }
}

function calculateAge(date) {
    var today = new Date();
    var bday = new Date(date);

    var age = today.getFullYear() - bday.getFullYear();

    var m = today.getMonth() - bday.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < bday.getDate()))
        age--;

    return age;
}

$(window).scroll()