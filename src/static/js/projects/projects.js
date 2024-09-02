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
    fetch('/api/projects', {
        method: 'POST',
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
        fetch(`/api/project/${projectId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message); // Show success message

                // Remove the row from the table
                const row = document.querySelector(`tr[data-project-id="${projectId}"]`);
                if (row) {
                    row.remove();
                }
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
