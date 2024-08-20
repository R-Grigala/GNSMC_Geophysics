document.addEventListener("DOMContentLoaded", function() {
    // Fetch data from API endpoint
    fetch('/api/projects')
        .then(response => response.json())
        .then(data => {

            const projectTableBody = document.getElementById('projectTableBody');
            data.forEach(project => {
                const row = `
                    <tr data-href="/view_project/${project.id}">
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
                            <a class="btn btn-info" href="/edit_project/${project.id}">Edit</a>
                        </td>
                        <td>
                            <form action="#" method="POST" style="display:inline;">
                                <button type="submit" class="btn btn-danger btn-block" onclick="return confirm('Are you sure you want to delete this project?');">Delete</button>
                            </form>
                        </td>
                    </tr>
                `;
                projectTableBody.innerHTML += row;
            });
            
            // Add click event listener to each <tr> to navigate to detailed view
            const tableRows = projectTableBody.getElementsByTagName('tr');
            Array.from(tableRows).forEach(row => {
                row.style.cursor = 'pointer';
                row.addEventListener('click', function() {
                    const href = row.getAttribute('data-href');
                    if (href) {
                        window.location.href = href;
                    }
                });
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});