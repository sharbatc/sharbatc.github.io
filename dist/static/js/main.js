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
        console.log('LocalStorage not available, using default theme');
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
    
    // Add visual feedback for mobile
    const themeButton = document.querySelector('.theme-toggle');
    if (themeButton) {
        themeButton.style.transform = 'scale(0.95)';
        setTimeout(() => {
            themeButton.style.transform = 'scale(1)';
        }, 150);
    }
    
    // Force a small delay to ensure changes are applied
    setTimeout(() => {
        console.log('Theme changed to:', currentTheme);
    }, 100);
}

function applyTheme(theme) {
    const html = document.documentElement;
    const body = document.body;
    
    // Remove any existing theme classes and attributes
    html.classList.remove('light-theme', 'dark-theme');
    body.classList.remove('light-theme', 'dark-theme');
    html.removeAttribute('data-theme');
    
    // Apply new theme with multiple methods for compatibility
    if (theme === 'light') {
        html.classList.add('light-theme');
        body.classList.add('light-theme');
        html.setAttribute('data-theme', 'light');
        html.style.setProperty('color-scheme', 'light');
    } else {
        html.classList.add('dark-theme');
        body.classList.add('dark-theme'); 
        html.setAttribute('data-theme', 'dark');
        html.style.setProperty('color-scheme', 'dark');
    }
    
    // Force repaint
    html.style.display = 'none';
    html.offsetHeight; // Trigger reflow
    html.style.display = '';
}

function updateThemeIcon(theme) {
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        if (theme === 'light') {
            themeIcon.className = 'fas fa-moon';
            themeIcon.setAttribute('aria-label', 'Switch to dark mode');
        } else {
            themeIcon.className = 'fas fa-sun';
            themeIcon.setAttribute('aria-label', 'Switch to light mode');
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
    
    // Theme toggle button - improved reliability for mobile
    const themeToggleBtn = document.querySelector('.theme-toggle');
    if (themeToggleBtn) {
        // Remove any existing event listeners and onclick
        themeToggleBtn.onclick = null;
        themeToggleBtn.removeAttribute('onclick');

        // Use only click and keyboard events to avoid double toggling on mobile
        const handleThemeToggle = function(e) {
            e.preventDefault();
            e.stopPropagation();
            // Add visual feedback
            themeToggleBtn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                themeToggleBtn.style.transform = 'scale(1)';
            }, 150);
            toggleTheme();
        };

        themeToggleBtn.addEventListener('click', handleThemeToggle, { passive: false });
        // Keyboard support
        themeToggleBtn.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleThemeToggle(e);
            }
        });

        // Ensure button is properly styled for interaction
        themeToggleBtn.style.cursor = 'pointer';
        themeToggleBtn.style.userSelect = 'none';
        themeToggleBtn.style.webkitUserSelect = 'none';
        themeToggleBtn.style.webkitTapHighlightColor = 'transparent';
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

    // Mobile post info collapse functionality
    const mobilePostInfoToggle = document.querySelector('[data-bs-target="#mobilePostInfo"]');
    const mobilePostInfo = document.getElementById('mobilePostInfo');
    const mobileToggleIcon = document.getElementById('mobile-toggle-icon');
    
    if (mobilePostInfoToggle && mobilePostInfo && mobileToggleIcon) {
        mobilePostInfo.addEventListener('show.bs.collapse', function() {
            mobileToggleIcon.classList.remove('fa-chevron-down');
            mobileToggleIcon.classList.add('fa-chevron-up');
        });
        
        mobilePostInfo.addEventListener('hide.bs.collapse', function() {
            mobileToggleIcon.classList.remove('fa-chevron-up');
            mobileToggleIcon.classList.add('fa-chevron-down');
        });
    }
    
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