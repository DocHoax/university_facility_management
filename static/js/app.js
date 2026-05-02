document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('[data-nav-toggle]');
    const header = document.querySelector('[data-nav-root]');
    const nav = document.querySelector('[data-primary-nav]');
    const notificationBadge = document.querySelector('[data-notification-badge]');
    const notificationLink = document.querySelector('[data-notification-link]');

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

    const updateNotificationBadge = (count) => {
        if (!notificationBadge || !notificationLink) {
            return;
        }

        if (count > 0) {
            notificationBadge.textContent = count > 99 ? '99+' : String(count);
            notificationBadge.hidden = false;
            notificationLink.classList.add('has-notifications');
        } else {
            notificationBadge.hidden = true;
            notificationBadge.textContent = '0';
            notificationLink.classList.remove('has-notifications');
        }
    };

    const refreshNotifications = async () => {
        if (!notificationBadge || !notificationLink) {
            return;
        }

        try {
            const response = await fetch('/notifications/live/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
                cache: 'no-store',
            });

            if (!response.ok) {
                return;
            }

            const data = await response.json();
            updateNotificationBadge(Number(data.unread_count || 0));
        } catch (error) {
            // Polling should fail silently so the site remains usable offline or during brief network issues.
        }
    };

    refreshNotifications();
    window.setInterval(refreshNotifications, 8000);
});
