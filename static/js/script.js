// Toggle mobile menu
document.addEventListener('DOMContentLoaded', function() {
    const menuButton = document.querySelector('.menu-button');
    const dropdownMenu = document.querySelector('.dropdown-menu');
    
    menuButton.addEventListener('click', function() {
        dropdownMenu.classList.toggle('show');
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.menu-container')) {
            dropdownMenu.classList.remove('show');
        }
    });
    
    // Add active class to current page in menu
    const currentPage = window.location.pathname;
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        if (item.getAttribute('href') === currentPage) {
            item.classList.add('active');
        }
    });
    
    // Theme Toggle Functionality
    const themeToggle = document.getElementById('theme-toggle');
    
    // Check for saved theme preference or use default
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Set initial theme
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    // If the current theme is dark, check the toggle
    if (currentTheme === 'dark') {
        themeToggle.checked = true;
    }
    
    // Function to switch theme
    function switchTheme(e) {
        if (e.target.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    }
    
    // Add event listener for theme toggle
    themeToggle.addEventListener('change', switchTheme);
    
    // Initialize form placeholders
    if (window.location.pathname === '/date') {
        const formatSelect = document.getElementById('format');
        const dateInput = document.getElementById('date');
        
        if (formatSelect && dateInput) {
            // Set initial placeholder based on default selected format
            updateDatePlaceholder(formatSelect.value);
            
            // Update placeholder when format changes
            formatSelect.addEventListener('change', function() {
                updateDatePlaceholder(this.value);
            });
        }
    }
    
    // Function to update date input placeholder
    function updateDatePlaceholder(format) {
        const dateInput = document.getElementById('date');
        if (!dateInput) return;
        
        switch(format) {
            case 'MM/DD/YYYY':
                dateInput.placeholder = 'e.g., 04/21/2025';
                break;
            case 'DD/MM/YYYY':
                dateInput.placeholder = 'e.g., 21/04/2025';
                break;
            case 'YYYY-MM-DD':
                dateInput.placeholder = 'e.g., 2025-04-21';
                break;
            case 'Month DD, YYYY':
                dateInput.placeholder = 'e.g., April 21, 2025';
                break;
            default:
                dateInput.placeholder = 'Enter date';
        }
    }
    
    // Add pulse effect to validate buttons
    const validateButtons = document.querySelectorAll('.validate-btn');
    validateButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.classList.add('pulse');
        });
        
        button.addEventListener('mouseleave', function() {
            this.classList.remove('pulse');
        });
    });
});