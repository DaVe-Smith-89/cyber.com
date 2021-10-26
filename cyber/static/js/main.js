
//navigation bar drop down

// const { AOS } = require("./aos");

$(document).ready(function(){

    // navigation bar togle
    $('nav button').click(function(){    
        // $('.nav-bar').css('height', '50vh');
        $('.nav-bar').toggle(500);
    });

    // aos int
    AOS.init();

    $('.btn-ex').click(function(){
        // $('.alert-box').hide();
        $('.alert-box').css('display', 'none')
    });

});





