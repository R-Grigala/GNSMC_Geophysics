document.addEventListener("DOMContentLoaded", function() {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    const geophysicLoggingTableContainer = document.getElementById('geophysicLoggingTableContainer');
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");

    // Fetch data from API endpoint geophysic_logging
    fetch(`/api/geophysic_logging/${geophysicalId}`)
        .then(response => response.json())
        .then(data => {

            // Check if data is an array
            if (Array.isArray(data)) {
                const geophysicLoggingTable = document.getElementById('geophysicLoggingTable');

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
                    geophysicLoggingTable.innerHTML += row;
                });
            }else{
                // If data is not an array, hide the table
                geophysicLoggingTableContainer.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});

let geophysicLoggingId = null;

// Open the modal for creating or editing a GeophysicSeismic record
function openGeophysicLoggingModal(editMode = false, geophyLoggingId = null) {
    const modalTitle = document.getElementById('GeophysicLoggingModalTitle');
    const submitButton = document.getElementById('submitGeophysicLoggingBtn');
    const form = document.getElementById('GeophysicLoggingForm');
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    
    isEditMode = editMode;
    currentGeophysicalId = geophysicalId;
    geophysicLoggingId = geophyLoggingId;

    if (editMode) {
        modalTitle.textContent = "გეოფიზიკური კაროტაჟის განახლება";
        submitButton.textContent = "განახლება";
        fetchGeophysicLoggingData(currentGeophysicalId, geophysicLoggingId);
    } else {
        modalTitle.textContent = "სეისმური პროფილის დამატება";
        submitButton.textContent = "დამატება";
        form.reset();
    }

    const modal = new bootstrap.Modal(document.getElementById('GeophysicLoggingModal'));
    modal.show();
}

// Fetch data for editing a GeophysicLogging record
function fetchGeophysicLoggingData(geophysicalId, geophysicLoggingId) {
    fetch(`/api/geophysic_logging/${geophysicalId}/${geophysicLoggingId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('geophysicLoggingId').value = data.id;
                document.getElementById('logging_longitude').value = data.longitude;
                document.getElementById('logging_latitude').value = data.latitude;
                document.getElementById('logging_profile_length').value = data.profile_length;

            } else {
                alert('გეოფიზიკური კაროტაჟი არ მოიძებნა.');
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

function submitGeophysicLoggingForm(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('GeophysicLoggingForm'));
    const url = isEditMode ? `/api/geophysic_logging/${currentGeophysicalId}/${geophysicLoggingId}` : `/api/geophysic_logging/${currentGeophysicalId}`;
    const method = isEditMode ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + JSON.stringify(data)); // Handle errors
        } else {
            alert(data.message);
            window.location.reload(); // Reload the page to reflect changes
        }
        
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error: გეოფიზიკური კაროტაჟის დამატება რედაქტირებისას.');
    });
}

document.getElementById('GeophysicLoggingForm').onsubmit = submitGeophysicLoggingForm;

function deleteGeophysicLogging(id) {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");

    if (confirm('ნამდვილად გსურთ გეოფიზიკური კაროტაჟის წაშლა?')) {
        fetch(`/api/geophysic_logging/${geophysicalId}/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                // Optionally, remove the row from the table
                const row = document.querySelector(`tr[data-geophysicLogging-id="${id}"]`);
                if (row) {
                    row.remove();
                }
            } else if (data.error) {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting record.');
        });
    }
}