/**
 * LOGIC CHO VÒNG QUAY PHẦN THƯỞNG
 */

document.addEventListener('DOMContentLoaded', () => {
    const btnVerifyCode = document.getElementById('btnVerifyCode');
    const spinCodeInput = document.getElementById('spinCode');
    const spinMessage = document.getElementById('spinMessage');
    const spinActionBox = document.getElementById('spinActionBox');
    const btnSpin = document.getElementById('btnSpin');
    const wheel = document.getElementById('wheel');
    const rewardModalOverlay = document.getElementById('rewardModalOverlay');
    const rewardModalCloseBtn = document.getElementById('rewardModalCloseBtn');
    const rewardResult = document.getElementById('rewardResult');

    // Cấu hình các phần thưởng theo thứ tự các góc trên wheel (mỗi góc 60 độ)
    // Wheel chia làm 6 phần, bắt đầu từ 0-60 độ, 60-120, ... theo chiều kim đồng hồ
    const segments = [
        "Giảm 10% Học Phí",
        "Giảm 20% Học Phí",
        "Học Thử 2 Buổi Miễn Phí",
        "Chúc Bạn May Mắn Lần Sau",
        "Giảm 5% Học Phí",
        "Áo Thun Gia Sư THT"
    ];

    let currentRotation = 0;
    let isSpinning = false;
    let validatedCode = null;

    // Giả lập danh sách mã hợp lệ (có thể mở rộng hoặc kết nối API)
    const validCodes = ['THT2026', 'GIASUVIP', 'HOCCODE', 'PYTHON50', 'CPLUS100'];

    if (btnVerifyCode) {
        btnVerifyCode.addEventListener('click', () => {
            const code = spinCodeInput.value.trim().toUpperCase();
            if (!code) {
                showMessage('Vui lòng nhập mã quay thưởng!', 'error');
                return;
            }

            // Trong môi trường production, bước này nên gọi API. Ở đây giả lập tĩnh.
            if (!validCodes.includes(code)) {
                showMessage('Mã quay thưởng không hợp lệ hoặc không tồn tại.', 'error');
                return;
            }

            // Kiểm tra mã đã được sử dụng chưa (sử dụng localStorage để demo)
            const usedCodes = JSON.parse(localStorage.getItem('usedSpinCodes') || '[]');
            if (usedCodes.includes(code)) {
                showMessage('Mã này đã được sử dụng. Vui lòng nhập mã khác.', 'error');
                return;
            }

            // Mã hợp lệ và chưa sử dụng
            showMessage('Mã hợp lệ! Bạn có 1 lượt quay.', 'success');
            validatedCode = code;
            spinCodeInput.disabled = true;
            btnVerifyCode.disabled = true;
            spinActionBox.style.display = 'block';
        });
    }

    if (btnSpin) {
        btnSpin.addEventListener('click', () => {
            if (isSpinning || !validatedCode) return;
            
            isSpinning = true;
            btnSpin.disabled = true;
            
            // Số vòng quay random từ 5 đến 10 vòng
            const spins = Math.floor(Math.random() * 5) + 5;
            // Góc dừng random (0 đến 359)
            const randomDegree = Math.floor(Math.random() * 360);
            
            // Tổng góc quay tính từ vị trí hiện tại
            const totalDegree = (spins * 360) + randomDegree;
            currentRotation += totalDegree;
            
            // Áp dụng CSS quay
            wheel.style.transform = `rotate(${currentRotation}deg)`;
            
            // Tính toán phần thưởng
            // Vòng quay quay góc currentRotation. 
            // Mũi tên nằm ở vị trí 0 độ (trên cùng). 
            // Vùng chiếu vào mũi tên sẽ là vùng có góc ban đầu bị kéo ngược lại.
            const normalizedDegree = (360 - (currentRotation % 360)) % 360;
            
            // Mỗi đoạn là 60 độ
            const winningIndex = Math.floor(normalizedDegree / 60);
            const reward = segments[winningIndex];

            // Đánh dấu mã đã sử dụng vào localStorage
            const usedCodes = JSON.parse(localStorage.getItem('usedSpinCodes') || '[]');
            usedCodes.push(validatedCode);
            localStorage.setItem('usedSpinCodes', JSON.stringify(usedCodes));

            // Hiển thị modal kết quả sau khi quay xong (khớp với thời gian transition CSS là 5s)
            setTimeout(() => {
                isSpinning = false;
                rewardResult.innerText = reward;
                rewardModalOverlay.classList.add('active');
            }, 5000);
        });
    }

    if (rewardModalCloseBtn) {
        rewardModalCloseBtn.addEventListener('click', () => {
            rewardModalOverlay.classList.remove('active');
            // Reset trạng thái sau khi quay xong 1 mã
            spinCodeInput.disabled = false;
            btnVerifyCode.disabled = false;
            spinCodeInput.value = '';
            spinActionBox.style.display = 'none';
            validatedCode = null;
            showMessage('', '');
            btnSpin.disabled = false;
        });
    }

    function showMessage(text, type) {
        spinMessage.innerText = text;
        spinMessage.className = 'spin-msg ' + type;
    }
});
