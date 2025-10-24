document.addEventListener('DOMContentLoaded', function() {
    
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalHTML = submitBtn.innerHTML;
                
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Processando...';
                
                setTimeout(() => {
                    if (submitBtn.disabled) {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalHTML;
                    }
                }, 3000);
            }
        });
    });
    
    const priceInputs = document.querySelectorAll('input[name="price"]');
    priceInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });
    
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Animação de entrada suave para cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    entry.target.style.transition = 'all 0.5s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });
    
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const productName = this.getAttribute('data-product-name') || 'este item';
            const confirmed = confirm(`🗑️ Tem certeza que deseja excluir "${productName}"?\n\nEsta ação não pode ser desfeita.`);
            
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });
    
    const largeIcons = document.querySelectorAll('.display-1, .display-2, .display-3, .display-4');
    largeIcons.forEach(icon => {
        if (icon.classList.contains('bi')) {
            icon.style.transition = 'transform 0.3s ease';
            
            icon.closest('.card')?.addEventListener('mouseenter', () => {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
            });
            
            icon.closest('.card')?.addEventListener('mouseleave', () => {
                icon.style.transform = 'scale(1) rotate(0deg)';
            });
        }
    });
    
    const animateCounter = (element, target, duration = 1000) => {
        let current = 0;
        const increment = target / (duration / 16);
        
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                element.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        };
        
        updateCounter();
    };
    
    const statNumbers = document.querySelectorAll('.card-body h3');
    statNumbers.forEach(stat => {
        const text = stat.textContent.trim();
        const number = parseInt(text.replace(/\D/g, ''));
        
        if (!isNaN(number) && number > 0 && number < 1000) {
            stat.textContent = '0';
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        setTimeout(() => {
                            animateCounter(stat, number);
                        }, 300);
                        observer.unobserve(entry.target);
                    }
                });
            });
            
            observer.observe(stat);
        }
    });
    
    const copyableElements = document.querySelectorAll('[data-copyable]');
    copyableElements.forEach(element => {
        element.style.cursor = 'pointer';
        element.title = 'Clique para copiar';
        
        element.addEventListener('click', async function() {
            const text = this.textContent;
            
            try {
                await navigator.clipboard.writeText(text);
                
                const originalHTML = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check-circle text-success"></i> Copiado!';
                
                setTimeout(() => {
                    this.innerHTML = originalHTML;
                }, 2000);
            } catch (err) {
                console.error('Erro ao copiar:', err);
            }
        });
    });
    
    const navLinks = document.querySelectorAll('a[href]:not([href^="#"]):not([target="_blank"])');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.classList.contains('btn-secondary')) return;
            
            const overlay = document.createElement('div');
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255,255,255,0.9);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
                font-size: 2rem;
            `;
            overlay.innerHTML = '<i class="bi bi-hourglass-split text-primary"></i>';
            
            document.body.appendChild(overlay);
            
            setTimeout(() => {
                overlay.remove();
            }, 3000);
        });
    });
    
    console.log('🛍️ Minha Loja - Sistema carregado com sucesso!');
    console.log('✅ Bootstrap Icons integrado');
    console.log('🎨 Animações e interações ativadas');
});