// main.js - JobPortal Interactions

document.addEventListener('DOMContentLoaded', () => {

    // Mobile Navbar Toggle
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');
    
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            const icon = navToggle.querySelector('i');
            if(navLinks.classList.contains('open')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // Auto-dismiss Alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(() => {
                const parent = alert.parentElement;
                if(parent) parent.remove();
            }, 400); // Wait for transition
        }, 5000);
    });

    // Profile Tabs (if any)
    const tabs = document.querySelectorAll('.profile-tab');
    if (tabs.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
            });
        });
    }
});
