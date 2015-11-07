/**
 * The North Start - Main Script
 * @author Brian Yang
 */

/*jslint browser: true, devel: true, plusplus: true*/
/*global $, jQuery*/

/* Question navigation */
$(document).ready(function () {
    "use strict";
    
    $(document).foundation();
    
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
    
    
});