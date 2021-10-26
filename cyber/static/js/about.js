
$(document).ready(function(){
    if ($(window).width() < 415) {
        // $('.nav-bar').toggle(500);
        window.scroll(0, 800);
    } else if ($(window).width() < 769) {
        // $('.nav-bar').toggle(500);
        window.scroll(0, 770);
    } else if ($(window).width() < 1171) {
        // $('.nav-bar').toggle(500);
        window.scrollTo(0, 550);
    } else {
        window.scrollTo(0, 450);
    }
})
