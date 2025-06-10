// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize form animations
    initializeFormAnimations();
    
    // Initialize copy functionality
    initializeCopyFunctionality();
});

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initializeFormAnimations() {
    const inputs = document.querySelectorAll('.form-control-custom');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
    });
}

function initializeCopyFunctionality() {
    window.copyToClipboard = function(text, button) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text).then(() => {
                showCopySuccess(button);
            }).catch(() => {
                fallbackCopyTextToClipboard(text, button);
            });
        } else {
            fallbackCopyTextToClipboard(text, button);
        }
    };
}

function fallbackCopyTextToClipboard(text, button) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopySuccess(button);
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
        showToast('Erro ao copiar. Tente selecionar e copiar manualmente.', 'error');
    }
    
    document.body.removeChild(textArea);
}

function showCopySuccess(button) {
    const originalText = button.innerHTML;
    const originalClasses = button.className;
    
    button.innerHTML = '✅ Copiado!';
    button.className = button.className.replace('btn-outline-secondary', 'btn-success');
    button.classList.add('copied');
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.className = originalClasses;
        button.classList.remove('copied');
    }, 2000);
}

function showToast(message, type = 'info') {
    const toastContainer = getOrCreateToastContainer();
    const toastId = 'toast-' + Date.now();
    
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : 'primary'} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '11';
        document.body.appendChild(container);
    }
    return container;
}

// Utility functions
function showElement(elementId, display = 'block') {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = display;
        element.classList.add('fade-in');
    }
}

function hideElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
        element.classList.remove('fade-in');
    }
}

function toggleElement(elementId, display = 'block') {
    const element = document.getElementById(elementId);
    if (element) {
        if (element.style.display === 'none' || !element.style.display) {
            showElement(elementId, display);
        } else {
            hideElement(elementId);
        }
    }
}

// Loading states
function showLoading(message = 'Carregando...') {
    const loadingHTML = `
        <div class="loading-container">
            <div class="spinner-custom"></div>
            <p class="mt-3">${message}</p>
        </div>
    `;
    
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.innerHTML = loadingHTML;
        showElement('loading');
    }
}

function hideLoading() {
    hideElement('loading');
}

// Form validation helpers
function validateURL(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Date formatting
function formatDate(dateString, locale = 'pt-BR') {
    const date = new Date(dateString);
    return date.toLocaleString(locale);
}

// Export functions for global use
window.URLShortener = {
    showToast,
    showElement,
    hideElement,
    toggleElement,
    showLoading,
    hideLoading,
    validateURL,
    formatDate,
    copyToClipboard
};
