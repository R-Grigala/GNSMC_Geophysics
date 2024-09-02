document.addEventListener("DOMContentLoaded", function() {
    // Define the login and registration page URLs
    const loginPage = '/login'; // Adjust this to your actual login page URL
    const registrationPage = '/registration'; // Adjust this to your actual registration page URL

    // Get the current page URL
    const currentPage = window.location.pathname;

    // Check for the presence of an access token
    const token = sessionStorage.getItem('access_token');

    // If there's no token and the user is not on the login or registration page, redirect to the login page
    if (!token && currentPage !== loginPage && currentPage !== registrationPage) {
        window.location.href = loginPage;
    }
});
