const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
const navLinkItems = document.querySelectorAll('.nav-link');
const revealElements = document.querySelectorAll('.reveal');
const sliderTrack = document.querySelector('.slider-track');
const sliderCards = document.querySelectorAll('.testimonial-card');
const prevButton = document.querySelector('.slider-control.prev');
const nextButton = document.querySelector('.slider-control.next');
let sliderIndex = 0;
let sliderInterval;

// Toggle navigation on mobile
navToggle?.addEventListener('click', () => {
    navToggle.classList.toggle('open');
    navLinks?.classList.toggle('open');
});

navLinkItems.forEach(link => link.addEventListener('click', () => {
    navLinks?.classList.remove('open');
    navToggle?.classList.remove('open');
}));

// Smoothly highlight active navigation link
const sections = document.querySelectorAll('section');
const observerOptions = {
    threshold: 0.35
};

const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            navLinkItems.forEach(link => {
                link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
            });
        }
    });
}, observerOptions);

sections.forEach(section => sectionObserver.observe(section));

// Reveal animations on scroll
const revealObserver = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
            obs.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.25,
    rootMargin: '0px 0px -10% 0px'
});

revealElements.forEach(el => revealObserver.observe(el));

// Testimonials slider logic
function updateSlider(index) {
    if (!sliderTrack || sliderCards.length === 0) return;
    const cardWidth = sliderCards[0].offsetWidth + 24; // width + gap approximation
    sliderTrack.scrollTo({
        left: cardWidth * index,
        behavior: 'smooth'
    });
}

function showNextSlide() {
    sliderIndex = (sliderIndex + 1) % sliderCards.length;
    updateSlider(sliderIndex);
}

function showPrevSlide() {
    sliderIndex = (sliderIndex - 1 + sliderCards.length) % sliderCards.length;
    updateSlider(sliderIndex);
}

nextButton?.addEventListener('click', () => {
    showNextSlide();
    restartSliderInterval();
});

prevButton?.addEventListener('click', () => {
    showPrevSlide();
    restartSliderInterval();
});

function startSliderInterval() {
    sliderInterval = setInterval(showNextSlide, 6000);
}

function restartSliderInterval() {
    clearInterval(sliderInterval);
    startSliderInterval();
}

if (sliderCards.length > 0) {
    startSliderInterval();
}

// Back to top gentle scroll effect
const backToTop = document.querySelector('.back-to-top');
backToTop?.addEventListener('click', (event) => {
    event.preventDefault();
    document.getElementById('home')?.scrollIntoView({ behavior: 'smooth' });
});

// Add floating sparkle effect to hero badges
const heroBadges = document.querySelector('.hero-badges');
if (heroBadges) {
    const sparkle = document.createElement('span');
    sparkle.className = 'sparkle';
    heroBadges.appendChild(sparkle);

    setInterval(() => {
        sparkle.style.left = `${Math.random() * 100}%`;
        sparkle.style.top = `${Math.random() * 100}%`;
        sparkle.classList.remove('animate');
        void sparkle.offsetWidth; // restart animation
        sparkle.classList.add('animate');
    }, 2500);
}
