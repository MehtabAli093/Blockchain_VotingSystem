// Client-side form validation
document.addEventListener('DOMContentLoaded', function() {
    // Login form validation
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            const role = document.getElementById('role').value;
            
            if (!username || !password || !role) {
                e.preventDefault();
                alert('Please fill in all fields');
            }
        });
    }
    
    // Registration form validation
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            const fullName = document.getElementById('full_name').value.trim();
            const role = document.getElementById('role').value;
            const party = document.getElementById('party') ? document.getElementById('party').value.trim() : '';
            
            if (!username || !password || !fullName || !role) {
                e.preventDefault();
                alert('Please fill in all required fields');
                return;
            }
            
            if (role === 'candidate' && !party) {
                e.preventDefault();
                alert('Please enter your political party');
            }
        });
    }
    
    // Flash message auto-dismiss
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        });
    }, 5000);
});