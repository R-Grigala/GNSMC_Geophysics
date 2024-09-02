document.addEventListener("DOMContentLoaded", function() {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    const geophysicElectricTableContainer = document.getElementById('geophysicElectricTableContainer');
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");

    // Fetch data from API endpoint geophysic_electrical
    fetch(`/api/geophysic_electrical/${geophysicalId}`)
        .then(response => response.json())
        .then(data => {

            // Check if data is an array
            if (Array.isArray(data)) {
                const geophysicElectricTable = document.getElementById('geophysicElectricTable');

                data.forEach(data => {
                    const archivalImgLink = data.archival_img ? 
                    `<a href="/${projectId}/geophysical/${data.geophysical_id}/electrical/archival_img/${data.archival_img}" target="_blank">${data.archival_img}</a>` : 
                    '---';

                    const archivalExcelLink = data.archival_excel ? 
                        `<a href="/${projectId}/geophysical/${data.geophysical_id}/electrical/archival_excel/${data.archival_excel}" target="_blank">${data.archival_excel}</a>` : 
                        '---';

                    const archivalPdfLink = data.archival_pdf ? 
                    `<a href="/${projectId}/geophysical/${data.geophysical_id}/electrical/archival_pdf/${data.archival_pdf}" target="_blank">${data.archival_pdf}</a>` : 
                    '---';

                    const row = `
                        <tr data-geophysicElectrical-id="${data.id}">
                            <td>${data.longitude}</td>
                            <td>${data.latitude}</td>
                            <td>${data.profile_length}</td>
                            <td>${archivalImgLink}</td>
                            <td>${archivalExcelLink}</td>
                            <td>${archivalPdfLink}</td>
                            <td>
                                <img src="/static/img/edit_icon.png" style="width: 30px; height: 30px; cursor: pointer;" alt="Edit" onclick="openGeophysicElectricalModal(true, ${data.id})">
                            </td>
                            <td>
                                <img src="/static/img/trash_icon.png" style="width: 30px; height: 30px; cursor: pointer;" alt="Delete" class="delete-icon" onclick="deleteGeophysicElectrical(${data.id})">
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

let geophysicElectricalId = null;

// Open the modal for creating or editing a GeophysicElectrical record
function openGeophysicElectricalModal(editMode = false, geophyElectricalId = null) {
    const modalTitle = document.getElementById('GeophysicElectricalModalTitle');
    const submitButton = document.getElementById('submitGeophysicElectricalBtn');
    const form = document.getElementById('GeophysicElectricalForm');
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    
    isEditMode = editMode;
    currentGeophysicalId = geophysicalId;
    geophysicElectricalId = geophyElectricalId;

    if (editMode) {
        modalTitle.textContent = "ელექტრული პროფილის განახლება";
        submitButton.textContent = "განახლება";
        fetchGeophysicElectricalData(currentGeophysicalId, geophysicElectricalId);
    } else {
        modalTitle.textContent = "ელექტრული პროფილის დამატება";
        submitButton.textContent = "დამატება";
        form.reset();
    }

    const modal = new bootstrap.Modal(document.getElementById('GeophysicElectricalModal'));
    modal.show();
}

// Fetch data for editing a GeophysicElectrical record
function fetchGeophysicElectricalData(geophysicalId, geophysicElectricalId) {
    fetch(`/api/geophysic_electrical/${geophysicalId}/${geophysicElectricalId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('geophysicElectricalId').value = data.id;
                document.getElementById('electrical_longitude').value = data.longitude;
                document.getElementById('electrical_latitude').value = data.latitude;
                document.getElementById('electrical_profile_length').value = data.profile_length;

            } else {
                alert('ელექტრული პროფილი არ მოიძებნა.');
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

function submitGeophysicElectricalForm(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('GeophysicElectricalForm'));
    const url = isEditMode ? `/api/geophysic_electrical/${currentGeophysicalId}/${geophysicElectricalId}` : `/api/geophysic_electrical/${currentGeophysicalId}`;
    const method = isEditMode ? 'PUT' : 'POST';

    // Retrieve the JWT token from sessionStorage (or wherever you store it)
    const token = sessionStorage.getItem('access_token');

    // makeApiRequest is in the globalAccessControl.js
    makeApiRequest(url, {
        method: method,
        headers: {
            'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error); // Handle errors
            window.location.reload();
        } else {
            alert(data.message);
            window.location.reload(); // Reload the page to reflect changes
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error: ელექტრული პროფილის დამატება რედაქტირებისას.');
    });
}

document.getElementById('GeophysicElectricalForm').onsubmit = submitGeophysicElectricalForm;


function deleteGeophysicElectrical(id) {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");

    if (confirm('ნამდვილად გსურთ ელექტრული პროფილის წაშლა?')) {

        // Retrieve the JWT token from sessionStorage (or wherever you store it)
        const token = sessionStorage.getItem('access_token');
        
        // makeApiRequest is in the globalAccessControl.js
        makeApiRequest(`/api/geophysic_electrical/${geophysicalId}/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                // Optionally, remove the row from the table
                const row = document.querySelector(`tr[data-geophysicElectrical-id="${id}"]`);
                if (row) {
                    row.remove();
                }
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting record.');
        });
    }
}