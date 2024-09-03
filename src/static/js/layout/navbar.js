document.addEventListener("DOMContentLoaded", function() {
    const navLinksStart = document.getElementById('navLinksStart');
    const navLinksEnd = document.getElementById('navLinksEnd');
    
    // Define static navigation items
    const navItems = [
        { endpoint: '/projects', text: 'მთავარი' },
        // Add other static links as needed
    ];

    // Define the login and registration links
    const authLinks = [
        { endpoint: '/login', text: 'შესვლა' },
        { endpoint: '/registration', text: 'რეგისტრაცია' }
    ];

    // Get the current path
    const currentPath = window.location.pathname;

    // Add static navigation items to the start of the navbar
    navItems.forEach(item => {
        const link = document.createElement('a');
        link.href = item.endpoint;
        link.className = currentPath === item.endpoint ? 'btn btn-sm btn-info m-1' : 'btn btn-sm btn-primary m-1';
        link.textContent = item.text;

        const listItem = document.createElement('li');
        listItem.className = 'nav-item';
        listItem.appendChild(link);

        navLinksStart.appendChild(listItem);
    });

    // Check for access_token in sessionStorage and update the navigation
    if (sessionStorage.getItem('access_token')) {
        // User is logged in, show Logout button
        const logoutItem = document.createElement('li');
        logoutItem.className = 'nav-item d-flex align-items-center';

        // Retrieve the user's email from sessionStorage
        const userEmail = sessionStorage.getItem('user_email');
        if (userEmail) {
            const emailSpan = document.createElement('span');
            emailSpan.className = 'me-2'; // Margin end for spacing
            emailSpan.textContent = userEmail;
            emailSpan.style.fontSize = 'small';

            logoutItem.appendChild(emailSpan); // Append email first
        }

        const logoutLink = document.createElement('a');
        logoutLink.href = '/login';
        logoutLink.className = 'btn btn-sm btn-danger m-1';
        logoutLink.textContent = 'გასვლა';
        logoutLink.onclick = function() {
            sessionStorage.removeItem('access_token');
            sessionStorage.removeItem('refresh_token');
            sessionStorage.removeItem('user_email');
            window.location.reload(); // Refresh to show the updated nav
        };

        logoutItem.appendChild(logoutLink);
        navLinksEnd.appendChild(logoutItem);
    } else {
        // User is not logged in, show Login and Registration buttons
        authLinks.forEach(link => {
            const authItem = document.createElement('li');
            authItem.className = 'nav-item';

            const authLink = document.createElement('a');
            authLink.href = link.endpoint;
            authLink.className = currentPath === link.endpoint ? 'btn btn-sm btn-info m-1' : 'btn btn-sm btn-primary m-1';
            authLink.textContent = link.text;

            authItem.appendChild(authLink);
            navLinksEnd.appendChild(authItem);
        });
    }
});