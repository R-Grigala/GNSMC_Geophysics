document.addEventListener("DOMContentLoaded", function() {
    const projectIdElement = document.getElementById("projectId");
    const projectId = projectIdElement.getAttribute("data-project-id");
    // Fetch data from API endpoint
    fetch(`/api/geological/${projectId}`)
        .then(response => response.json())
        .then(data => {

            const geologicalTableBody = document.getElementById('geologicalTableBody');
            data.forEach(geological => {
                const row = `
                    <tr>
                        <td>${geological.geological_survey ? "Yes" : "No"}</td>
                        <td>${geological.objects_number}</td>
                        <td>${geological.boreholes ? "Yes" : "No"}</td>
                        <td>${geological.boreholes_number}</td>
                        <td>${geological.pits ? "Yes" : "No"}</td>
                        <td>${geological.pits_number}</td>
                        <td>${geological.laboratory_tests ? "Yes" : "No"}</td>
                        <td>${geological.points_number}</td>
                        <td>${geological.archival_material}</td>
                        <td>
                            <a class="btn btn-info" href="/edit_project/${geological.id}">Edit</a>
                        </td>
                        <td>
                            <form action="#" method="POST" style="display:inline;">
                                <button type="submit" class="btn btn-danger btn-block" onclick="return confirm('Are you sure you want to delete this station?');">Delete</button>
                            </form>
                        </td>
                    </tr>
                `;
                geologicalTableBody.innerHTML += row;
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});