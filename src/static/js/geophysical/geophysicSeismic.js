document.addEventListener("DOMContentLoaded", function() {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    // Fetch data from API endpoint geophysic_seismic
    fetch(`/api/geophysic_seismic/${geophysicalId}`)
        .then(response => response.json())
        .then(data => {

            const geologicalTableBody = document.getElementById('GeophysSeismicTable');
            data.forEach(data => {
                const row = `
                    <tr>
                        <td>${data.longitude}</td>
                        <td>${data.latitude}</td>
                        <td>${data.profile_length}</td>
                        <td>${data.vs30}</td>
                        <td>${data.ground_category_geo}</td>
                        <td>${data.ground_category_euro}</td>
                        <td>${data.archival_img}</td>
                        <td>${data.archival_excel}</td>
                        <td>${data.archival_pdf}</td>
                        <td>
                            <a class="btn btn-info" href="#">Edit</a>
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