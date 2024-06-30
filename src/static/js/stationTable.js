document.addEventListener("DOMContentLoaded", function() {
    // Fetch data from API endpoint
    fetch('/api/view_stations')
        .then(response => response.json())
        .then(data => {
            // Populate table with data
            const stationTableBody = document.getElementById('stationTableBody');
            data.forEach(station => {
                const row = `
                    <tr>
                        <td>${station.tStStatuse}</td>
                        <td>${station.tStCode}</td>
                        <td>${station.tStNetworkCode}</td>
                        <td>${station.tStLocation}</td>
                        <td>${station.tStLatitude}</td>
                        <td>${station.tStLongitude}</td>
                        <td>${station.tStElevation}</td>
                        <td>${station.tStOpenDate}</td>
                        <td>${station.tStCloseDate}</td>
                        <td>${station.tStType}</td>
                        <td>${station.tStShow}</td>
                        <td>${station.tStLastEditor}</td>
                        <td>${station.tStLastEditTime}</td>
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
                stationTableBody.innerHTML += row;
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle error scenario, e.g., show an error message on the UI
        });
});