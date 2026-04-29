document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('[data-nav-toggle]');
    const header = document.querySelector('[data-nav-root]');
    const nav = document.querySelector('[data-primary-nav]');

    if (!toggle || !header || !nav) {
        return;
    }

    const closeNav = () => {
        header.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
    };

    toggle.addEventListener('click', () => {
        const isOpen = header.classList.toggle('nav-open');
        toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    nav.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
            if (window.matchMedia('(max-width: 960px)').matches) {
                closeNav();
            }
        });
    });

    window.addEventListener('resize', () => {
        if (!window.matchMedia('(max-width: 960px)').matches) {
            closeNav();
        }
    });
});
