// Add an event listener for the DOMContentLoaded event
document.addEventListener("DOMContentLoaded", function () {
    let summary_polling_function = startPolling(true);
    let detailed_polling_function = startPolling(false);
    summary_polling_function();
    detailed_polling_function();
});

export function startPolling(summary) {
    make_step_containers_unclickable(summary);
    make_refresh_button_unclickable(summary);

    function get_data_status(summary) {
        let url = (summary) ? '/summary_data_status' : '/detailed_data_status';

        fetch(url)
            .then(response => response.json())
            .then(data => {

                // If data.message is Null, that means that there is no record of us ever having fetched data for this
                // user. If this is the summary refresh request, hit the refresh endpoint and keep polling as long as
                // the response to the refresh request isn't an error.
                if (data.status === null) {
                    if (summary) {
                        let refresh_data_function = get_refresh_data_function(
                            summary,
                            (data) => {
                                // If the refresh message has been accepted, update the log message and continue polling.
                                add_log_line_to_log(summary, data.message);
                                setTimeout(get_data_status, 2000, summary)
                            },
                            (data) => {
                                // If the refresh message is unsuccessful, then stop polling and unlock the refresh button.
                                add_log_line_to_log(summary, data.message);
                                make_refresh_button_clickable(summary);
                            }
                        );
                        refresh_data_function();
                        return;
                    } else {
                        // Otherwise if it's detailed, just log it, stop polling, and unlock the refresh button.
                        add_log_line_to_log(summary, data.message);
                        make_refresh_button_clickable(summary);
                    }
                } else {

                    // Otherwise update the content of the log container.
                    add_log_line_to_log(summary, data.message);

                    if (data.stop_polling) {
                        if (data.status == 'finished') {
                            make_step_containers_clickable(summary);
                        }
                        make_refresh_button_clickable(summary);
                    } else {
                        setTimeout(get_data_status, 2000, summary)
                    }
                }
            })
            .catch(error => {
                console.error('Error polling endpoint:', error);
            });
    }

    return function () {
        get_data_status(summary);
    };
}

function make_step_containers_clickable(summary) {
    // Select all elements with the class 'step-container'
    const stepContainers = document.querySelectorAll('.step-container');

    // Loop through each element and remove the 'greyed-out' class
    stepContainers.forEach((element) => {
        // download-data is a special case. We never want to grey/ungray it.
        if (element.id !== 'download-data') {
            if (element.classList.contains('summary') == summary) {
                element.classList.remove('greyed-out');
            }
        }
    });
}

export function make_step_containers_unclickable(summary) {
    // Select all elements with the class 'step-container'
    const stepContainers = document.querySelectorAll('.step-container');

    // Loop through each element
    stepContainers.forEach((element) => {
        // download-data is a special case. We never want to grey/ungray it.
        if (element.id !== 'download-data') {
            if (element.classList.contains('summary') == summary) {
                element.classList.add('greyed-out');
            }
        }
    });
}

export function make_refresh_button_clickable(summary) {
    let id = (summary) ? 'summary-refresh-button' : 'detailed-refresh-button';
    let refresh_button = document.getElementById(id);
    refresh_button.classList.remove('greyed-out');
}


export function make_refresh_button_unclickable(summary) {
    let id = (summary) ? 'summary-refresh-button' : 'detailed-refresh-button';
    let refresh_button = document.getElementById(id);
    refresh_button.classList.add('greyed-out');
}

export function add_event_to_summary_refresh_button() {
    const buttonDiv = document.getElementById('summary-refresh-button');
    let summary = true;

    let button_function = get_refresh_data_function(summary, (data) => {
        add_log_line_to_log(summary, data.message);
        let poll_function = startPolling(true);
        poll_function();
    }, (data) => {
        add_log_line_to_log(summary, data.message);
    });

    buttonDiv.addEventListener('click', () => {
        // Only call the button function if the button isn't greyed out.
        if (!buttonDiv.classList.contains('greyed-out')) {
            button_function();
        }
    });
}

export function add_event_to_detailed_refresh_button() {
    const buttonDiv = document.getElementById('detailed-refresh-button');
    let summary = false;

    let button_function = get_refresh_data_function(summary, (data) => {
        add_log_line_to_log(summary, data.message);
        let poll_function = startPolling(false);
        poll_function();
    }, (data) => {
        add_log_line_to_log(summary, data.message);
    });

    buttonDiv.addEventListener('click', () => {
        // Only call the button function if the button isn't greyed out.
        if (!buttonDiv.classList.contains('greyed-out')) {
            button_function();
        }
    });
}

function get_refresh_data_function(summary, f_refresh_success, f_refresh_fail) {
    function attempt_refresh_data() {
        var url = (summary) ? 'refresh_summary_data' : 'refresh_detailed_data';
        fetch(url).then(response => response.json())
            .then(data => {
                if (data.refresh_accepted) {
                    f_refresh_success(data);
                } else {
                    f_refresh_fail(data);
                }
            }).catch(error => {
                console.error('Error polling endpoint:', error);
            })
    }
    return attempt_refresh_data
}

function add_log_line_to_log(summary, message) {
    var logContainer = document.getElementById((summary) ? 'summary-log-container-text' : 'detailed-log-container-text');
    logContainer.innerHTML = message;
}
