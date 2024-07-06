document.addEventListener("DOMContentLoaded", function() {
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");
    // Fetch data from API endpoint
    fetch(`/api/geophysical/${projectId}`)
        .then(response => response.json())
        .then(data => {

            const geophysicalTableBody = document.getElementById('geophysicalTableBody');
            data.forEach(geophysical => {
            
                const row = `
                    <tr>
                        <td>${geophysical.seismic_profiles ? "Yes" : "No"}</td>
                        <td>${geophysical.profiles_number}</td>
                        <td>${geophysical.vs30}</td>
                        <td>${geophysical.vs30_section}</td>
                        <td>${geophysical.ground_category_geo}</td>
                        <td>${geophysical.ground_category_euro}</td>
                        <td>${geophysical.geophysical_logging ? "Yes" : "No"}</td>
                        <td>${geophysical.logging_number}</td>
                        <td>${geophysical.electrical_profiles ? "Yes" : "No"}</td>
                        <td>${geophysical.point_number}</td>
                        <td>${geophysical.georadar ? "Yes" : "No"}</td>
                        <td>${geophysical.archival_material}</td>
                        <td>
                            <a class="btn btn-info" href="/edit_project/${geophysical.id}">Edit</a>
                        </td>
                        <td>
                            <form action="#" method="POST" style="display:inline;">
                                <button type="submit" class="btn btn-danger btn-block" onclick="return confirm('Are you sure you want to delete this station?');">Delete</button>
                            </form>
                        </td>
                    </tr>
                `;
                geophysicalTableBody.innerHTML += row;
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});