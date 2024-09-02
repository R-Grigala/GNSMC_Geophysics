// Define the refreshToken function globally
function refreshToken() {
    const refreshToken = sessionStorage.getItem('refresh_token');

    return fetch('/api/refresh', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${refreshToken}`, // Send the refresh token
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to refresh token');
        }
        return response.json();
    })
    .then(data => {
        if (data.access_token) {
            sessionStorage.setItem('access_token', data.access_token); // Save new access token
            return data.access_token;
        } else {
            throw new Error('Failed to refresh token');
        }
    })
    .catch(error => {
        console.error('Error refreshing token:', error);
        // Optionally, handle logout or token renewal failure
    });
}

function makeApiRequest(url, options) {
    return fetch(url, options)
        .then(response => {
            if (response.status === 401) {
                // Unauthorized - token might be expired
                return refreshToken()
                    .then(newToken => {
                        // Retry the original request with new token
                        options.headers['Authorization'] = `Bearer ${newToken}`;
                        return fetch(url, options);
                    });
            }
            return response;
        })
        .then(response => response.json());
}

// The DOMContentLoaded event listener
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