/**
 * The North Start - Main Script
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
        if (question + 1 !== total) {
            $('.question:eq(' + question + ')').removeClass('current');
        
            question++;
            
            $.scrollTo('.question:eq(' + question + ') p', 500, {offset: -$(window).height() / 2});
            
            $('.question:eq(' + question + ')').addClass('current');
        }
        
    }
    
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
    
    $('.dest-slider-result').change(function () {

        $('.continue').fadeIn();
        
        var extraQuestion = $('.area-question');
        extraQuestion.attr('style', '');
        $('.dest-slider-result').each(function (index, value) {
            
            if ($(value).val() > 1) {
                console.log(extraQuestion[index]);
                $(extraQuestion[index]).css('display', 'block');
            }
        });
    
    });
    
    $('.continue').click(function () {
        $(this).fadeOut();
        nextQuestion();
    });
});