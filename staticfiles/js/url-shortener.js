// static/js/url-shortener.js

class URLShortenerApp {
    constructor() {
        this.form = document.getElementById('shorten-form');
        this.resultContainer = document.getElementById('result');
        this.errorContainer = document.getElementById('error');
        this.loadingContainer = document.getElementById('loading');
        
        this.init();
    }
    
    init() {
        if (this.form) {
            this.bindEvents();
            this.setupFormValidation();
        }
    }
    
    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Real-time URL validation
        const urlInput = document.getElementById('original_url');
        if (urlInput) {
            urlInput.addEventListener('input', (e) => this.validateURLInput(e.target));
        }
        
        // Expiration date validation
        const expiresInput = document.getElementById('expires_at');
        if (expiresInput) {
            expiresInput.addEventListener('change', (e) => this.validateExpirationDate(e.target));
        }
    }
    
    setupFormValidation() {
        const inputs = this.form.querySelectorAll('input[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });
    }
    
    validateURLInput(input) {
        const url = input.value.trim();
        
        if (url && !this.isValidURL(url)) {
            this.showFieldError(input, 'URL inválida. Use o formato: https://exemplo.com');
            return false;
        }
        
        this.clearFieldError(input);
        return true;
    }
    
    validateExpirationDate(input) {
        const selectedDate = new Date(input.value);
        const now = new Date();
        
        if (input.value && selectedDate <= now) {
            this.showFieldError(input, 'A data de expiração deve ser no futuro');
            return false;
        }
        
        this.clearFieldError(input);
        return true;
    }
    
    validateField(input) {
        if (input.hasAttribute('required') && !input.value.trim()) {
            this.showFieldError(input, 'Este campo é obrigatório');
            return false;
        }
        
        if (input.type === 'url') {
            return this.validateURLInput(input);
        }
        
        if (input.type === 'datetime-local') {
            return this.validateExpirationDate(input);
        }
        
        return true;
    }
    
    showFieldError(input, message) {
        this.clearFieldError(input);
        
        input.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        
        input.parentNode.appendChild(errorDiv);
    }
    
    clearFieldError(input) {
        input.classList.remove('is-invalid');
        
        const errorDiv = input.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    isValidURL(string) {
        try {
            const url = new URL(string);
            return url.protocol === 'http:' || url.protocol === 'https:';
        } catch (_) {
            return false;
        }
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            return;
        }
        
        this.showLoading();
        
        try {
            const formData = new FormData(this.form);
            const response = await fetch(this.form.dataset.url || '/shorten/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showSuccess(data);
                this.clearForm();
            } else {
                this.showError(data.error || 'Erro desconhecido');
            }
            
        } catch (error) {
            console.error('Erro na requisição:', error);
            this.showError('Erro de conexão. Tente novamente.');
        } finally {
            this.hideLoading();
        }
    }
    
    validateForm() {
        const inputs = this.form.querySelectorAll('input[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    showLoading() {
        this.hideAllMessages();
        if (this.loadingContainer) {
            this.loadingContainer.style.display = 'block';
            this.loadingContainer.classList.add('fade-in');
        }
    }
    
    hideLoading() {
        if (this.loadingContainer) {
            this.loadingContainer.style.display = 'none';
        }
    }
    
    showSuccess(data) {
        this.hideAllMessages();
        
        if (this.resultContainer) {
            const shortUrlInput = document.getElementById('short-url');
            const originalUrlDisplay = document.getElementById('original-url-display');
            const expiresInfo = document.getElementById('expires-info');
            const expiresDisplay = document.getElementById('expires-at-display');
            
            if (shortUrlInput) shortUrlInput.value = data.short_url;
            if (originalUrlDisplay) originalUrlDisplay.textContent = data.original_url;
            
            if (data.expires_at && expiresInfo && expiresDisplay) {
                const expireDate = new Date(data.expires_at);
                expiresDisplay.textContent = expireDate.toLocaleString('pt-BR');
                expiresInfo.style.display = 'block';
            } else if (expiresInfo) {
                expiresInfo.style.display = 'none';
            }
            
            this.resultContainer.style.display = 'block';
            this.resultContainer.classList.add('slide-up');
            
            // Focus no input da URL encurtada para facilitar cópia
            if (shortUrlInput) {
                setTimeout(() => shortUrlInput.select(), 100);
            }
        }
        
        // Show success toast
        URLShortener.showToast('URL encurtada com sucesso!', 'success');
    }
    
    showError(message) {
        this.hideAllMessages();
        
        if (this.errorContainer) {
            const errorMessage = document.getElementById('error-message');
            if (errorMessage) {
                errorMessage.textContent = message;
            }
            
            this.errorContainer.style.display = 'block';
            this.errorContainer.classList.add('fade-in');
        }
        
        // Show error toast
        URLShortener.showToast(message, 'error');
    }
    
    hideAllMessages() {
        [this.resultContainer, this.errorContainer, this.loadingContainer].forEach(container => {
            if (container) {
                container.style.display = 'none';
                container.classList.remove('fade-in', 'slide-up');
            }
        });
    }
    
    clearForm() {
        const inputs = this.form.querySelectorAll('input:not([type="hidden"])');
        inputs.forEach(input => {
            input.value = '';
            this.clearFieldError(input);
        });
    }
}

// Copy to clipboard function specifically for URL results
function copyShortURL() {
    const shortUrlInput = document.getElementById('short-url');
    const copyButton = document.querySelector('.btn-copy');
    
    if (shortUrlInput && copyButton) {
        URLShortener.copyToClipboard(shortUrlInput.value, copyButton);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new URLShortenerApp();
    
    // Make copy function globally available
    window.copyShortURL = copyShortURL;
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = URLShortenerApp;
}
