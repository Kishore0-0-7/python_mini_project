// Common JavaScript functions for the Password Generator app

// Display a toast notification
function showToast(message, type = 'success') {
    // You could implement a toast notification system here
    // For simplicity, we're using alert for now
    alert(message);
}

// Format a date string
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Check password strength
function checkPasswordStrength(password) {
    let strength = 0;
    
    // Length check
    if (password.length >= 8) strength += 1;
    if (password.length >= 12) strength += 1;
    
    // Character type checks
    if (/[a-z]/.test(password)) strength += 1;  // lowercase
    if (/[A-Z]/.test(password)) strength += 1;  // uppercase
    if (/[0-9]/.test(password)) strength += 1;  // numbers
    if (/[^a-zA-Z0-9]/.test(password)) strength += 1;  // special chars
    
    // Return strength rating (0-6)
    return strength;
}

// Strength label
function getStrengthLabel(strength) {
    if (strength <= 2) return 'Weak';
    if (strength <= 4) return 'Moderate';
    return 'Strong';
}

// Initialize tooltips if Bootstrap is available
document.addEventListener('DOMContentLoaded', function() {
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}); 