/* ==========================================================================
   CODEZEN TUTOR - APP JAVASCRIPT LOGIC
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

    // 1. TYPING EFFECT (HERO TITLE)
    const typingTextEl = document.getElementById('typingText');
    const words = ["Scratch", "Python", "C++ Nền Tảng", "Sinh Viên CNTT"];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;

    function typeEffect() {
        const currentWord = words[wordIndex];
        
        if (isDeleting) {
            typingTextEl.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 50; // Deleting is faster
        } else {
            typingTextEl.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 120; // Typing speed
        }

        // Word completed typing
        if (!isDeleting && charIndex === currentWord.length) {
            typingSpeed = 1500; // Pause at full word
            isDeleting = true;
        } 
        // Word deleted fully
        else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            typingSpeed = 500; // Pause before typing next word
        }

        setTimeout(typeEffect, typingSpeed);
    }
    
    if (typingTextEl) {
        typeEffect();
    }

    // 2. STICKY HEADER TRANSITION ON SCROLL
    const mainHeader = document.getElementById('mainHeader');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            mainHeader.classList.add('scrolled');
        } else {
            mainHeader.classList.remove('scrolled');
        }
    });

    // 3. MOBILE MENU HAMBURGER TOGGLE
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const navMenu = document.getElementById('navMenu');
    
    if (hamburgerBtn && navMenu) {
        hamburgerBtn.addEventListener('click', () => {
            hamburgerBtn.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close mobile menu when clicking nav links
        document.querySelectorAll('.nav-link, .nav-btn-mobile').forEach(link => {
            link.addEventListener('click', () => {
                hamburgerBtn.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }

    // 4. THEME SWITCHER (DARK / LIGHT MODE)
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    
    // Check saved theme or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (savedTheme === 'light') {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
    } else {
        document.body.classList.remove('light-mode');
        document.body.classList.add('dark-mode');
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            if (document.body.classList.contains('dark-mode')) {
                document.body.classList.remove('dark-mode');
                document.body.classList.add('light-mode');
                localStorage.setItem('theme', 'light');
            } else {
                document.body.classList.remove('light-mode');
                document.body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark');
            }
        });
    }

    // 5. PATHWAY TAB SWITCHER
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            
            // Remove active classes
            tabButtons.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            // Add active to current
            btn.classList.add('active');
            
            const targetPane = document.getElementById(`tab-${targetTab}`);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });

    // 6. INTERACTIVE TUITION CALCULATOR
    // Course Database
    const coursesDb = {
        cap1: [
            {
                id: "scratch_basic",
                title: "Lập Trình Scratch Cơ Bản",
                desc: "Phát triển tư duy logic, sáng tạo trò chơi trực quan cho học sinh cấp 1 bằng công cụ kéo thả Scratch khối lệnh chuẩn MIT.",
                rate: 200000, // đ per hour
                length: 1.5 // hours per session
            },
            {
                id: "scratch_advanced",
                title: "Lập Trình Scratch Nâng Cao",
                desc: "Học sâu cấu trúc khối lệnh tự định nghĩa, clone nhân vật, tương tác vật lý game và lập trình thuật toán trò chơi phức tạp.",
                rate: 220000,
                length: 1.5
            }
        ],
        cap2: [
            {
                id: "python_basic",
                title: "Lập Trình Python Cơ Bản",
                desc: "Bước đầu làm quen cú pháp dòng lệnh viết tay Python, rèn luyện cấu trúc rẽ nhánh, mảng danh sách và viết tập lệnh giải toán logic.",
                rate: 250000,
                length: 1.5
            },
            {
                id: "python_pygame",
                title: "Lập Trình Python & Đồ Họa Pygame",
                desc: "Học mảng nâng cao, xử lý file, kết hợp lập trình game đồ họa 2D Pygame thực chiến tăng tính hứng thú tư duy trực quan.",
                rate: 280000,
                length: 1.5
            }
        ],
        cap3: [
            {
                id: "cplus_basic",
                title: "Giải Thuật C++ Nền Tảng",
                desc: "Xây dựng tư duy giải thuật tối ưu trên C++, mảng động, thao tác tệp, con trỏ. Chuẩn bị nền tảng vững chắc cho học sinh giỏi tin học.",
                rate: 300000,
                length: 1.5
            },
            {
                id: "cplus_advanced",
                title: "Luyện Thi Học Sinh Giỏi / Tin Học Trẻ",
                desc: "Đào tạo chuyên giải đề thi HSG, Olympic. Quy hoạch động, thuật toán đồ thị cơ bản đến nâng cao, tối ưu độ phức tạp thuật toán O(N).",
                rate: 350000,
                length: 1.5
            }
        ],
        sinhvien: [
            {
                id: "dsa_uni",
                title: "Cấu Trúc Dữ Liệu & Giải Thuật Đại Học",
                desc: "Lấy lại gốc đại học, hiểu sâu bản chất phân phối RAM bộ nhớ con trỏ, cấu trúc Stack, Queue, Linked List, Cây nhị phân trên C++/Java.",
                rate: 350000,
                length: 1.5
            },
            {
                id: "oop_java",
                title: "Lập Trình Hướng Đối Tượng (OOP)",
                desc: "Thấu suốt 4 tính chất OOP (Đóng gói, Kế thừa, Đa hình, Trừu tượng). Rèn luyện viết code chuẩn clean code trên nền tảng Java/C++.",
                rate: 320000,
                length: 1.5
            },
            {
                id: "web_fullstack",
                title: "Lập Trình Web ReactJS & NodeJS",
                desc: "Hướng dẫn thực hành xây dựng ứng dụng Web Fullstack Front-End React và Back-End API Node.js/SQL. Đồng hành hỗ trợ làm đồ án xuất sắc.",
                rate: 380000,
                length: 1.5
            }
        ]
    };

    const levelRadios = document.querySelectorAll('input[name="student_level"]');
    const courseSelect = document.getElementById('course_package');
    const sessionBtns = document.querySelectorAll('#sessionsPerWeek .toggle-btn');
    
    let activeLevel = "cap1";
    let activeSessions = 2; // Default 2 sessions per week

    // Populate course dropdown based on level
    function populateCourses(level) {
        if (!courseSelect) return;
        courseSelect.innerHTML = "";
        
        const courses = coursesDb[level];
        courses.forEach(course => {
            const option = document.createElement('option');
            option.value = course.id;
            option.textContent = course.title;
            courseSelect.appendChild(option);
        });

        calculateTuition();
    }

    // Main calculator math logic
    function calculateTuition() {
        if (!courseSelect) return;
        
        const selectedCourseId = courseSelect.value;
        const courses = coursesDb[activeLevel];
        const activeCourse = courses.find(c => c.id === selectedCourseId);

        if (!activeCourse) return;

        // Update suggested details
        document.getElementById('suggestedCourseTitle').textContent = activeCourse.title;
        document.getElementById('suggestedCourseDesc').textContent = activeCourse.desc;
        
        // Formatting function
        const formatCurrency = (val) => {
            return new Intl.NumberFormat('vi-VN').format(val) + " đ";
        };

        // Rates
        const rate = activeCourse.rate;
        const length = activeCourse.length;
        const sessionPrice = rate * length;
        
        // Monthly math
        const monthlySessions = activeSessions * 4;
        const monthlyPrice = sessionPrice * monthlySessions;

        // Write to DOM
        document.getElementById('hourlyRate').innerHTML = `${formatCurrency(rate)} <span class="unit">/ giờ</span>`;
        document.getElementById('sessionRate').innerHTML = `${formatCurrency(sessionPrice)} <span class="unit">/ buổi</span>`;
        document.getElementById('monthlyTotal').textContent = formatCurrency(monthlyPrice);
    }

    // Radio Listeners
    levelRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.checked) {
                activeLevel = e.target.value;
                populateCourses(activeLevel);
            }
        });
    });

    // Select Listener
    if (courseSelect) {
        courseSelect.addEventListener('change', calculateTuition);
    }

    // Session buttons listener
    sessionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            sessionBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeSessions = parseInt(btn.getAttribute('data-val'));
            calculateTuition();
        });
    });

    // Init Calculator on load
    populateCourses("cap1");

    // 7. TESTIMONIAL SLIDER
    const slider = document.getElementById('testimonialSlider');
    const slides = document.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('#sliderDots .dot');
    let currentSlide = 0;
    let sliderInterval;

    function showSlide(index) {
        if (index < 0) index = slides.length - 1;
        if (index >= slides.length) index = 0;
        
        currentSlide = index;
        
        slides.forEach((slide, i) => {
            if (i === currentSlide) {
                slide.classList.add('active');
            } else {
                slide.classList.remove('active');
            }
        });

        dots.forEach((dot, i) => {
            if (i === currentSlide) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    function startSliderAutoPlay() {
        sliderInterval = setInterval(() => {
            showSlide(currentSlide + 1);
        }, 6000); // 6s cycle
    }

    function stopSliderAutoPlay() {
        clearInterval(sliderInterval);
    }

    // Dot click listeners
    dots.forEach(dot => {
        dot.addEventListener('click', () => {
            const targetIdx = parseInt(dot.getAttribute('data-index'));
            showSlide(targetIdx);
            stopSliderAutoPlay();
            startSliderAutoPlay(); // Reset timer
        });
    });

    if (slider && slides.length > 0) {
        startSliderAutoPlay();
    }

    // 8. CONTACT LEAD FORM VALIDATION AND SUBMISSION
    const leadForm = document.getElementById('leadForm');
    const parentNameInput = document.getElementById('parent_name');
    const phoneInput = document.getElementById('phone_number');
    const emailInput = document.getElementById('email_address');
    const levelSelect = document.getElementById('child_level');
    const notesInput = document.getElementById('notes');

    // Success Modal elements
    const successModalOverlay = document.getElementById('successModalOverlay');
    const modalParentName = document.getElementById('modalParentName');
    const modalPhone = document.getElementById('modalPhone');
    const modalLevel = document.getElementById('modalLevel');
    const modalCloseBtn = document.getElementById('modalCloseBtn');

    // Utility validators
    function validatePhone(phone) {
        // Simple Vietnamese 10-digit number validator starting with 0
        const phoneRegex = /^(0[3|5|7|8|9])[0-9]{8}$/;
        return phoneRegex.test(phone.trim());
    }

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email.trim());
    }

    function setError(inputEl, errorElId, isError) {
        const formGroup = inputEl.closest('.form-group');
        if (isError) {
            formGroup.classList.add('invalid');
        } else {
            formGroup.classList.remove('invalid');
        }
    }

    // Input listeners to clear errors on keyup/change
    if (parentNameInput) {
        parentNameInput.addEventListener('input', () => {
            if (parentNameInput.value.trim() !== "") {
                setError(parentNameInput, null, false);
            }
        });
    }

    if (phoneInput) {
        phoneInput.addEventListener('input', () => {
            if (validatePhone(phoneInput.value)) {
                setError(phoneInput, null, false);
            }
        });
    }

    if (emailInput) {
        emailInput.addEventListener('input', () => {
            if (validateEmail(emailInput.value)) {
                setError(emailInput, null, false);
            }
        });
    }

    if (leadForm) {
        leadForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            let isFormValid = true;

            // 1. Name validate
            if (parentNameInput.value.trim() === "") {
                setError(parentNameInput, null, true);
                isFormValid = false;
            } else {
                setError(parentNameInput, null, false);
            }

            // 2. Phone validate
            if (!validatePhone(phoneInput.value)) {
                setError(phoneInput, null, true);
                isFormValid = false;
            } else {
                setError(phoneInput, null, false);
            }

            // 3. Email validate
            if (!validateEmail(emailInput.value)) {
                setError(emailInput, null, true);
                isFormValid = false;
            } else {
                setError(emailInput, null, false);
            }

            if (!isFormValid) {
                // Scroll to first invalid item
                const firstInvalid = document.querySelector('.form-group.invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                return;
            }

            // Form is fully valid - Process lead registration
            const levelTextMap = {
                cap1: "Học sinh Cấp 1",
                cap2: "Học sinh Cấp 2",
                cap3: "Học sinh Cấp 3",
                sinhvien: "Sinh Viên Đại Học"
            };

            const parentNameVal = parentNameInput.value.trim();
            const phoneVal = phoneInput.value.trim();
            const emailVal = emailInput.value.trim();
            const levelVal = levelSelect.value;
            const notesVal = notesInput.value.trim();

            const leadObj = {
                parentName: parentNameVal,
                phone: phoneVal,
                email: emailVal,
                level: levelVal,
                levelText: levelTextMap[levelVal],
                notes: notesVal,
                timestamp: new Date().toISOString()
            };

            // Save to localStorage Offline DB for demonstration/static administration
            const existingLeads = JSON.parse(localStorage.getItem('codezen_leads')) || [];
            existingLeads.push(leadObj);
            localStorage.setItem('codezen_leads', JSON.stringify(existingLeads));

            // Populate success modal
            if (modalParentName && modalPhone && modalLevel) {
                modalParentName.textContent = parentNameVal;
                modalPhone.textContent = phoneVal;
                modalLevel.textContent = levelTextMap[levelVal];
            }

            // Display success modal
            if (successModalOverlay) {
                successModalOverlay.classList.add('active');
            }

            // Reset form
            leadForm.reset();
        });
    }

    // Close Modal Listener
    if (modalCloseBtn && successModalOverlay) {
        modalCloseBtn.addEventListener('click', () => {
            successModalOverlay.classList.remove('active');
        });

        // Close when clicking overlay backdrop
        successModalOverlay.addEventListener('click', (e) => {
            if (e.target === successModalOverlay) {
                successModalOverlay.classList.remove('active');
            }
        });
    }

});
