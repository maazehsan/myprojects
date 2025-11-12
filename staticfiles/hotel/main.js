  AOS.init({
            duration: 1000,
            once: true,
            offset: 100
        });

        window.addEventListener('scroll', function() {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        function toggleMenu() {
            const navLinks = document.getElementById('navLinks');
            navLinks.classList.toggle('active');
        }

        function showPage(pageId) {
            document.querySelectorAll('.page').forEach(page => {
                page.classList.add('hidden');
            });
            
            const newPage = document.getElementById(pageId);
            newPage.classList.remove('hidden');
            
            document.querySelectorAll('.nav-links a').forEach(link => {
                link.classList.remove('active');
            });
            
            document.getElementById('navLinks').classList.remove('active');
            
            // Scroll to top
            window.scrollTo(0, 0);
            
            // Completely reinitialize AOS
            setTimeout(() => {
                AOS.init({
                    duration: 1000,
                    once: false,
                    offset: 100,
                    disable: false,
                    startEvent: 'DOMContentLoaded',
                    initClassName: 'aos-init',
                    animatedClassName: 'aos-animate'
                });
            }, 100);
        }


        let currentTestimonial = 0;
        const testimonials = document.querySelectorAll('.testimonial');
        const dots = document.querySelectorAll('.dot');

        function showTestimonial(n) {
            testimonials.forEach(testimonial => testimonial.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));
            
            currentTestimonial = (n + testimonials.length) % testimonials.length;
            
            testimonials[currentTestimonial].classList.add('active');
            dots[currentTestimonial].classList.add('active');
        }

        function currentSlide(n) {
            showTestimonial(n);
        }

        setInterval(() => {
            showTestimonial(currentTestimonial + 1);
        }, 5000);


        document.querySelector('.submit-btn').addEventListener('click', function(e) {
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;
            
            // Remove any existing alerts
            const existingAlert = document.querySelector('.form-alert');
            if (existingAlert) {
                existingAlert.remove();
            }
            
            // Create new alert element
            const alertDiv = document.createElement('div');
            alertDiv.className = 'form-alert';
            
            if (name && email && subject && message) {
                alertDiv.classList.add('success');
                alertDiv.textContent = 'Thank you for your message! We will get back to you soon.';
                
                // Insert alert at the top of the form
                const contactForm = document.querySelector('.contact-form');
                contactForm.insertBefore(alertDiv, contactForm.firstChild);
                
                // Clear form after short delay
                setTimeout(() => {
                    contactForm.reset();
                }, 500);
            } else {
                alertDiv.classList.add('error');
                alertDiv.textContent = 'Please fill in all fields.';
                
                // Insert alert at the top of the form
                const contactForm = document.querySelector('.contact-form');
                contactForm.insertBefore(alertDiv, contactForm.firstChild);
            }
            
            // Automatically remove the alert after 5 seconds
            setTimeout(() => {
                alertDiv.style.opacity = '0';
                setTimeout(() => alertDiv.remove(), 300);
            }, 5000);
        });


        document.querySelector('.newsletter-form button').addEventListener('click', function() {
            const email = this.previousElementSibling.value;
            if (email) {
                alert('Thank you for subscribing to our newsletter!');
                this.previousElementSibling.value = '';
            } else {
                alert('Please enter your email address.');
            }
        });