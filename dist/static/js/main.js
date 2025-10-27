// Academic Website JavaScript

// Theme Management with improved cross-browser support
let currentTheme = 'dark'; // Default theme

function initializeTheme() {
    // Check for saved theme preference with fallback
    try {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
            currentTheme = savedTheme;
        } else {
            // Default to dark theme
            currentTheme = 'dark';
            localStorage.setItem('theme', currentTheme);
        }
    } catch (e) {
        // LocalStorage might not be available, use default
        currentTheme = 'dark';
    }
    
    applyTheme(currentTheme);
    updateThemeIcon(currentTheme);
}

function toggleTheme() {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    try {
        localStorage.setItem('theme', currentTheme);
    } catch (e) {
        // LocalStorage might not be available, continue anyway
        console.log('Could not save theme preference');
    }
    
    applyTheme(currentTheme);
    updateThemeIcon(currentTheme);
}

function applyTheme(theme) {
    const html = document.documentElement;
    const body = document.body;
    
    // Remove any existing theme classes
    html.classList.remove('light-theme', 'dark-theme');
    body.classList.remove('light-theme', 'dark-theme');
    
    // Remove data attribute
    html.removeAttribute('data-theme');
    
    // Apply new theme
    if (theme === 'light') {
        html.classList.add('light-theme');
        body.classList.add('light-theme');
        html.setAttribute('data-theme', 'light');
    } else {
        html.classList.add('dark-theme');
        body.classList.add('dark-theme'); 
        html.setAttribute('data-theme', 'dark');
    }
}

function updateThemeIcon(theme) {
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        if (theme === 'light') {
            themeIcon.className = 'fas fa-moon';
        } else {
            themeIcon.className = 'fas fa-sun';
        }
    }
}

// Initialize theme on page load
initializeTheme();

document.addEventListener('DOMContentLoaded', function() {
    // Ensure theme is properly set
    initializeTheme();
    
    // Mobile navigation improvements
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Close mobile menu when clicking on nav links
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                    toggle: false
                });
                bsCollapse.hide();
            }
        });
    });
    
    // Improve mobile dropdown behavior
    const dropdownElements = document.querySelectorAll('.dropdown-toggle');
    dropdownElements.forEach(dropdown => {
        dropdown.addEventListener('click', function(e) {
            // On mobile, ensure dropdown works properly
            if (window.innerWidth <= 768) {
                e.stopPropagation();
            }
        });
    });
    
    // Handle window resize for responsive behavior
    window.addEventListener('resize', function() {
        const navbarCollapse = document.querySelector('.navbar-collapse');
        if (window.innerWidth > 768 && navbarCollapse && navbarCollapse.classList.contains('show')) {
            const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                toggle: false
            });
            bsCollapse.hide();
        }
    });
    
    // Theme toggle button - ensure it works on mobile and all browsers
    const themeToggleBtn = document.querySelector('.theme-toggle');
    if (themeToggleBtn) {
        // Remove any existing event listeners
        themeToggleBtn.onclick = null;
        
        // Add multiple event types for better compatibility
        themeToggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleTheme();
        });
        
        // Add touch support for mobile
        themeToggleBtn.addEventListener('touchend', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleTheme();
        });
        
        // Add keyboard support
        themeToggleBtn.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleTheme();
            }
        });
    }
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in-up');
        }, index * 100);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Language switcher functionality
    const langButtons = document.querySelectorAll('.dropdown-item[href*="/"]');
    langButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Store language preference
            const newLang = this.getAttribute('href').split('/')[1];
            localStorage.setItem('preferredLanguage', newLang);
        });
    });

    // Do not auto-redirect from root based on previously stored language.
    // The site default should be English; users can still switch languages manually.

    // Add loading states to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.getAttribute('href') && !this.getAttribute('href').startsWith('#')) {
                this.classList.add('disabled');
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>' + this.innerText;
            }
        });
    });

    // Navbar scroll effect - disabled on mobile for better performance
    if (window.innerWidth > 768) {
        let lastScrollTop = 0;
        const navbar = document.querySelector('.navbar');
        
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                // Scrolling down
                navbar.style.transform = 'translateY(-100%)';
            } else {
                // Scrolling up
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScrollTop = scrollTop;
        });

        // Add transition to navbar
        navbar.style.transition = 'transform 0.3s ease-in-out';
    }
});

// Utility functions
function showToast(message, type = 'info') {
    // Simple toast notification system
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

// Copy to clipboard function for code blocks
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Code copied to clipboard!', 'success');
    }, function(err) {
        showToast('Failed to copy code', 'danger');
    });
}

// Email obfuscation
function revealEmail(element) {
    const email = element.getAttribute('data-email');
    if (email) {
        element.href = 'mailto:' + email;
        element.textContent = email;
    }
}