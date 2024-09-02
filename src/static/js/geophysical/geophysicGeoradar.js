document.addEventListener("DOMContentLoaded", function() {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    const geophysicGeoradarTableContainer = document.getElementById('geophysicGeoradarTableContainer');
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");

    // Fetch data from API endpoint geophysic_logging
    fetch(`/api/geophysic_georadar/${geophysicalId}`)
        .then(response => response.json())
        .then(data => {

            // Check if data is an array
            if (Array.isArray(data)) {
                const geophysicGeoradarTable = document.getElementById('geophysicGeoradarTable');

                data.forEach(data => {
                    const archivalImgLink = data.archival_img ? 
                    `<a href="/${projectId}/geophysical/${data.geophysical_id}/georadar/archival_img/${data.archival_img}" target="_blank">${data.archival_img}</a>` : 
                    '---';

                    const archivalExcelLink = data.archival_excel ? 
                        `<a href="/${projectId}/geophysical/${data.geophysical_id}/georadar/archival_excel/${data.archival_excel}" target="_blank">${data.archival_excel}</a>` : 
                        '---';

                    const archivalPdfLink = data.archival_pdf ? 
                    `<a href="/${projectId}/geophysical/${data.geophysical_id}/georadar/archival_pdf/${data.archival_pdf}" target="_blank">${data.archival_pdf}</a>` : 
                    '---';

                    const row = `
                        <tr data-geophysicGeoradar-id="${data.id}">
                            <td>${data.longitude}</td>
                            <td>${data.latitude}</td>
                            <td>${data.profile_length}</td>
                            <td>${archivalImgLink}</td>
                            <td>${archivalExcelLink}</td>
                            <td>${archivalPdfLink}</td>
                            <td>
                                <img src="/static/img/edit_icon.png" style="width: 30px; height: 30px; cursor: pointer;" alt="Edit" onclick="openGeophysicGeoradarModal(true, ${data.id})">
                            </td>
                            <td>
                                <img src="/static/img/trash_icon.png" style="width: 30px; height: 30px; cursor: pointer;" alt="Delete" onclick="deleteGeophysicGeoradar(${data.id})">
                            </td>
                        </tr>
                    `;
                    geophysicGeoradarTable.innerHTML += row;
                });
            }else{
                // If data is not an array, hide the table
                geophysicGeoradarTableContainer.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});


let geophysicGeoradarId = null;

// Open the modal for creating or editing a GeophysicGeoradar record
function openGeophysicGeoradarModal(editMode = false, geophyGeoradarId = null) {
    const modalTitle = document.getElementById('GeophysicGeoradarModalTitle');
    const submitButton = document.getElementById('submitGeophysicGeoradarBtn');
    const form = document.getElementById('GeophysicGeoradarForm');
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    
    isEditMode = editMode;
    currentGeophysicalId = geophysicalId;
    geophysicGeoradarId = geophyGeoradarId;

    if (editMode) {
        modalTitle.textContent = "გეორადარის განახლება";
        submitButton.textContent = "განახლება";
        fetchGeophysicGeoradarData(currentGeophysicalId, geophysicGeoradarId);
    } else {
        modalTitle.textContent = "გეორადარის დამატება";
        submitButton.textContent = "დამატება";
        form.reset();
    }

    const modal = new bootstrap.Modal(document.getElementById('GeophysicGeoradarModal'));
    modal.show();
}


// Fetch data for editing a geophysicGeoradar record
function fetchGeophysicGeoradarData(geophysicalId, geophysicGeoradarId) {
    fetch(`/api/geophysic_georadar/${geophysicalId}/${geophysicGeoradarId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('geophysicGeoradarId').value = data.id;
                document.getElementById('georadar_longitude').value = data.longitude;
                document.getElementById('georadar_latitude').value = data.latitude;
                document.getElementById('georadar_profile_length').value = data.profile_length;

            } else {
                alert('გეორადარის ჩანაწერი არ მოიძებნა.');
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

function submitGeophysicGeoradarForm(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('GeophysicGeoradarForm'));
    const url = isEditMode ? `/api/geophysic_georadar/${currentGeophysicalId}/${geophysicGeoradarId}` : `/api/geophysic_georadar/${currentGeophysicalId}`;
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
        alert('Error: გეორადარის დამატება რედაქტირებისას.');
    });
}

document.getElementById('GeophysicGeoradarForm').onsubmit = submitGeophysicGeoradarForm;

function deleteGeophysicGeoradar(id) {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");

    if (confirm('ნამდვილად გსურთ გეორადარის ჩანაწერის წაშლა?')) {
        // Retrieve the JWT token from sessionStorage (or wherever you store it)
        const token = sessionStorage.getItem('access_token');
        
        // makeApiRequest is in the globalAccessControl.js
        makeApiRequest(`/api/geophysic_georadar/${geophysicalId}/${id}`, {
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
                const row = document.querySelector(`tr[data-geophysicGeoradar-id="${id}"]`);
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