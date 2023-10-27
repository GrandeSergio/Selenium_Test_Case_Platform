$(document).ready(function() {
    // Get the current URL
    var currentUrl = window.location.pathname;

    // Loop through each sidebar link
    $('.sidebar-link').each(function() {
        // Get the href attribute of the link
        var linkUrl = $(this).attr('href');

        // Check if the current URL matches the link URL
        if (currentUrl === linkUrl) {
            // Add the active class to the link
            $(this).addClass('active');
        }
    });
});
window.addEventListener('DOMContentLoaded', function() {
    var containerHeight = document.querySelector('.main-container').offsetHeight;
    document.getElementById('custom-row').style.height = containerHeight + 'px';
});