$(document).ready(function () {
    var chart_div = document.getElementById('example-chart')
    const loading_div = document.querySelector('.lds-ellipsis');

    // Fetch the chart data asynchronously
    $.getJSON('/example_chart_data', function (chartData) {
        chartData = JSON.parse(chartData);

        // Remove the loading spinner div
        loading_div.remove();

        // Create the Plotly chart
        Plotly.newPlot(chart_div, chartData.data, chartData.layout, { responsive: true });
    });
});


// Get the modal and close button elements
const modal = document.getElementById("modal");
const closeModalButton = document.getElementById("close-modal");

// Function to check URL query parameters
function getQueryParameter(paramName) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(paramName);
}

const url_query_params = new URLSearchParams(window.location.search);
const rateLimitExceeded = getQueryParameter("rate_limit_exceeded");
const scopeIncorrect = getQueryParameter("scope_incorrect");

const modalTitle = document.querySelector(".modal-content h1");
const modalContent = document.querySelector(".modal-content p");

if (rateLimitExceeded === "True") {
    modalTitle.textContent = "Rate limit exceeded!";
    modalContent.textContent = "Sadly, when this app is popular, it goes over its limit of 6000 requests / day to the Strava API. Please bookmark this page and check back in a few days.";
    modal.style.display = "block";
} else if (scopeIncorrect === "True") {
    modalTitle.textContent = "Scope incorrect!";
    modalContent.textContent = "Please login again, but this time give this webapp access to the default scopes. Otherwise it can't request the data required to generate cool plots.";
    modal.style.display = "block";
}

// Function to close the modal
function closeModal() {
    modal.style.display = "none";
    removeQueryParams()
}

// Function to remove the query parameters
function removeQueryParams() {
    var url = window.location.href;
    var updatedUrl = url.split('?')[0]; // Remove query string
    history.replaceState({}, document.title, updatedUrl); // Update URL without query parameter
}

// Event listeners
closeModalButton.addEventListener("click", closeModal);

// Close the modal if the user clicks anywhere outside of it
window.addEventListener("click", function (event) {
    if (event.target === modal) {
        closeModal();
    }
});
