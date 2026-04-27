// Main JS for shared logic
console.log("Mindwell App Loaded");

// Common UI interactions if needed
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('mouseleave', e => {
        button.blur();
    });
});

// Theme Toggle Logic
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const icon = document.getElementById('themeIcon');

    if (current === 'light') {
        html.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        if (icon) icon.className = 'fas fa-moon';
    } else {
        html.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        if (icon) icon.className = 'fas fa-sun';
    }
}

// Load saved theme
(function () {
    const saved = localStorage.getItem('theme');
    if (saved) {
        document.documentElement.setAttribute('data-theme', saved);
        const icon = document.getElementById('themeIcon');
        if (icon) {
            icon.className = saved === 'light' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }
})();

// Active Link Highlight
document.addEventListener('DOMContentLoaded', () => {
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
            link.style.color = "var(--text-white)";
        }
    });
});
