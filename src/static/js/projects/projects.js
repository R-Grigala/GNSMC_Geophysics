document.addEventListener("DOMContentLoaded", function() {
    // Fetch data from API endpoint
    fetch('/api/projects')
        .then(response => response.json())
        .then(data => {
            const projectTableBody = document.getElementById('projectTableBody');
            data.forEach(project => {
                const row = `
                    <tr data-project-id="${project.id}">
                        <td>${project.projects_name}</td>
                        <td>${project.contract_number || '----'}</td>
                        <td>${project.start_time}</td>
                        <td>${project.end_time}</td>
                        <td>${project.contractor || '----'}</td>
                        <td>${project.proj_location}</td>
                        <td>${project.proj_latitude}</td>
                        <td>${project.proj_longitude}</td>
                        <td>${project.geological_study ? "Yes" : "No"}</td>
                        <td>${project.geophysical_study ? "Yes" : "No"}</td>
                        <td>${project.hazard_study ? "Yes" : "No"}</td>
                        <td>${project.geodetic_study ? "Yes" : "No"}</td>
                        <td>${project.other_study ? "Yes" : "No"}</td>
                        <td>
                            <a class="btn btn-sm btn-primary" href="/view_project/${project.id}">View</a>
                        </td>
                        <td>
                            <a class="btn btn-sm btn-info" onclick="openEditProjectModal(${project.id})">Edit</a>
                        </td>
                        <td>
                            <img src="/static/img/trash_icon.png" alt="Delete" class="delete-icon" onclick="confirmDelete(${project.id})" style="width: 30px; height: 30px; cursor: pointer;">
                        </td>
                    </tr>
                `;
                projectTableBody.innerHTML += row;
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});

// Send POST request for creating a new project
function createProjectForm(event) {
    event.preventDefault(); // Prevent form submission

    const form = document.getElementById('addProjectForm');
    const formData = new FormData(form);

    // Proceed with the form submission regardless of the file type
    submitForm(formData);
}

function submitForm(formData) {
    // Retrieve the JWT token from sessionStorage (or wherever you store it)
    const token = sessionStorage.getItem('access_token');

    fetch('/api/projects', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); // Show success message
            window.location.reload();
        } else {
            alert('Error occurred while creating the project.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    });
}

// Open edit Project Modal
function openEditProjectModal(projectId) {
    fetch(`/api/project/${projectId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('editProjectId').value = data.id;
            document.getElementById('editProjectName').value = data.projects_name;
            document.getElementById('editContractNumber').value = data.contract_number;
            document.getElementById('editStartTime').value = data.start_time;
            document.getElementById('editEndTime').value = data.end_time;
            document.getElementById('editContractor').value = data.contractor;
            document.getElementById('editProjLocation').value = data.proj_location;
            document.getElementById('editProjLatitude').value = data.proj_latitude;
            document.getElementById('editProjLongitude').value = data.proj_longitude;

            // Set the data-project-id attribute for later use
            document.getElementById('editProjectForm').setAttribute('data-project-id', data.id);

            var editProjectModal = new bootstrap.Modal(document.getElementById('editProjectModal'));
            editProjectModal.show();
        })
        .catch(error => console.error('Error fetching project data:', error));
}

// Send PUT request for edit project
function editProjectForm(event) {
    event.preventDefault(); // Prevent form submission

    const formData = new FormData(document.getElementById('editProjectForm'));
    const projectId = document.getElementById("editProjectForm").getAttribute("data-project-id");

    // Retrieve the JWT token from sessionStorage (or wherever you store it)
    const token = sessionStorage.getItem('access_token');

    fetch(`/api/project/${projectId}`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); // Show success message
            form.reset();
        } else {
            alert('Error occurred while editing the project.');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to confirm and delete a project
function confirmDelete(projectId) {
    const confirmed = confirm('დარწმუნებული ხართ რომ გსურთ ამ პროექტის წაშლა?');

    if (confirmed) {

        // Retrieve the JWT token from sessionStorage (or wherever you store it)
        const token = sessionStorage.getItem('access_token');
        
        fetch(`/api/project/${projectId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}` // Include the JWT token in the Authorization header
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                // Optionally, remove the row from the table
                const row = document.querySelector(`tr[data-project-id="${projectId}"]`);
                if (row) {
                    row.remove();
                }
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error deleting project:', error);
            alert('An error occurred while deleting the project');
        });
    }
}
