document.addEventListener("DOMContentLoaded", function() {
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");
    const geophysicalTableContainer = document.getElementById('geophysicalTableContainer');

    fetch(`/api/geophysical/${projectId}`)
    .then(response => response.json())
    .then(data => {
        // Check if data is an array
        if (Array.isArray(data)) {
            data.forEach(geophysical => {
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
                        <td>${geophysical.archival_material || '----'}</td>
                        <td>
                            <a class="btn btn-sm btn-primary" href="/view_geophysical/${geophysical.id}">View</a>
                        </td>
                        <td>
                            <a class="btn btn-sm btn-info" onclick="openEditGeophysicalModal(${geophysical.id}, ${projectId})">Edit</a>
                        </td>
                        <td>
                            <a class="btn btn-sm btn-danger btn-block" 
                                    onclick="deleteGeophysicalRecord(${geophysical.id}, ${projectId})">Delete
                            </a>
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

function createGeophysicalForm(event) {

    event.preventDefault(); // Prevent the default form submission

    // Create a FormData object from the form
    const form = document.getElementById('addGeophysicalForm');
    const formData = new FormData(form);

    // Use the dynamic project ID
    const projectId = document.getElementById('projectId').getAttribute('data-project-id');

    // Make a POST request to your Flask API
    fetch(`/api/geophysical/${projectId}`, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); // Display success message or handle response
            form.reset(); // Reset the form
            window.location.reload();
        } else {
            alert('Error: ' + JSON.stringify(data)); // Handle errors
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while creating the geophysical record.');
    });
}

function deleteGeophysicalRecord(geophysicalId, projectId) {
    if (!confirm('დარწმუნებული ხართ რომ გსურთ ამ გეოფიზიკის წაშლა?')) return;

    // Send DELETE request to the API
    fetch(`/api/geophysical/${projectId}/${geophysicalId}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (response.ok) {
            // Remove the row from the table
            const row = document.querySelector(`tr[data-geophysical-id="${geophysicalId}"]`);
            if (row) {
                row.remove();
            }
            alert('წარმატებით წაიშალა გეოფიზიკის ჩანაწერი.');
        } else {
            // Handle error responses
            response.json().then(data => {
                alert('Error: ' + data.message);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the geophysical record.');
    });
}

// Function to open the edit modal with existing data
function openEditGeophysicalModal(geophysicalId, projectId) {
    // Fetch the existing data for the geophysical record
    fetch(`/api/geophysical/${projectId}/${geophysicalId}`)
    .then(response => response.json())
    .then(data => {
        if (data) {
            // Fill the form fields with existing data
            document.getElementById('editProjectId').value = projectId;
            document.getElementById('editGeophysicalId').value = data.id;
            document.getElementById('editVs30').value = data.vs30;
            document.getElementById('editGroundCategoryGeo').value = data.ground_category_geo;
            document.getElementById('editGroundCategoryEuro').value = data.ground_category_euro;

            // Handle the existing archival material file
            const archivalMaterialContainer = document.getElementById('existingArchivalMaterial');
            if (data.archival_material) {
                archivalMaterialContainer.innerHTML = `
                    <p>არსებული საარქივო ფაილი :&emsp;<a href="/geophysical/archival_material/${projectId}/${data.archival_material}" target="_blank">${data.archival_material}</a></p>
                `;
            } else {
                archivalMaterialContainer.innerHTML = `<p>არ არის ატვირთული საარქივო ფაილი.</p>`;
            }

            // Show the modal
            var editGeophysicalModal = new bootstrap.Modal(document.getElementById('editGeophysicalModal'));
            editGeophysicalModal.show();
        } else {
            alert('Geophysical record not found.');
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        alert('An error occurred while fetching geophysical data.');
    });
}

function editGeophysicalForm(event) {
    event.preventDefault(); // Prevent the default form submission

    // Create a FormData object from the form
    const form = document.getElementById('editGeophysicalForm');
    const formData = new FormData(form);

    // Get the geophysical ID
    const geophysicalId = document.getElementById('editGeophysicalId').value;
    const projectId = document.getElementById('editProjectId').value;

    // Make a PUT request to your Flask API
    fetch(`/api/geophysical/${projectId}/${geophysicalId}`, {
        method: 'PUT',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); // Display success message or handle response
            window.location.reload(); // Reload the page to reflect changes
        } else {
            alert('Error: ' + JSON.stringify(data)); // Handle errors
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the geophysical record.');
    });
}