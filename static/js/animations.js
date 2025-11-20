// Pet Insurance App Animations
document.addEventListener('DOMContentLoaded', function() {
    
    // Add floating pet icons
    createFloatingElements();
    
    // Add click animations to pet cards
    initializePetCards();
    
    // Add particle effects
    createParticleEffect();
    
    // Add scroll animations
    initializeScrollAnimations();
});

// Create floating pet icons in the background
function createFloatingElements() {
    const floatingContainer = document.createElement('div');
    floatingContainer.className = 'floating-container';
    floatingContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    `;
    
    const petIcons = ['🐕', '🐱', '🐾', '❤️', '🏥', '🎾'];
    
    for (let i = 0; i < 8; i++) {
        const element = document.createElement('div');
        element.className = 'floating-element';
        element.innerHTML = petIcons[Math.floor(Math.random() * petIcons.length)];
        element.style.cssText = `
            position: absolute;
            font-size: ${Math.random() * 30 + 20}px;
            opacity: ${Math.random() * 0.3 + 0.1};
            top: ${Math.random() * 100}%;
            left: ${Math.random() * 100}%;
            animation: float ${Math.random() * 4 + 6}s ease-in-out infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
        floatingContainer.appendChild(element);
    }
    
    document.body.appendChild(floatingContainer);
}

// Initialize pet card interactions
function initializePetCards() {
    const petCards = document.querySelectorAll('.pet-card');
    
    petCards.forEach(card => {
        card.addEventListener('click', function() {
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // Add ripple effect
            createRippleEffect(this, event);
            
            // Navigate after animation
            setTimeout(() => {
                const petType = this.dataset.pet;
                if (petType) {
                    window.location.href = `/select-pet/?type=${petType}`;
                }
            }, 300);
        });
        
        // Add flying pets on hover
        card.addEventListener('mouseenter', function() {
            const petType = this.dataset.pet;
            createFlyingPets(this, petType);
        });
        
        // Stop flying pets on leave
        card.addEventListener('mouseleave', function() {
            clearFlyingPets(this);
        });
    });
}

// Create flying pets effect
function createFlyingPets(card, petType) {
    // Clear any existing flying pets first
    clearFlyingPets(card);
    
    const flyingContainer = document.createElement('div');
    flyingContainer.className = 'flying-pets-container';
    flyingContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
        z-index: 10;
        overflow: hidden;
    `;
    
    const pets = petType === 'dog' ? 
        ['🐕', '🦴', '🎾', '❤️', '🐕‍🦺'] : 
        ['🐱', '🐟', '🧶', '💜', '😸'];
    
    // Create multiple flying pets
    for (let i = 0; i < 3; i++) {
        setTimeout(() => {
            const flyingPet = document.createElement('div');
            flyingPet.className = 'flying-pet';
            flyingPet.innerHTML = pets[Math.floor(Math.random() * pets.length)];
            flyingPet.style.cssText = `
                position: absolute;
                font-size: ${Math.random() * 1.5 + 1}rem;
                left: ${Math.random() * 80 + 10}%;
                bottom: 0;
                animation: flyUp ${2 + Math.random() * 2}s ease-out forwards;
                pointer-events: none;
                z-index: 15;
            `;
            flyingContainer.appendChild(flyingPet);
            
            // Remove after animation
            setTimeout(() => {
                if (flyingPet.parentNode) {
                    flyingPet.remove();
                }
            }, 4000);
        }, i * 500);
    }
    
    card.appendChild(flyingContainer);
}

// Clear flying pets
function clearFlyingPets(card) {
    const existingContainer = card.querySelector('.flying-pets-container');
    if (existingContainer) {
        existingContainer.remove();
    }
}

// Create ripple effect on click
function createRippleEffect(element, event) {
    const ripple = document.createElement('div');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s ease-out;
        pointer-events: none;
        z-index: 1000;
    `;
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Create particle effect
function createParticleEffect() {
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particle-container';
    particleContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    `;
    
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(90, 200, 189, 0.6);
            border-radius: 50%;
            top: ${Math.random() * 100}%;
            left: ${Math.random() * 100}%;
            animation: particleFloat ${Math.random() * 10 + 10}s linear infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
        particleContainer.appendChild(particle);
    }
    
    document.body.appendChild(particleContainer);
}

// Initialize scroll animations
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Add CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    @keyframes particleFloat {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    .pet-card {
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes flyUp {
        0% {
            transform: translateY(0) translateX(0) rotate(0deg) scale(1);
            opacity: 0.8;
        }
        25% {
            transform: translateY(-50px) translateX(20px) rotate(10deg) scale(1.2);
            opacity: 1;
        }
        50% {
            transform: translateY(-100px) translateX(-15px) rotate(-8deg) scale(1.1);
            opacity: 0.9;
        }
        75% {
            transform: translateY(-150px) translateX(30px) rotate(15deg) scale(0.9);
            opacity: 0.6;
        }
        100% {
            transform: translateY(-200px) translateX(-10px) rotate(-12deg) scale(0.5);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Affiliate Code Functionality
function applyAffiliateCode() {
    const codeInput = document.getElementById('affiliateCode');
    const statusDiv = document.getElementById('affiliateStatus');
    const statusMessage = statusDiv.querySelector('.status-message');
    const code = codeInput.value.trim().toUpperCase();
    
    // Clear previous status
    statusDiv.style.display = 'none';
    statusDiv.className = 'affiliate-status';
    
    if (!code) {
        showAffiliateStatus('error', 'Παρακαλώ εισάγετε έναν κωδικό συνεργάτη.');
        return;
    }
    
    // Validate code format
    if (code.length < 3) {
        showAffiliateStatus('error', 'Ο κωδικός πρέπει να έχει τουλάχιστον 3 χαρακτήρες.');
        return;
    }
    
    // Call API to validate code
    fetch('/api/validate-affiliate-code/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Store affiliate code in localStorage for later use
            localStorage.setItem('affiliateCode', code);
            
            // Show success message with discount info
            let message = data.message;
            if (data.discount) {
                if (data.discount.type === 'percentage') {
                    message += `<br><strong style="color: #28a745; font-size: 1.1em;">Έκπτωση ${data.discount.value}%</strong>`;
                } else {
                    message += `<br><strong style="color: #28a745; font-size: 1.1em;">Έκπτωση ${data.discount.value}€</strong>`;
                }
            }
            showAffiliateStatus('success', message);
    
            // Add visual feedback to the input
            codeInput.style.borderColor = 'rgba(76, 175, 80, 0.6)';
            codeInput.style.background = 'rgba(76, 175, 80, 0.1)';
        } else {
            showAffiliateStatus('error', data.error || 'Ο κωδικός δεν είναι έγκυρος.');
            codeInput.style.borderColor = 'rgba(220, 53, 69, 0.6)';
            codeInput.style.background = 'rgba(220, 53, 69, 0.1)';
        }
    })
    .catch(error => {
        console.error('Error validating code:', error);
        showAffiliateStatus('error', 'Σφάλμα κατά την επικύρωση του κωδικού. Παρακαλώ δοκιμάστε ξανά.');
    });
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showAffiliateStatus(type, message) {
    const statusDiv = document.getElementById('affiliateStatus');
    const statusMessage = statusDiv.querySelector('.status-message');
    
    statusDiv.className = `affiliate-status ${type}`;
    statusMessage.innerHTML = message; // Use innerHTML to support HTML formatting
    statusDiv.style.display = 'block';
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 5000);
    }
}

// Initialize affiliate code functionality
document.addEventListener('DOMContentLoaded', function() {
    const affiliateInput = document.getElementById('affiliateCode');
    if (affiliateInput) {
        affiliateInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                applyAffiliateCode();
            }
        });
        
        // Load saved affiliate code if exists
        const savedCode = localStorage.getItem('affiliateCode');
        if (savedCode) {
            affiliateInput.value = savedCode;
            showAffiliateStatus('success', `✓ Κωδικός "${savedCode}" είναι ήδη ενεργός.`);
        }
    }
});

