export function tab_function() {
    var plot_container = document.querySelector('.plot-container');
    // Get the url from the plot container.

    var url = plot_container.getAttribute("data-url");

    $.ajax({
        url: url,
        method: 'GET',
        success: plot_function,
        error: error_handler
    });
}


function plot_function(response) {
    const loading_div = document.querySelector('.lds-ellipsis');
    var plot_container = document.querySelector('.plot-container');
    if (plot_container === null) {
        return;
    }

    var div_key = plot_container.getAttribute('data-key');

    if (div_key && div_key === response.key) {

        // Remove loading spinner div
        if (loading_div !== null) {
            loading_div.remove();
        }

        // Create the Plotly chart
        Plotly.newPlot('plot-container', response.chart_json.data, response.chart_json.layout, { responsive: true });
    }
}

function error_handler(error) {
    console.log(error);
}
