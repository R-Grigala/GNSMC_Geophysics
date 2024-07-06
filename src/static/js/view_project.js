document.addEventListener("DOMContentLoaded", function() {
    // Fetch data from API endpoint
    fetch('/api/project/1')
        .then(response => response.json())
        .then(data => {
            console.log(data)
            const projectTableBody = document.getElementById('view_projectTableBody');
            const row = `
                <tr>
                    <td>${data.projects_name}</td>
                    <td>${data.contract_number}</td>
                    <td>${data.start_time}</td>
                    <td>${data.end_time}</td>
                    <td>${data.contractor}</td>
                    <td>${data.proj_location}</td>
                    <td>${data.proj_latitude}</td>
                    <td>${data.proj_longitude}</td>
                    <td>${data.geological_study ? "Yes" : "No"}</td>
                    <td>${data.geophysical_study ? "Yes" : "No"}</td>
                    <td>${data.hazard_study ? "Yes" : "No"}</td>
                    <td>${data.geodetic_study ? "Yes" : "No"}</td>
                    <td>${data.other_study ? "Yes" : "No"}</td>
                    <td>
                        <a class="btn btn-info" href="/edit_project/${data.id}">Edit</a>
                    </td>
                    <td>
                        <form action="#" method="POST" style="display:inline;">
                            <button type="submit" class="btn btn-danger btn-block" onclick="return confirm('Are you sure you want to delete this station?');">Delete</button>
                        </form>
                    </td>
                </tr>
            `;
            projectTableBody.innerHTML += row;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});