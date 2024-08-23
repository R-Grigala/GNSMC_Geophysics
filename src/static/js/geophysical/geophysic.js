// Function to handle the form submission
function createGeophysicalForm(event) {

    event.preventDefault(); // Prevent the default form submission

    // Create a FormData object from the form
    const form = document.getElementById('addGeophysicalForm');
    const formData = new FormData(form);
    const projectId = document.getElementById('projectId').getAttribute('data-project-id');
    console.log(projectId)

    // Make a POST request to your Flask API
    fetch(`/api/geophysical/1`, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message); // Display success message or handle response
            $('#CreateGeophysicalModal').modal('hide'); // Hide the modal
            form.reset(); // Reset the form
        } else {
            alert('Error: ' + JSON.stringify(data)); // Handle errors
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while creating the geophysical record.');
    });
}
