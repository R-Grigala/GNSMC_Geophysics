document.addEventListener("DOMContentLoaded", function() {
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");
    const geophysicalTableContainer = document.getElementById('geophysicalTableContainer');

    fetch(`/api/geophysical/${projectId}`)
    .then(response => response.json())
    .then(data => {
        // Check if data is an array
        if (Array.isArray(data)) {
            const geophysicalTableBody = document.getElementById('geophysicalTableBody');

            data.forEach(geophysical => {
                const archivalMaterialLink = geophysical.archival_material ? 
                `<a href="/geophysical/archival_material/${projectId}/${geophysical.archival_material}" target="_blank">${geophysical.archival_material}</a>` : 
                '---';

                const row = `
                    <tr data-geophysical-id="${geophysical.id}">
                        <td>${geophysical.seismic_profiles ? "Yes" : "No"}</td>
                        <td>${geophysical.profiles_number}</td>
                        <td>${geophysical.vs30}</td>
                        <td>${geophysical.ground_category_geo}</td>
                        <td>${geophysical.ground_category_euro}</td>
                        <td>${geophysical.geophysical_logging ? "Yes" : "No"}</td>
                        <td>${geophysical.logging_number}</td>
                        <td>${geophysical.electrical_profiles ? "Yes" : "No"}</td>
                        <td>${geophysical.point_number}</td>
                        <td>${geophysical.georadar ? "Yes" : "No"}</td>
                        <td>${archivalMaterialLink}</td>
                        <td>
                            <a class="btn btn-sm btn-primary" href="/view_geophysical/${geophysical.id}">View</a>
                        </td>
                        <td>
                            <a class="btn btn-sm btn-info" onclick="openGeophysicalModal(true, ${geophysical.id})">Edit</a>
                        </td>
                        <td>
                            <img src="/static/img/x_button.png" alt="Delete" class="delete-icon" onclick="deleteGeophysical(${geophysical.id}, ${projectId})" style="width: 25px; height: 25px; cursor: pointer;">
                        </td>
                    </tr>
                `;
                geophysicalTableBody.innerHTML += row;
            });
        } else {
            // If data is not an array, hide the table
            geophysicalTableContainer.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        // Handle error scenario, e.g., show an error message on the UI
    });

});


let isEditMode = false;
let currentProjectId = null;
let geophysicalId = null;

// Open the modal for creating or editing a Geophysical record
function openGeophysicalModal(editMode = false, geophyId = null) {
    const modalTitle = document.getElementById('GeophysicalModalTitle');
    const submitButton = document.getElementById('submitGeophysicalBtn');
    const form = document.getElementById('GeophysicalForm');
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");
    
    isEditMode = editMode;
    currentProjectId = projectId;
    geophysicalId = geophyId;

    if (editMode) {
        modalTitle.textContent = "სეისმური პროფილის განახლება";
        submitButton.textContent = "განახლება";
        fetchGeophysicalData(currentProjectId, geophysicalId);
    } else {
        modalTitle.textContent = "სეისმური პროფილის დამატება";
        submitButton.textContent = "დამატება";
        form.reset();
    }

    const modal = new bootstrap.Modal(document.getElementById('GeophysicalModal'));
    modal.show();
}

// Fetch data for editing a Geophysical record
function fetchGeophysicalData(geophysicalId, projectId) {
    // Fetch the existing data for the geophysical record
    fetch(`/api/geophysical/${projectId}/${geophysicalId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                // Fill the form fields with existing data
                document.getElementById('geophysicalId').value = data.id;
                document.getElementById('vs30').value = data.vs30;
                document.getElementById('groundCategoryGeo').value = data.ground_category_geo;
                document.getElementById('groundCategoryEuro').value = data.ground_category_euro;

                console.log(document.getElementById('vs30').value, data.vs30)
    
            } else {
                alert('გეოფიზიკური კვლევა არ მოიძებნა.');
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function submitGeophysicalForm(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('GeophysicalForm'));
    const url = isEditMode ? `/api/geophysical/${currentProjectId}/${geophysicalId}` : `/api/geophysical/${currentProjectId}`;
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
        alert('Error: გეოფიზიკური კვლევის დამატება რედაქტირებისას.');
    });
}

document.getElementById('GeophysicalForm').onsubmit = submitGeophysicalForm;


function deleteGeophysical(id, projectId) {
    if (confirm('ნამდვილად გსურთ ამ გეოფიზიკის წაშლა?')) {
        fetch(`/api/geophysical/${projectId}/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                // Optionally, remove the row from the table
                const row = document.querySelector(`tr[data-geophysical-id="${id}"]`);
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
