import { startPolling } from "./home_script.js";

$(document).ready(function () {
    $('.step-container').click(step_container_clicked);
});

function step_container_clicked() {
    // Check if the clicked element has the "greyed-out" class
    if ($(this).hasClass('greyed-out')) {
        return; // Exit the function without performing any action
    }

    var url = $(this).data('url');

    // Remove 'clicked' class from all divs
    $('.step-container').removeClass('clicked');

    // Add 'clicked' class to the clicked div
    $(this).addClass('clicked');

    // Call the page endpoint to get the new page and re-render the main content container
    $.ajax({
        url: url,
        method: 'GET',
        success: (response) => {
            // Replace the main content container with the response we get.
            $('.main-content-container').html(response);

            // In the special case that this is the "Download Strava Data" button, also
            // block access to all other buttons and start polling again to unblock them.
            if ($(this).attr('id') === 'download-data') {
                let summary_polling_function = startPolling(true);
                let detailed_polling_function = startPolling(false);
                summary_polling_function();
                detailed_polling_function();
            }
        },
        error: error_handler
    });
}

function error_handler(error) {
    console.log(error);
}
