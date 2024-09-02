// Define the refreshToken function globally
function refreshToken() {
    const refreshToken = sessionStorage.getItem('refresh_token');

    if (!refreshToken) {
        window.location.href = '/login';
    }

    return fetch('/api/refresh', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${refreshToken}`, // Send the refresh token
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 401) {
            // Unauthorized, token may be invalid or expired
            throw new Error('Refresh token is invalid or expired');
        }
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
        // Clear refresh token and redirect to login page if refresh fails
        sessionStorage.removeItem('refresh_token');
        window.location.href = '/login'; // Redirect to login page
    });
}

function makeApiRequest(url, options) {
    const token = sessionStorage.getItem('access_token');
    
    // Ensure the Authorization header is set
    if (token) {
        options.headers = options.headers || {};
        options.headers['Authorization'] = `Bearer ${token}`;
    }

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
            if (response.status === 422) {
                // Unauthorized - token might be expired
                sessionStorage.removeItem('access_token');
                window.location.href = '/login';
            }
            else {
                return response;
            }
            
        })
        .then(response => response.json())
        .catch(error => {
            console.error('API Request Error:', error);
            // Handle errors appropriately
        });
}

// The DOMContentLoaded event listener
document.addEventListener("DOMContentLoaded", function() {
    // Define the login and registration page URLs
    const loginPage = '/login'; // Adjust this to your actual login page URL
    const registrationPage = '/registration'; // Adjust this to your actual registration page URL
    const homePage = '/projects'; 

    // Get the current page URL
    const currentPage = window.location.pathname;

    // Check for the presence of an access token
    const token = sessionStorage.getItem('access_token');

    // If there's no token and the user is not on the login or registration page, attempt to refresh the token
    if (!token && currentPage !== loginPage && currentPage !== registrationPage) {
        // If no new token is obtained, redirect to the login page
        window.location.href = loginPage;
    }
    if (token && (currentPage === loginPage || currentPage === registrationPage)) {
        window.location.href = homePage;
    }
});
