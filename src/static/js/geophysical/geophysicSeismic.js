document.addEventListener("DOMContentLoaded", function() {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    const geophysicSeismicTableContainer = document.getElementById('geophysicSeismicTableContainer');
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");
    
    // Fetch data from API endpoint geophysic_seismic
    fetch(`/api/geophysic_seismic/${geophysicalId}`)
        .then(response => response.json())
        .then(data => {

            // Check if data is an array
            if (Array.isArray(data)) {
                const geophysicSeismicTable = document.getElementById('geophysicSeismicTable');

                data.forEach(data => {
                    const archivalImgLink = data.archival_img ? 
                        `<a href="/${projectId}/geophysical/${data.geophysical_id}/seismic/archival_img/${data.archival_img}" target="_blank">${data.archival_img}</a>` : 
                        '---';

                    const archivalExcelLink = data.archival_excel ? 
                        `<a href="/${projectId}/geophysical/${data.geophysical_id}/seismic/archival_excel/${data.archival_excel}" target="_blank">${data.archival_excel}</a>` : 
                        '---';

                    const archivalPdfLink = data.archival_pdf ? 
                        `<a href="/${projectId}/geophysical/${data.geophysical_id}/seismic/archival_pdf/${data.archival_pdf}" target="_blank">${data.archival_pdf}</a>` : 
                        '---';

                    const row = `
                        <tr data-geophysicSeismic-id="${data.id}">
                            <td>${data.longitude}</td>
                            <td>${data.latitude}</td>
                            <td>${data.profile_length}</td>
                            <td>${data.vs30}</td>
                            <td>${data.ground_category_geo}</td>
                            <td>${data.ground_category_euro}</td>
                            <td>${archivalImgLink}</td>
                            <td>${archivalExcelLink}</td>
                            <td>${archivalPdfLink}</td>
                            <td>
                                <img src="/static/img/pen-solid.svg" alt="Edit" style="width: 20px; height: 20px; cursor: pointer;" onclick="openGeophysicSeismicModal(true, ${data.id})">
                            </td>
                            <td>
                                <img src="/static/img/trash-solid.svg" alt="Delete" style="width: 20px; height: 20px; cursor: pointer;" onclick="deleteGeophysicSeismic(${data.id})">
                            </td>
                        </tr>
                    `;
                    geophysicSeismicTable.innerHTML += row;
                });
            } else {
                // If data is not an array, hide the table
                geophysicSeismicTableContainer.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});


let isEditMode = false;
let currentGeophysicalId = null;
let geophysicSeismicId = null;

// Open the modal for creating or editing a GeophysicSeismic record
function openGeophysicSeismicModal(editMode = false, geophySeismicId = null) {
    const modalTitle = document.getElementById('GeophysicSeismicModalTitle');
    const submitButton = document.getElementById('submitGeophysicSeismicBtn');
    const form = document.getElementById('GeophysicSeismicForm');
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    
    isEditMode = editMode;
    currentGeophysicalId = geophysicalId;
    geophysicSeismicId = geophySeismicId;

    if (editMode) {
        modalTitle.textContent = "სეისმური პროფილის განახლება";
        submitButton.textContent = "განახლება";
        fetchGeophysicSeismicData(currentGeophysicalId, geophysicSeismicId);
    } else {
        modalTitle.textContent = "სეისმური პროფილის დამატება";
        submitButton.textContent = "დამატება";
        form.reset();
    }

    const modal = new bootstrap.Modal(document.getElementById('GeophysicSeismicModal'));
    modal.show();
}

// Fetch data for editing a GeophysicSeismic record
function fetchGeophysicSeismicData(geophysicalId, geophysicSeismicId) {
    fetch(`/api/geophysic_seismic/${geophysicalId}/${geophysicSeismicId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('geophysicSeismicId').value = data.id;
                document.getElementById('seismic_longitude').value = data.longitude;
                document.getElementById('seismic_latitude').value = data.latitude;
                document.getElementById('seismic_profile_length').value = data.profile_length;
                document.getElementById('seismic_vs30').value = data.vs30;
                document.getElementById('seismic_ground_category_geo').value = data.ground_category_geo;
                document.getElementById('seismic_ground_category_euro').value = data.ground_category_euro;


                // console.log(data);
            } else {
                alert('სეისმური პროფილი არ მოიძებნა.');
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

function submitGeophysicSeismicForm(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('GeophysicSeismicForm'));
    const url = isEditMode ? `/api/geophysic_seismic/${currentGeophysicalId}/${geophysicSeismicId}` : `/api/geophysic_seismic/${currentGeophysicalId}`;
    const method = isEditMode ? 'PUT' : 'POST';

    const token = sessionStorage.getItem('access_token');

    // makeApiRequest is in the globalAccessControl.js
    makeApiRequest(url, {
        method: method,
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            window.location.reload(); // Reload the page to reflect changes
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error: სეისმური პროფილის დამატება რედაქტირებისას.');
    });
}

document.getElementById('GeophysicSeismicForm').onsubmit = submitGeophysicSeismicForm;


function deleteGeophysicSeismic(id) {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");

    if (confirm('ნამდვილად გსურთ სეისმური პროფილის წაშლა?')) {
        const token = sessionStorage.getItem('access_token');
        
        // makeApiRequest is in the globalAccessControl.js
        makeApiRequest(`/api/geophysic_seismic/${geophysicalId}/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(data => {
            if (data.message) {
                alert(data.message);
                const row = document.querySelector(`tr[data-geophysicSeismic-id="${id}"]`);
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