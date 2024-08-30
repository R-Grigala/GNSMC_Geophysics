document.addEventListener("DOMContentLoaded", function() {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    const geophysicElectricTableContainer = document.getElementById('geophysicElectricTableContainer');
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");

    // Fetch data from API endpoint geophysic_logging
    fetch(`/api/geophysic_electrical/${geophysicalId}`)
        .then(response => response.json())
        .then(data => {

            // Check if data is an array
            if (Array.isArray(data)) {
                const geophysicElectricTable = document.getElementById('geophysicElectricTable');

                data.forEach(data => {
                    const archivalImgLink = data.archival_img ? 
                    `<a href="/${projectId}/geophysical/${data.geophysical_id}/logging/archival_img/${data.archival_img}" target="_blank">${data.archival_img}</a>` : 
                    '---';

                    const archivalExcelLink = data.archival_excel ? 
                        `<a href="/${projectId}/geophysical/${data.geophysical_id}/logging/archival_excel/${data.archival_excel}" target="_blank">${data.archival_excel}</a>` : 
                        '---';

                    const archivalPdfLink = data.archival_pdf ? 
                    `<a href="/${projectId}/geophysical/${data.geophysical_id}/logging/archival_pdf/${data.archival_pdf}" target="_blank">${data.archival_pdf}</a>` : 
                    '---';

                    const row = `
                        <tr data-geophysicLogging-id="${data.id}">
                            <td>${data.longitude}</td>
                            <td>${data.latitude}</td>
                            <td>${data.profile_length}</td>
                            <td>${archivalImgLink}</td>
                            <td>${archivalExcelLink}</td>
                            <td>${archivalPdfLink}</td>
                            <td>
                                <a class="btn btn-sm btn-info" onclick="openGeophysicLoggingModal(true, ${data.id})">Edit</a>
                            </td>
                            <td>
                                <img src="/static/img/x_button.png" style="width: 25px; height: 25px; cursor: pointer;" alt="Delete" class="delete-icon" onclick="deleteGeophysicLogging(${data.id})">
                            </td>
                        </tr>
                    `;
                    geophysicElectricTable.innerHTML += row;
                });
            }else{
                // If data is not an array, hide the table
                geophysicElectricTableContainer.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});