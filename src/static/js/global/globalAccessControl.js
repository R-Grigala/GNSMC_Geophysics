function clearSessionData(redirect = true) {
    // Remove all session-related data
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('refresh_token');
    sessionStorage.removeItem('user_email');
    
    // Optionally redirect the user to the login page or another page
    if (redirect) {
        window.location.href = '/login'; // Redirect to the login page
    }
}

function isTokenExpired(token) {
    if (!token) return true;

    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Date.now() / 1000; // Current time in seconds

    return currentTime > payload.exp;
}

// Define the refreshToken function globally
function refreshToken() {
    const refreshToken = sessionStorage.getItem('refresh_token');

    if (!refreshToken) {
        clearSessionData(); // Clear session data and redirect to login
        return Promise.reject('No refresh token available');
    }

    return fetch('/api/refresh', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${refreshToken}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 401) {
            alert("გთხოვთ ხელახლა გაიაროთ ავტორიზაცია.");
            clearSessionData(); // Clear session data and redirect to login
            return Promise.reject('Unauthorized');
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
        clearSessionData(); // Clear session data and redirect to login
    });
}

function makeApiRequest(url, options) {
    const token = sessionStorage.getItem('access_token');
    
    // Check if the token is expired
    if (isTokenExpired(token)) {
        return refreshToken().then(newToken => {
            options.headers = options.headers || {};
            options.headers['Authorization'] = `Bearer ${newToken}`;
            return fetch(url, options);
        });
    }

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
                // Unprocessable Entity - likely related to the request data
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

function showAlert(category, message) {
    const alertPlaceholder = document.getElementById('alertPlaceholder');
    
    // Create a new alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${category} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add the alert to the placeholder
    alertPlaceholder.appendChild(alertDiv);
    
    // Optional: Auto-close the alert after a timeout
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000); // 5000 milliseconds = 5 seconds
}

function closeModal(modalName) {
    const modalElement = document.getElementById(modalName);
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    if (modalInstance) {
        modalInstance.hide();
    }
    
    // Manually remove backdrop
    const backdrop = document.querySelector('.modal-backdrop');
    if (backdrop) {
        backdrop.remove();
    }
}

// The DOMContentLoaded event listener
document.addEventListener("DOMContentLoaded", function() {
    const loginPage = '/login';
    const registrationPage = '/registration';
    const homePage = '/';
    const currentPage = window.location.pathname;
    const token = sessionStorage.getItem('access_token');

    if (!token && currentPage !== loginPage && currentPage !== registrationPage) {
        window.location.href = loginPage;
    }

    // Check if the token is expired and redirect to login if necessary
    if (token && isTokenExpired(token)) {
        refreshToken(); // Clear session data and redirect to login
    }

    // Redirect to home page if token exists and user is on the login or registration page
    if (token && (currentPage === loginPage || currentPage === registrationPage)) {
        window.location.href = homePage;
    }
});