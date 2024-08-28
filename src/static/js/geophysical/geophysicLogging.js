document.addEventListener("DOMContentLoaded", function() {
    const geophysicalIdElement = document.getElementById("geophysicalId");
    const geophysicalId = geophysicalIdElement.getAttribute("data-geophysical-id");
    const geophysicLoggingTableContainer = document.getElementById('geophysicLoggingTableContainer');

    // Fetch data from API endpoint geophysic_logging
    fetch(`/api/geophysic_logging/${geophysicalId}`)
        .then(response => response.json())
        .then(data => {

            // Check if data is an array
            if (Array.isArray(data)) {
                const geophysicLoggingTable = document.getElementById('geophysicLoggingTable');
                data.forEach(data => {
                    const row = `
                        <tr>
                            <td>${data.longitude}</td>
                            <td>${data.latitude}</td>
                            <td>${data.profile_length}</td>
                            <td>${data.archival_img}</td>
                            <td>${data.archival_excel}</td>
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
                    geophysicLoggingTable.innerHTML += row;
                });
            }else{
                // If data is not an array, hide the table
                geophysicLoggingTableContainer.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});