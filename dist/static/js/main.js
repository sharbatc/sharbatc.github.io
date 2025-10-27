// Academic Website JavaScript

// Theme Management
function initializeTheme() {
    // Check for saved theme preference or default to 'dark'
    // User preference: default site theme should be dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
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
    
    // Theme toggle button - ensure it works on mobile
    const themeToggleBtn = document.querySelector('.theme-toggle');
    if (themeToggleBtn) {
        // Add touch-friendly behavior
        themeToggleBtn.addEventListener('touchstart', function(e) {
            e.preventDefault();
            toggleTheme();
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