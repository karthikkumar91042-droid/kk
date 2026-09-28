// BusGo - Main JavaScript

// ── Mobile Nav Toggle ────────────────────────────────────────
function toggleNav() {
    const links = document.getElementById('navLinks');
    if (links) links.classList.toggle('open');
}

// Close nav on outside click
document.addEventListener('click', function (e) {
    const nav = document.getElementById('navLinks');
    const btn = document.getElementById('hamburger');
    if (nav && btn && !nav.contains(e.target) && !btn.contains(e.target)) {
        nav.classList.remove('open');
    }
});

// ── Auto-dismiss Flash Messages ──────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(100%)';
            flash.style.transition = 'all 0.3s ease';
            setTimeout(() => flash.remove(), 300);
        }, 4000);
    });
});

// ── Search Form Validation ───────────────────────────────────
const searchForm = document.getElementById('searchForm');
if (searchForm) {
    searchForm.addEventListener('submit', function (e) {
        const src = document.getElementById('source').value;
        const dst = document.getElementById('destination').value;
        if (src === dst && src !== '') {
            e.preventDefault();
            alert('Source and destination cannot be the same city!');
            return;
        }
        const btn = document.getElementById('searchBtn');
        if (btn) {
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
            btn.disabled = true;
        }
    });
}

// ── Active Nav Link Highlight ────────────────────────────────
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
        link.style.color = '#6366f1';
    }
});

// ── Smooth scroll for anchor links ──────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ── Input field animation ────────────────────────────────────
document.querySelectorAll('.form-group input, .form-group select').forEach(el => {
    el.addEventListener('focus', function () {
        this.parentElement.style.transform = 'scale(1.01)';
        this.parentElement.style.transition = 'transform 0.2s ease';
    });
    el.addEventListener('blur', function () {
        this.parentElement.style.transform = '';
    });
});

// ── Tooltip helper ───────────────────────────────────────────
document.querySelectorAll('[title]').forEach(el => {
    el.addEventListener('mouseenter', function () {
        const tip = document.createElement('div');
        tip.className = 'tooltip-popup';
        tip.textContent = this.getAttribute('title');
        tip.style.cssText = `
            position: fixed;
            background: rgba(0,0,0,0.85);
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.78rem;
            pointer-events: none;
            z-index: 10000;
            white-space: nowrap;
        `;
        document.body.appendChild(tip);
        const rect = this.getBoundingClientRect();
        tip.style.top  = (rect.top - 36) + 'px';
        tip.style.left = (rect.left + rect.width / 2 - tip.offsetWidth / 2) + 'px';
        this._tooltip = tip;
    });
    el.addEventListener('mouseleave', function () {
        if (this._tooltip) {
            this._tooltip.remove();
            this._tooltip = null;
        }
    });
});
