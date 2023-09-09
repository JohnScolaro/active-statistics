export function tab_function() {
    var plot_container = document.querySelector('.table-container');
    // Get the url from the trivia container.

    var url = plot_container.getAttribute("data-url");

    $.ajax({
        url: url,
        method: 'GET',
        success: table_function,
        error: error_handler
    });
}


function table_function(response) {
    const loading_div = document.querySelector('.lds-ellipsis');
    var table_container = document.querySelector('.table-container');
    if (table_container === null) {
        return;
    }

    var div_key = table_container.getAttribute('data-key');

    if (div_key && div_key === response.key) {

        // Remove loading spinner div
        if (loading_div !== null) {
            loading_div.remove();
        }

        // Generate the table from the data
        let show_headings = response.chart_json.show_headings
        let table_data = response.chart_json.table_data
        let heading_order = response.chart_json.heading_order

        const table = document.createElement("table");
        const thead = document.createElement("thead");
        const tbody = document.createElement("tbody");

        if (show_headings) {
            const headingRow = document.createElement("tr");
            for (const column of heading_order) {
                const th = document.createElement("th");
                th.textContent = column;
                headingRow.appendChild(th);
            }
            thead.appendChild(headingRow);
        }
        // Create data rows
        const numRows = Object.values(table_data)[0].length;
        for (let i = 0; i < numRows; i++) {
            const row = document.createElement("tr");
            for (const column of heading_order) {
                const td = document.createElement("td");
                td.innerHTML = table_data[column][i];
                row.appendChild(td);
            }
            tbody.appendChild(row);
        }

        table.appendChild(thead);
        table.appendChild(tbody);
        table_container.appendChild(table);

    }
}

function error_handler(error) {
    console.log(error);
}
