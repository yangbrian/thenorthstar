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
    //var lastScroll = 0;
    //$(window).scroll(function (e) {
    //    var scroll = $(this).scrollTop();
    //    if (scroll > lastScroll) {
    //        // scrolling down
    //
    //        if ((question + 1) != total && passedCenter($('.question:eq(' + (question + 1) + ')'), false)) {
    //            $('.question:eq(' + (question) + ')').removeClass('current');
    //            question++;
    //            $('.question:eq(' + (question) + ')').addClass('current');
    //        }
    //    } else {
    //        // scrolling up
    //        if ((question - 1) >= 0 && passedCenter($('.question:eq(' + (question - 1) + ')'), true)) {
    //
    //            $('.question:eq(' + (question) + ')').removeClass('current');
    //            question--;
    //            $('.question:eq(' + (question) + ')').addClass('current');
    //        }
    //    }
    //});
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

    var locationList = data.locationMap;
    var locations = {};

    $.each(locationList, function(index, value) {
        locations[value[0]] = {
            long: value[2],
            lat: value[1],
            city: value[3]
        }
    });

    console.log(locations);

    $.each(flights, function(index, value) {
        var newRow = $('<tr>')
            .append($('<td>').html(value.destination))
            .append($('<td>').html(value.time))
            .append($('<td>').html(value.date))
            .append($('<td>').html(value.fare));

        newRow.on('click', function () {
            console.log("row clicked");
            amcharts(locations[value.destination].long, locations[value.destination].lat, locations[value.destination].city);
        });
        $('#results-table').append(
            newRow
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


var amcharts = function(long, lat, city) {

    console.log("Amcharts");
    console.log(long + ", " + lat);

    // create AmMap object
    var map = new AmCharts.AmMap();
    // set path to images
    map.pathToImages = "/static/am-images/";

    /* create data provider object
     map property is usually the same as the name of the map file.

     getAreasFromMap indicates that amMap should read all the areas available
     in the map data and treat them as they are included in your data provider.
     in case you don't set it to true, all the areas except listed in data
     provider will be treated as unlisted.
     */

    //Use Below for adding Labels (dots, populated based on flights that fit criteria)
    //addLabel(x, y, text, align, size, color, rotation, alpha, bold, url)
    //allLabels property, type Array[Label] with format above

    originLong= -74.0059;
    originLat= 40.7127;
    originName= "New York City";

    destinLong= long;
    destinLat= lat;
    destinName= city;

    //destinLong= -40.639    //-71.0589
    //destinLat= -73.779
    //destinName= "new york not city"




    var dataProvider = {
        map: "usa2High",
        //manually posts dot at given Long/Lat, circle, color, label, title, description,
        images:[
            //Origin Point
            {latitude:originLat,
                longitude:originLong,
                type:"circle",
                color:"#efd000",
                scale:1.2,
                label:"New York",
                labelShiftY:2,
                zoomLevel:3,
                title: "(Origin) "+ originName,
                labelColor:"#f2001f",
                labelRollOverColor:"#f2d300",
                description:"Placeholder string"},

            //Destination Points
            {latitude:destinLat,
                longitude:destinLong,
                type:"circle",
                color:"#f2001f",
                scale:0.8,
                label:city,
                labelShiftY:2,
                zoomLevel:3,
                title: "(Destination) "+ destinName,
                labelColor:"#f2001f",
                labelRollOverColor:"#f2d300",
                rollOverColor:"#f2d300",
                description:city + " is the second coolest city in the United States."
    }
        ],




        "lines": [
            {
                id:"line1",
                "latitudes": [originLat, destinLat], //MUST MAKE DYNAMIC
                "longitudes": [originLong, destinLong], //MUST MAKE DYNAMIC

                "arc": -0.8,
                "alpha": 0.65,
                "arrowColor": "#f2001f",
                "arrow": "middle",
                "arrowSize": 6,
                "arrowAlpha": 0.65,
                //"color": "#f2d300", //gold
                "color": "#f2001f", //red
                "thickness": 2.0,
                "arrowAlpha": 0.9
            }
        ],


        "allLabels": [
            {
                "color": "#f2001f"
            }
        ],


        /*
         "imagesSettings": {
         "alpha": 0.5,
         "adjustAnimationSpeed":true,
         "arc": 0.8,
         "centered": true,
         "color": "#f2d300"

         }

         */



        "getAreasFromMap":true



    };
    // pass data provider to the map object
    map.dataProvider = dataProvider;

    /* create areas settings
     * autoZoom set to true means that the map will zoom-in when clicked on the area
     * selectedColor indicates color of the clicked area.
     */
    map.areasSettings = {
        autoZoom: true,
        selectedColor: "#194989",
        color: "#002f6d",
        rollOverOutlineColor: "#f2d300"
    };

    // let's say we want a small map to be displayed, so let's create it
    map.smallMap = new AmCharts.SmallMap();

    // write the map to container div
    map.write("mapdiv");




};
