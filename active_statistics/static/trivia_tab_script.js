export function tab_function() {
    var plot_container = document.querySelector('.trivia-container');
    // Get the url from the trivia container.

    var url = plot_container.getAttribute("data-url");

    $.ajax({
        url: url,
        method: 'GET',
        success: trivia_function,
        error: error_handler
    });
}


function trivia_function(response) {
    const loading_div = document.querySelector('.lds-ellipsis');
    var trivia_container = document.querySelector('.trivia-container');
    if (trivia_container === null) {
        return;
    }

    var div_key = trivia_container.getAttribute('data-key');

    if (div_key && div_key === response.key) {

        // Remove loading spinner div
        if (loading_div !== null) {
            loading_div.remove();
        }

    }

    console.log(response)

    let trivia_data = response.chart_json

    const table = document.createElement('table');

    // Populate the table with data
    trivia_data.forEach(rowData => {
        const row = document.createElement('tr');

        rowData.forEach((cellData, index) => {
            const cell = document.createElement('td');

            // If the cellData is a URL and not null, create a link element
            if (index === 2 && cellData !== null) {
                const link = document.createElement('a');
                link.href = cellData;
                link.textContent = 'View on Strava';
                link.target = '_blank'; // Open the link in a new tab
                cell.appendChild(link);
            } else {
                cell.textContent = cellData || ''; // If cellData is null, leave the cell empty
            }

            row.appendChild(cell);
        });

        table.appendChild(row);
    });

    // Append the table to the container
    trivia_container.appendChild(table);
}

function error_handler(error) {
    console.log(error);
}
