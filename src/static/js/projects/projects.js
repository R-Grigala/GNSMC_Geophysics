document.addEventListener("DOMContentLoaded", function() {
    // Fetch data from API endpoint
    fetch('/api/projects')
        .then(response => response.json())
        .then(data => {
            const projectTableBody = document.getElementById('projectTableBody');
            data.forEach(project => {
                const row = `
                    <tr>
                        <td>${project.projects_name}</td>
                        <td>${project.contract_number}</td>
                        <td>${project.start_time}</td>
                        <td>${project.end_time}</td>
                        <td>${project.contractor}</td>
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
                            <a class="btn btn-sm btn-info" data-project-id="${project.id}" onclick="openEditProjectModal(${project.id})">Edit</a>
                        </td>
                        <td>
                            <a type="button" class="btn btn-sm btn-danger" data-project-id="${project.id}" onclick="confirmDelete(this)">Delete</a>
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

// Send POST request for create new project
function createProjectForm() {
    // Prevent form submission
    const form = document.getElementById('addProjectForm');
    const formData = new FormData(form);
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    fetch('/api/projects', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); // Show success message
            form.reset();
            $('#createProjectModal').modal('hide');
        } else {
            alert('Error occurred while adding the project.');
        }
    })
    .catch(error => console.error('Error:', error));
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

            var editProjectModal = new bootstrap.Modal(document.getElementById('editProjectModal'));
            editProjectModal.show();
        })
        .catch(error => console.error('Error fetching project data:', error));
}

// Send PUT request for edit project
function editProjectForm() {
    const form = document.getElementById('editProjectForm');
    const formData = new FormData(form);
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    fetch(`/api/project/${jsonData.project_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); // Show success message
            form.reset();
            $('#editProjectModal').modal('hide');
        } else {
            alert('Error occurred while editing the project.');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to confirm and delete a project
function confirmDelete(button) {
    const projectId = button.getAttribute('data-project-id');
    const confirmed = confirm('Are you sure you want to delete this project?');

    if (confirmed) {
        fetch(`/api/project/${projectId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message); // Show success message
                button.closest('tr').remove();
            } else {
                alert('Failed to delete project');
            }
        })
        .catch(error => {
            console.error('Error deleting project:', error);
            alert('An error occurred while deleting the project');
        });
    }
}


function showAlert(message, type = 'success') {
    // Get the alert placeholder element
    const alertPlaceholder = document.getElementById('alertPlaceholder');
    
    // Create a new alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Append the alert element to the placeholder
    alertPlaceholder.appendChild(alertDiv);
    
    // Automatically remove the alert after a few seconds
    setTimeout(() => {
        alertDiv.classList.remove('show');
        alertDiv.classList.add('fade');
        setTimeout(() => alertDiv.remove(), 150);
    }, 5000); // 5 seconds
}
