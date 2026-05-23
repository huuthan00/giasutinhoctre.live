from __future__ import annotations

import html
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "bai-giang-cpp-nentang"


LESSONS = [
    {
        "title": "Làm quen C++ và môi trường lập trình",
        "phase": "Giai đoạn 1 - Nền tảng C++",
        "objectives": [
            "Hiểu một chương trình C++ tối thiểu gồm những phần nào.",
            "Biết tạo file, biên dịch, chạy chương trình và đọc lỗi cơ bản.",
            "In được nhiều dòng thông tin ra màn hình bằng cout.",
        ],
        "theory": [
            "C++ là ngôn ngữ biên dịch: trước khi chạy, code cần được compiler chuyển thành chương trình máy hiểu được. Vì vậy lỗi cú pháp thường xuất hiện ở bước biên dịch, còn lỗi logic xuất hiện khi chương trình chạy nhưng kết quả sai.",
            "Một chương trình cơ bản thường có #include để dùng thư viện, hàm main() là điểm bắt đầu chạy, các câu lệnh nằm trong cặp ngoặc nhọn và kết thúc bằng dấu chấm phẩy. Học viên cần tập nhìn cấu trúc trước khi sửa từng dòng.",
            "cout dùng để in dữ liệu ra console. Có thể nối nhiều phần bằng toán tử << và dùng endl hoặc ký tự \\n để xuống dòng. Việc trình bày output rõ ràng giúp kiểm tra chương trình dễ hơn.",
        ],
        "example_title": "Chương trình giới thiệu bản thân",
        "code": r'''#include <iostream>
using namespace std;

int main() {
    cout << "Xin chao, minh la An!" << endl;
    cout << "Nam nay minh 15 tuoi." << endl;
    cout << "Muc tieu: hoc C++ de tu lam san pham demo." << endl;
    return 0;
}''',
        "explanation": [
            "Dòng include cho phép dùng cout và endl.",
            "main() là nơi chương trình bắt đầu chạy.",
            "Mỗi câu lệnh cout in một dòng riêng để output dễ đọc.",
            "return 0 báo rằng chương trình kết thúc bình thường.",
        ],
        "homework": [
            "Viết chương trình in họ tên, lớp, trường, sở thích và mục tiêu học C++.",
            "Sửa chương trình để in một thời khóa biểu 5 dòng.",
            "Cố tình xóa một dấu chấm phẩy, chạy lại và ghi lại thông báo lỗi compiler.",
        ],
    },
    {
        "title": "Nhập dữ liệu, biến và kiểu dữ liệu",
        "phase": "Giai đoạn 1 - Nền tảng C++",
        "objectives": [
            "Biết khai báo biến int, double, char, string, bool.",
            "Biết dùng cin và getline để nhập dữ liệu.",
            "Hiểu biến là nơi lưu giá trị tạm trong bộ nhớ.",
        ],
        "theory": [
            "Biến giống như một hộp có tên. Kiểu dữ liệu quyết định hộp đó chứa loại giá trị nào: int cho số nguyên, double cho số thực, string cho chuỗi, bool cho đúng/sai. Đặt tên biến rõ nghĩa giúp code tự giải thích được.",
            "cin đọc dữ liệu đến khoảng trắng, phù hợp cho số hoặc một từ. Với họ tên có khoảng trắng, cần dùng getline(cin, name). Khi chuyển từ cin sang getline, có thể cần cin.ignore() để bỏ ký tự xuống dòng còn lại trong bộ đệm.",
            "Học viên cần phân biệt nhập, lưu và xử lý. Nhập là lấy dữ liệu từ bàn phím, lưu là đặt vào biến, xử lý là dùng biến để tính toán hoặc tạo output.",
        ],
        "example_title": "Nhập thông tin học viên",
        "code": r'''#include <iostream>
#include <string>
using namespace std;

int main() {
    string name;
    int age;
    double mathScore;

    cout << "Nhap ho ten: ";
    getline(cin, name);

    cout << "Nhap tuoi: ";
    cin >> age;

    cout << "Nhap diem Toan: ";
    cin >> mathScore;

    cout << "\n--- THONG TIN ---\n";
    cout << "Ho ten: " << name << endl;
    cout << "Tuoi: " << age << endl;
    cout << "Diem Toan: " << mathScore << endl;
    return 0;
}''',
        "explanation": [
            "getline đọc được cả họ tên có dấu cách.",
            "age dùng int vì tuổi là số nguyên.",
            "mathScore dùng double vì điểm có thể là 8.5.",
            "Phần output được tách bằng tiêu đề để dễ kiểm tra.",
        ],
        "homework": [
            "Viết chương trình nhập tên sản phẩm, số lượng, đơn giá và in hóa đơn đơn giản.",
            "Viết chương trình nhập chiều dài, chiều rộng và in diện tích hình chữ nhật.",
            "Thử nhập tên có khoảng trắng bằng cin, sau đó đổi sang getline và so sánh kết quả.",
        ],
    },
    {
        "title": "Toán tử số học và biểu thức",
        "phase": "Giai đoạn 1 - Nền tảng C++",
        "objectives": [
            "Dùng được các toán tử +, -, *, / trong bài toán thực tế.",
            "Phân biệt chia nguyên và chia số thực.",
            "Biết viết biểu thức tính toán rõ ràng, đúng thứ tự ưu tiên.",
        ],
        "theory": [
            "Biểu thức là sự kết hợp giữa biến, hằng và toán tử để tạo ra một giá trị mới. C++ tính nhân/chia trước cộng/trừ, nhưng khi bài toán phức tạp nên dùng ngoặc để tránh hiểu nhầm.",
            "Khi cả hai vế của phép chia là int, kết quả là chia nguyên. Ví dụ 5 / 2 cho ra 2. Muốn có 2.5, cần dùng double hoặc ép kiểu bằng 1.0 * a / b.",
            "Trong các bài toán điểm, tiền, diện tích, nên chọn double nếu kết quả có thể lẻ. Chọn đúng kiểu dữ liệu giúp tránh mất phần thập phân.",
        ],
        "example_title": "Tính điểm trung bình 3 môn",
        "code": r'''#include <iostream>
using namespace std;

int main() {
    double toan, van, anh;
    cout << "Nhap diem Toan Van Anh: ";
    cin >> toan >> van >> anh;

    double average = (toan + van + anh) / 3.0;

    cout << "Diem trung binh: " << average << endl;
    return 0;
}''',
        "explanation": [
            "Dùng double để điểm có phần thập phân.",
            "Chia cho 3.0 để chắc chắn kết quả là số thực.",
            "Biến average lưu kết quả trung gian, giúp output gọn và dễ debug.",
        ],
        "homework": [
            "Nhập bán kính, tính chu vi và diện tích hình tròn với pi = 3.14.",
            "Nhập số phút, đổi thành số giờ dạng số thực.",
            "Nhập điểm 4 bài kiểm tra, tính trung bình có trọng số: bài cuối hệ số 2.",
        ],
    },
    {
        "title": "Chia nguyên, chia dư và bài toán chẵn lẻ",
        "phase": "Giai đoạn 1 - Nền tảng C++",
        "objectives": [
            "Hiểu phép chia dư % và ứng dụng.",
            "Giải được bài toán chẵn/lẻ, chia hết, tách giờ/phút.",
            "Biết kiểm tra nhanh output bằng nhiều dữ liệu mẫu.",
        ],
        "theory": [
            "Toán tử % trả về phần dư của phép chia nguyên. Nếu n % 2 == 0 thì n là số chẵn. Nếu n % k == 0 thì n chia hết cho k. Đây là công cụ rất hay gặp trong bài toán cơ bản.",
            "Chia nguyên và chia dư thường đi cùng nhau. Ví dụ đổi 135 phút thành 2 giờ 15 phút: giờ = 135 / 60, phút còn lại = 135 % 60.",
            "Khi học thuật toán cơ bản, học viên cần tạo thói quen tự đặt test: số nhỏ, số biên, số chia hết, số không chia hết. Test tốt giúp tìm lỗi sớm.",
        ],
        "example_title": "Đổi tổng số phút thành giờ và phút",
        "code": r'''#include <iostream>
using namespace std;

int main() {
    int totalMinutes;
    cout << "Nhap tong so phut: ";
    cin >> totalMinutes;

    int hours = totalMinutes / 60;
    int minutes = totalMinutes % 60;

    cout << totalMinutes << " phut = "
         << hours << " gio " << minutes << " phut\n";
    return 0;
}''',
        "explanation": [
            "Phép / lấy số giờ tròn.",
            "Phép % lấy số phút còn lại sau khi chia thành giờ.",
            "Nên thử 59, 60, 61, 135 để kiểm tra đủ trường hợp.",
        ],
        "homework": [
            "Nhập một số nguyên, in số đó là chẵn hay lẻ.",
            "Nhập số giây, đổi thành giờ - phút - giây.",
            "Nhập a và b, kiểm tra a có chia hết cho b không. Tự xử lý trường hợp b = 0.",
        ],
    },
    {
        "title": "Rẽ nhánh if/else cơ bản",
        "phase": "Giai đoạn 1 - Nền tảng C++",
        "objectives": [
            "Viết được điều kiện so sánh bằng if/else.",
            "Hiểu luồng chạy khi điều kiện đúng hoặc sai.",
            "Giải được bài toán phân loại đơn giản.",
        ],
        "theory": [
            "Rẽ nhánh giúp chương trình ra quyết định. if kiểm tra điều kiện, nếu đúng thì chạy khối lệnh bên trong. else chạy khi điều kiện của if sai. Điều kiện luôn cho kết quả true hoặc false.",
            "Các toán tử so sánh thường dùng gồm >, <, >=, <=, == và !=. Cần phân biệt = là gán giá trị, còn == là so sánh bằng.",
            "Khi viết điều kiện, nên đọc thành câu tiếng Việt. Ví dụ score >= 5 nghĩa là 'điểm lớn hơn hoặc bằng 5'. Cách này giúp học viên tự kiểm tra logic trước khi chạy.",
        ],
        "example_title": "Kiểm tra qua môn",
        "code": r'''#include <iostream>
using namespace std;

int main() {
    double score;
    cout << "Nhap diem: ";
    cin >> score;

    if (score >= 5.0) {
        cout << "Ket qua: Qua mon\n";
    } else {
        cout << "Ket qua: Can hoc lai\n";
    }

    return 0;
}''',
        "explanation": [
            "Nếu score từ 5.0 trở lên, chương trình in qua môn.",
            "Nếu không, khối else được chạy.",
            "Nên thử 4.9, 5.0, 8.0 để kiểm tra ranh giới.",
        ],
        "homework": [
            "Nhập tuổi, kiểm tra đủ 15 tuổi để tham gia khóa nâng cao hay chưa.",
            "Nhập nhiệt độ, nếu trên 37.5 thì in 'Can theo doi suc khoe'.",
            "Nhập số tiền mua hàng, nếu từ 500000 trở lên thì giảm 10%.",
        ],
    },
    {
        "title": "else-if, switch và điều kiện nhiều nhánh",
        "phase": "Giai đoạn 1 - Nền tảng C++",
        "objectives": [
            "Dùng được else-if cho nhiều mức phân loại.",
            "Dùng switch cho menu hoặc lựa chọn rời rạc.",
            "Biết sắp xếp điều kiện từ cụ thể đến tổng quát.",
        ],
        "theory": [
            "else-if dùng khi có nhiều khả năng nhưng chỉ chọn một. Chương trình kiểm tra từ trên xuống; gặp điều kiện đúng đầu tiên thì chạy và bỏ qua phần còn lại.",
            "switch phù hợp khi so sánh một biến nguyên hoặc ký tự với nhiều giá trị cố định. Mỗi case cần break để tránh chạy tiếp sang case sau.",
            "Với bài xếp loại, thứ tự điều kiện rất quan trọng. Nếu kiểm tra score >= 5 trước score >= 8, điểm 9 sẽ bị xếp vào mức trung bình. Vì vậy thường kiểm tra từ mức cao xuống thấp.",
        ],
        "example_title": "Xếp loại học lực",
        "code": r'''#include <iostream>
using namespace std;

int main() {
    double score;
    cout << "Nhap diem trung binh: ";
    cin >> score;

    if (score >= 8.0) {
        cout << "Xep loai: Gioi\n";
    } else if (score >= 6.5) {
        cout << "Xep loai: Kha\n";
    } else if (score >= 5.0) {
        cout << "Xep loai: Trung binh\n";
    } else {
        cout << "Xep loai: Can co gang\n";
    }

    return 0;
}''',
        "explanation": [
            "Các mức điểm được kiểm tra từ cao xuống thấp.",
            "Điểm 7.0 không đạt điều kiện >= 8.0 nhưng đạt >= 6.5.",
            "else cuối cùng xử lý mọi trường hợp còn lại.",
        ],
        "homework": [
            "Viết menu chọn 1-4: cộng, trừ, nhân, chia hai số.",
            "Nhập tháng, in số ngày tương ứng, tạm bỏ qua năm nhuận.",
            "Nhập điểm và in cả xếp loại lẫn lời nhận xét ngắn.",
        ],
    },
    {
        "title": "Vòng lặp for và bài toán lặp biết trước số lần",
        "phase": "Giai đoạn 1 - Nền tảng C++",
        "objectives": [
            "Hiểu biến đếm, điều kiện dừng và bước tăng trong for.",
            "Dùng for để tính tổng, in dãy số, in bảng cửu chương.",
            "Biết tránh lỗi chạy thiếu hoặc thừa một lần.",
        ],
        "theory": [
            "Vòng lặp for phù hợp khi biết trước số lần lặp. Cấu trúc gồm khởi tạo, điều kiện tiếp tục và cập nhật. Mỗi phần cần rõ ràng để tránh vòng lặp vô hạn.",
            "Biến đếm thường bắt đầu từ 0 hoặc 1. Nếu duyệt n phần tử mảng thì thường dùng 0 đến n - 1. Nếu in số tự nhiên từ 1 đến n thì dùng 1 đến n.",
            "Khi tính tổng, cần khởi tạo sum = 0 trước vòng lặp. Nếu quên khởi tạo, biến có thể chứa giá trị rác và kết quả sai.",
        ],
        "example_title": "In bảng cửu chương",
        "code": r'''#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "Nhap so can in bang cuu chuong: ";
    cin >> n;

    for (int i = 1; i <= 10; i++) {
        cout << n << " x " << i << " = " << n * i << endl;
    }

    return 0;
}''',
        "explanation": [
            "i chạy từ 1 đến 10 nên vòng lặp chạy đúng 10 lần.",
            "Mỗi lần lặp in một phép nhân.",
            "Biểu thức n * i được tính lại theo giá trị i hiện tại.",
        ],
        "homework": [
            "Nhập n, tính tổng từ 1 đến n.",
            "Nhập n, in các số chẵn từ 2 đến n.",
            "In hình tam giác sao có n dòng.",
        ],
    },
    {
        "title": "while, do-while và lặp chưa biết trước số lần",
        "phase": "Giai đoạn 1 - Nền tảng C++",
        "objectives": [
            "Phân biệt for, while và do-while.",
            "Dùng while để nhập đến khi gặp điều kiện dừng.",
            "Dùng break/continue đúng tình huống.",
        ],
        "theory": [
            "while phù hợp khi chưa biết trước số lần lặp. Chương trình tiếp tục lặp khi điều kiện còn đúng. Điều kiện cần thay đổi bên trong vòng lặp, nếu không chương trình có thể lặp vô hạn.",
            "do-while chạy thân vòng lặp ít nhất một lần rồi mới kiểm tra điều kiện. Kiểu này phù hợp cho menu vì người dùng cần thấy menu trước khi chọn thoát.",
            "break thoát khỏi vòng lặp ngay lập tức. continue bỏ qua phần còn lại của lần lặp hiện tại và chuyển sang lần tiếp theo. Hai lệnh này cần dùng tiết chế để code vẫn dễ đọc.",
        ],
        "example_title": "Nhập số đến khi gặp 0",
        "code": r'''#include <iostream>
using namespace std;

int main() {
    int x;
    int sum = 0;

    cout << "Nhap cac so nguyen, nhap 0 de dung:\n";
    while (true) {
        cin >> x;
        if (x == 0) {
            break;
        }
        sum += x;
    }

    cout << "Tong cac so da nhap: " << sum << endl;
    return 0;
}''',
        "explanation": [
            "while(true) tạo vòng lặp liên tục.",
            "Khi người dùng nhập 0, break dừng vòng lặp.",
            "Các số khác 0 được cộng vào sum.",
        ],
        "homework": [
            "Viết chương trình nhập mật khẩu đến khi đúng.",
            "Nhập các điểm số đến khi nhập -1, in điểm trung bình.",
            "Viết menu do-while gồm 1. Xin chào, 2. Tính bình phương, 0. Thoát.",
        ],
    },
    {
        "title": "Mảng một chiều",
        "phase": "Giai đoạn 1 - Nền tảng C++",
        "objectives": [
            "Khai báo, nhập và in mảng một chiều.",
            "Duyệt mảng bằng chỉ số từ 0 đến n - 1.",
            "Tính tổng, trung bình, max/min và đếm theo điều kiện.",
        ],
        "theory": [
            "Mảng dùng để lưu nhiều giá trị cùng kiểu dưới một tên chung. Mỗi phần tử có chỉ số, bắt đầu từ 0. Với n phần tử, chỉ số hợp lệ là 0 đến n - 1.",
            "Lỗi phổ biến nhất là truy cập sai chỉ số, ví dụ a[n]. Đây là vị trí ngoài mảng. Học viên cần đọc vòng lặp cẩn thận và luôn hỏi: chỉ số cuối cùng có hợp lệ không?",
            "Các thao tác cơ bản trên mảng gồm duyệt, cộng dồn, tìm giá trị lớn nhất/nhỏ nhất và đếm phần tử thỏa điều kiện. Đây là nền tảng cho xử lý danh sách sau này.",
        ],
        "example_title": "Thống kê điểm trong mảng",
        "code": r'''#include <iostream>
using namespace std;

int main() {
    int n;
    double scores[100];
    cout << "Nhap so hoc sinh: ";
    cin >> n;

    for (int i = 0; i < n; i++) {
        cout << "Diem hoc sinh " << i + 1 << ": ";
        cin >> scores[i];
    }

    double sum = 0;
    double maxScore = scores[0];
    for (int i = 0; i < n; i++) {
        sum += scores[i];
        if (scores[i] > maxScore) maxScore = scores[i];
    }

    cout << "Diem trung binh: " << sum / n << endl;
    cout << "Diem cao nhat: " << maxScore << endl;
    return 0;
}''',
        "explanation": [
            "Mảng scores lưu tối đa 100 điểm.",
            "Vòng lặp nhập dùng i từ 0 đến n - 1.",
            "maxScore khởi tạo bằng phần tử đầu tiên để so sánh hợp lý.",
        ],
        "homework": [
            "Nhập n số nguyên, đếm có bao nhiêu số chẵn.",
            "Nhập n điểm, in vị trí các điểm dưới 5.",
            "Nhập n số, tìm số nhỏ nhất và số lớn nhất.",
        ],
    },
    {
        "title": "Hàm cơ bản và mini game đoán số",
        "phase": "Giai đoạn 1 - Nền tảng C++",
        "objectives": [
            "Biết viết hàm có tham số và giá trị trả về.",
            "Tách chương trình thành các phần nhỏ dễ kiểm tra.",
            "Hoàn thành mini game đoán số bằng vòng lặp và điều kiện.",
        ],
        "theory": [
            "Hàm giúp gom một công việc có tên riêng. Thay vì viết mọi thứ trong main, ta tách thành hàm để code dễ đọc, dễ sửa và dễ tái sử dụng.",
            "Một hàm có thể nhận tham số và trả về kết quả. Ví dụ int square(int x) nhận x và trả về x * x. Nếu hàm chỉ in ra màn hình và không trả kết quả, dùng void.",
            "Khi làm game đoán số, cần xác định trạng thái: số bí mật, số người chơi đoán, số lượt đoán. Vòng lặp chạy đến khi đoán đúng hoặc hết lượt.",
        ],
        "example_title": "Hàm kiểm tra đoán đúng",
        "code": r'''#include <iostream>
using namespace std;

bool isCorrect(int guess, int secret) {
    return guess == secret;
}

void printHint(int guess, int secret) {
    if (guess < secret) {
        cout << "Can doan lon hon!\n";
    } else if (guess > secret) {
        cout << "Can doan nho hon!\n";
    }
}

int main() {
    int secret = 37;
    int guess;

    do {
        cout << "Nhap so ban doan: ";
        cin >> guess;
        if (!isCorrect(guess, secret)) {
            printHint(guess, secret);
        }
    } while (!isCorrect(guess, secret));

    cout << "Chuc mung! Ban da doan dung.\n";
    return 0;
}''',
        "explanation": [
            "isCorrect trả về true/false, giúp điều kiện trong main dễ đọc.",
            "printHint chỉ in gợi ý nên dùng void.",
            "secret đang cố định để dễ test; buổi sau có thể thêm random.",
        ],
        "homework": [
            "Thêm biến đếm số lượt đoán vào game.",
            "Viết hàm bool isEven(int n) và dùng trong chương trình nhập mảng.",
            "Viết hàm double average(double a[], int n) để tính trung bình mảng điểm.",
        ],
    },
]


MORE_LESSONS = [
    ("Mảng hai chiều và ma trận", "Mảng hai chiều lưu dữ liệu dạng bảng. Học viên cần nắm dòng, cột, chỉ số và cách duyệt lồng nhau.", "Nhập bảng điểm 3 học sinh x 4 môn, tính tổng từng học sinh.", ["Tạo ma trận 3x3 và in đường chéo chính.", "Tính tổng từng cột của ma trận.", "Tìm giá trị lớn nhất trong ma trận."]),
    ("Vector và danh sách linh hoạt", "vector phù hợp khi số lượng phần tử có thể thay đổi. Các thao tác quan trọng là push_back, size, truy cập bằng chỉ số và duyệt.", "Quản lý danh sách điểm bằng vector<double>, thêm điểm và tính trung bình.", ["Nhập danh sách tên bằng vector<string>.", "Thêm điểm đến khi nhập -1 rồi tính trung bình.", "Tìm điểm cao nhất trong vector."]),
    ("Sắp xếp nổi bọt và chọn trực tiếp", "Sắp xếp giúp đưa dữ liệu về thứ tự tăng hoặc giảm. Học viên cần hiểu ý tưởng đổi chỗ và số vòng lặp trước khi dùng thư viện.", "Cài đặt Bubble Sort cho mảng điểm và in sau mỗi lượt đổi.", ["Viết Selection Sort tăng dần.", "Sửa Bubble Sort thành giảm dần.", "Ghi lại từng bước sắp xếp mảng {5, 2, 9, 1}."]),
    ("Tìm kiếm tuyến tính và bảng xếp hạng", "Tìm kiếm tuyến tính duyệt từng phần tử, phù hợp với danh sách nhỏ hoặc chưa sắp xếp. Đây là cách tìm dễ hiểu nhất.", "Tìm học sinh theo tên trong danh sách vector<string>.", ["Tìm tất cả tên chứa chữ 'an'.", "Tìm vị trí điểm đầu tiên dưới 5.", "Kết hợp sort và tìm kiếm trong danh sách điểm."]),
    ("String cơ bản và nhập chuỗi", "string là kiểu dữ liệu lưu văn bản. Cần phân biệt cin và getline, chỉ số ký tự, length và duyệt từng ký tự.", "Nhập họ tên, in số ký tự và từng ký tự trên một dòng.", ["Đếm số khoảng trắng trong họ tên.", "In chữ cái đầu tiên và cuối cùng.", "Nhập câu và đếm số ký tự không phải khoảng trắng."]),
    ("Xử lý chuỗi và Caesar Cipher", "Các thao tác chuỗi như find, substr, toupper, tolower giúp xử lý văn bản. Caesar Cipher là ví dụ tốt để luyện duyệt từng ký tự.", "Mã hóa chuỗi bằng cách dịch mỗi chữ cái thêm 3 vị trí.", ["Viết chương trình đảo ngược chuỗi.", "Kiểm tra chuỗi palindrome đơn giản.", "Mã hóa Caesar với bước dịch do người dùng nhập."]),
    ("Hàm nâng cao và tách chương trình", "Tách hàm là kỹ năng quan trọng để chương trình không bị rối. Mỗi hàm nên làm một việc rõ ràng và có tên mô tả đúng việc đó.", "Tách chương trình tính điểm thành inputScore, averageScore, printResult.", ["Tách mini game đoán số thành ít nhất 3 hàm.", "Viết hàm findMax cho vector<double>.", "Viết hàm printMenu và dùng trong chương trình menu."]),
    ("Kiểm thử hàm và menu console", "Sau khi tách hàm, cần kiểm thử từng hàm bằng dữ liệu mẫu. Menu console giúp người dùng chọn chức năng lặp lại nhiều lần.", "Xây menu 1. Thêm điểm 2. Xem trung bình 0. Thoát.", ["Thêm chức năng xóa toàn bộ điểm.", "Thêm kiểm tra lựa chọn menu không hợp lệ.", "Ghi 5 test case cho hàm averageScore."]),
    ("Tham chiếu và truyền tham số", "Truyền tham trị tạo bản sao, truyền tham chiếu cho phép hàm thay đổi biến gốc. Đây là nền tảng để viết hàm xử lý dữ liệu gọn hơn.", "Viết hàm swapValues(int &a, int &b) và so sánh với truyền tham trị.", ["Viết hàm tăng điểm thưởng cho một biến score.", "Viết hàm nhập hai số bằng tham chiếu.", "Giải thích bằng lời vì sao swap truyền tham trị không đổi biến gốc."]),
    ("Bộ nhớ nhập môn và xử lý vector trong hàm", "Học viên chỉ cần hiểu trực quan rằng biến nằm trong bộ nhớ và tham chiếu giúp tránh copy không cần thiết. Với vector, nên truyền const reference khi chỉ đọc.", "Viết hàm printScores(const vector<double>& scores) và addBonus(vector<double>& scores).", ["Viết hàm tìm điểm cao nhất nhận const vector<double>&.", "Viết hàm cộng 0.5 điểm cho mọi phần tử.", "So sánh khi nào dùng const reference và khi nào dùng reference thường."]),
    ("Struct cơ bản", "struct giúp gom nhiều thông tin liên quan thành một kiểu dữ liệu mới. Ví dụ Student gồm name, age, score.", "Tạo struct Student và in thông tin một học sinh.", ["Tạo struct Product gồm id, name, price.", "Nhập 3 học sinh và in bảng.", "Viết hàm printStudent(Student s)."]),
    ("File I/O và ôn tập giai đoạn 2", "File giúp lưu dữ liệu sau khi chương trình kết thúc. Học viên cần biết ghi file bằng ofstream và đọc file bằng ifstream ở mức cơ bản.", "Ghi danh sách học sinh ra file students.txt rồi đọc lại.", ["Ghi 5 số nguyên ra file.", "Đọc danh sách điểm từ file và tính trung bình.", "Hoàn thiện chương trình quản lý học sinh có lưu file."]),
    ("Thiết kế dữ liệu dạng danh sách", "Trước khi code app quản lý, cần thiết kế dữ liệu: mỗi bản ghi có trường nào, dùng vector<struct> ra sao, chức năng chính là gì.", "Thiết kế vector<Student> với menu thêm, xem danh sách.", ["Vẽ bảng dữ liệu cho app quản lý kho.", "Viết struct Item gồm id, name, quantity, price.", "Tạo menu 4 lựa chọn cho app quản lý."]),
    ("Thêm, sửa, xóa phần tử trong danh sách", "CRUD là nhóm thao tác phổ biến: Create, Read, Update, Delete. Trong console app, mỗi thao tác nên là một hàm riêng.", "Thêm sản phẩm vào vector, sửa số lượng, xóa theo id.", ["Viết hàm removeStudentById.", "Viết hàm updateScoreById.", "Xử lý trường hợp id không tồn tại."]),
    ("Tìm kiếm tuyến tính theo mã và tên", "Linear Search phù hợp khi dữ liệu chưa sắp xếp. Có thể tìm chính xác theo mã hoặc tìm gần đúng theo một phần tên.", "Tìm sản phẩm theo id và tìm sản phẩm có tên chứa từ khóa.", ["Tìm học sinh theo tên.", "Tìm tất cả sản phẩm số lượng dưới 5.", "In thông báo rõ khi không tìm thấy."]),
    ("Tìm min, max và lọc dữ liệu", "Ngoài tìm một giá trị, chương trình quản lý thường cần lọc và thống kê: điểm cao nhất, giá thấp nhất, số lượng tồn kho thấp.", "Tìm học sinh điểm cao nhất và lọc học sinh đạt từ 8 trở lên.", ["Tìm sản phẩm đắt nhất.", "Lọc sản phẩm còn dưới 10 cái.", "Đếm số học sinh qua môn."]),
    ("Bubble Sort chi tiết", "Bubble Sort dễ hiểu vì liên tục so sánh hai phần tử liền kề và đổi chỗ nếu sai thứ tự. Tuy không tối ưu, nó giúp học viên hiểu bản chất sắp xếp.", "Sắp xếp mảng điểm tăng dần bằng Bubble Sort.", ["In mảng sau mỗi vòng lặp ngoài.", "Đổi thành sắp xếp giảm dần.", "Đếm số lần đổi chỗ."]),
    ("Selection Sort và Insertion Sort", "Selection Sort chọn phần tử nhỏ nhất đưa về đầu. Insertion Sort chèn phần tử vào đoạn đã sắp xếp. Hai thuật toán giúp học viên so sánh nhiều cách nghĩ.", "Cài đặt Selection Sort cho danh sách giá sản phẩm.", ["Cài đặt Insertion Sort.", "So sánh số bước của 3 thuật toán với mảng 5 phần tử.", "Sắp xếp danh sách tên theo alphabet."]),
    ("Binary Search", "Binary Search chỉ dùng khi danh sách đã sắp xếp. Mỗi bước bỏ đi một nửa phạm vi tìm kiếm, vì vậy nhanh hơn tìm tuyến tính với dữ liệu lớn.", "Tìm một điểm trong mảng đã sắp xếp tăng dần.", ["Viết binary search trả về vị trí hoặc -1.", "Test với phần tử đầu, giữa, cuối và không tồn tại.", "Giải thích vì sao cần sắp xếp trước khi binary search."]),
    ("std::sort và comparator", "Sau khi hiểu thuật toán cơ bản, học viên cần biết dùng thư viện chuẩn. std::sort nhanh, đáng tin cậy và có thể sắp xếp struct bằng comparator.", "Sắp xếp vector<Student> theo điểm giảm dần bằng comparator.", ["Sắp xếp sản phẩm theo giá tăng dần.", "Nếu bằng điểm, sắp xếp theo tên.", "Viết comparator riêng cho tuổi giảm dần."]),
    ("Lọc dữ liệu và thống kê", "Ứng dụng thực tế không chỉ tìm và sắp xếp mà còn lọc theo điều kiện và thống kê. Đây là cầu nối từ thuật toán cơ bản sang sản phẩm demo.", "Lọc sản phẩm tồn kho thấp và tính tổng giá trị kho.", ["Lọc học sinh điểm từ 8 trở lên.", "Tính điểm trung bình của nhóm đã lọc.", "In báo cáo thống kê rõ ràng."]),
    ("Sắp xếp nhiều tiêu chí", "Khi dữ liệu có nhiều trường, có thể cần sắp xếp theo tiêu chí phụ. Ví dụ điểm giảm dần, nếu bằng điểm thì tên tăng dần.", "Sắp xếp danh sách học sinh theo điểm giảm dần, tên tăng dần.", ["Sắp xếp sản phẩm theo số lượng tăng, nếu bằng thì giá giảm.", "Viết menu chọn tiêu chí sắp xếp.", "Thêm tiêu đề bảng khi in kết quả."]),
    ("Tích hợp mini app quản lý", "Buổi này ghép các phần đã học thành app nhỏ: vector<struct>, thêm, xem, tìm, sắp xếp, lọc. Mục tiêu là code chạy ổn và dễ giải thích.", "Mini app quản lý kho gồm thêm, xem, tìm theo tên, sắp xếp theo giá.", ["Hoàn thiện chức năng xóa.", "Thêm kiểm tra dữ liệu nhập âm.", "Chuẩn bị 10 dữ liệu mẫu để test."]),
    ("Ôn tập và sửa lỗi logic", "Trước khi làm dự án cuối khóa, học viên cần biết đọc lỗi, chia lỗi thành lỗi biên dịch, lỗi runtime và lỗi logic. Cách sửa tốt là tái hiện lỗi bằng test nhỏ.", "Debug một chương trình sắp xếp sai thứ tự và tìm nguyên nhân.", ["Tạo checklist test cho app quản lý.", "Sửa 3 lỗi cố ý trong code mẫu.", "Viết lại phần menu cho gọn hơn."]),
    ("Chọn đề tài dự án cuối khóa", "Dự án tốt là dự án vừa sức, có người dùng rõ, có luồng demo rõ và dùng lại kiến thức đã học. Không cần lớn, nhưng phải chạy ổn.", "So sánh 3 đề tài: todo app, quản lý kho, game caro đơn giản; chọn đề tài phù hợp.", ["Viết mô tả dự án 5-7 dòng.", "Liệt kê tối thiểu 5 chức năng.", "Vẽ luồng menu chính của dự án."]),
    ("Thiết kế tính năng và cấu trúc file code", "Trước khi code nhiều, cần chia chức năng thành hàm và xác định dữ liệu chính. Đây là bước giúp tránh code rối ở cuối khóa.", "Thiết kế struct, vector dữ liệu và danh sách hàm cho dự án.", ["Viết skeleton code có menu và hàm rỗng.", "Xác định dữ liệu mẫu để demo.", "Chọn 3 chức năng bắt buộc phải hoàn thành trước."]),
    ("Xây chức năng chính của sản phẩm", "Ưu tiên làm luồng chính chạy được trước: thêm dữ liệu, xem dữ liệu, tìm kiếm hoặc thao tác chính. Chưa cần làm đẹp nếu logic chưa ổn.", "Cài đặt 2-3 chức năng lõi của dự án đã chọn.", ["Hoàn thiện chức năng thêm.", "Hoàn thiện chức năng xem danh sách.", "Ghi lại lỗi gặp phải và cách sửa."]),
    ("Kiểm tra dữ liệu nhập và làm đẹp output", "Sản phẩm demo cần chịu được nhập sai cơ bản. Output cần có tiêu đề, khoảng cách và thông báo rõ ràng để người xem hiểu chương trình đang làm gì.", "Thêm kiểm tra số âm, lựa chọn menu sai và bảng in danh sách đẹp.", ["Thêm validate cho mọi input quan trọng.", "Chuẩn bị dữ liệu mẫu dùng khi demo.", "Viết hướng dẫn sử dụng 5 dòng trong chương trình."]),
    ("Chuẩn bị kịch bản demo", "Demo tốt không phải bấm ngẫu nhiên. Học viên cần chuẩn bị thứ tự thao tác để chứng minh sản phẩm có giá trị và chạy ổn.", "Viết kịch bản demo 5 phút: giới thiệu, thêm dữ liệu, tìm kiếm, sắp xếp, kết luận.", ["Viết script nói khi demo.", "Chuẩn bị 3 câu hỏi phản biện có thể gặp.", "Tự chạy demo ít nhất 3 lần và ghi lỗi."]),
    ("Bảo vệ sản phẩm cuối khóa", "Buổi cuối tập trung vào trình bày, giải thích code và phản hồi câu hỏi. Mục tiêu không phải sản phẩm quá lớn, mà là học viên chứng minh mình hiểu code và tự làm được.", "Demo sản phẩm, giải thích struct, vector, hàm tìm kiếm/sắp xếp đã dùng.", ["Viết nhật ký học tập: 3 điều đã học được.", "Liệt kê 3 hướng cải tiến sản phẩm.", "Nộp file code cuối cùng và ảnh chụp màn hình demo."]),
]


def code_for_more(index: int, title: str) -> str:
    snippets = {
        11: r'''#include <iostream>
using namespace std;

int main() {
    int scores[3][4] = {
        {8, 7, 9, 6},
        {6, 8, 7, 9},
        {9, 9, 8, 10}
    };

    for (int row = 0; row < 3; row++) {
        int total = 0;
        for (int col = 0; col < 4; col++) {
            total += scores[row][col];
        }
        cout << "Tong diem hoc sinh " << row + 1 << ": " << total << endl;
    }
    return 0;
}''',
        12: r'''#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<double> scores;
    double x;
    while (true) {
        cout << "Nhap diem (-1 de dung): ";
        cin >> x;
        if (x == -1) break;
        scores.push_back(x);
    }

    double sum = 0;
    for (double score : scores) sum += score;
    cout << "So diem da nhap: " << scores.size() << endl;
    cout << "Trung binh: " << sum / scores.size() << endl;
    return 0;
}''',
        13: r'''for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < n - 1 - i; j++) {
        if (a[j] > a[j + 1]) {
            int temp = a[j];
            a[j] = a[j + 1];
            a[j + 1] = temp;
        }
    }
}''',
        14: r'''int findName(vector<string> names, string keyword) {
    for (int i = 0; i < names.size(); i++) {
        if (names[i] == keyword) {
            return i;
        }
    }
    return -1;
}''',
        15: r'''string fullName;
cout << "Nhap ho ten: ";
getline(cin, fullName);

cout << "So ky tu: " << fullName.length() << endl;
for (int i = 0; i < fullName.length(); i++) {
    cout << i << ": " << fullName[i] << endl;
}''',
        16: r'''string text = "ABCXYZ";
int shift = 3;

for (char &c : text) {
    if (c >= 'A' && c <= 'Z') {
        c = char((c - 'A' + shift) % 26 + 'A');
    }
}
cout << text << endl;''',
        17: r'''double averageScore(vector<double> scores) {
    double sum = 0;
    for (double score : scores) sum += score;
    return sum / scores.size();
}''',
        18: r'''void printMenu() {
    cout << "1. Them diem\n";
    cout << "2. Xem trung binh\n";
    cout << "0. Thoat\n";
}''',
        19: r'''void swapValues(int &a, int &b) {
    int temp = a;
    a = b;
    b = temp;
}''',
        20: r'''void addBonus(vector<double> &scores, double bonus) {
    for (double &score : scores) {
        score += bonus;
        if (score > 10) score = 10;
    }
}''',
        21: r'''struct Student {
    string id;
    string name;
    double score;
};

void printStudent(Student s) {
    cout << s.id << " - " << s.name << " - " << s.score << endl;
}''',
        22: r'''ofstream out("students.txt");
for (Student s : students) {
    out << s.id << ";" << s.name << ";" << s.score << endl;
}
out.close();''',
    }
    if index in snippets:
        return snippets[index]
    if 23 <= index <= 34:
        return r'''struct Item {
    string id;
    string name;
    int quantity;
    double price;
};

void printItem(Item item) {
    cout << item.id << " | " << item.name
         << " | SL: " << item.quantity
         << " | Gia: " << item.price << endl;
}'''
    if 35 <= index <= 40:
        return r'''// Skeleton du an cuoi khoa
struct Task {
    int id;
    string title;
    bool done;
};

void showMenu() {
    cout << "1. Them viec\n";
    cout << "2. Xem danh sach\n";
    cout << "3. Tim kiem\n";
    cout << "0. Thoat\n";
}'''
    return r'''cout << "Vi du se duoc giao vien mo rong trong buoi hoc." << endl;'''


for i, (title, theory, example, homework) in enumerate(MORE_LESSONS, start=11):
    LESSONS.append(
        {
            "title": title,
            "phase": (
                "Giai đoạn 2 - Cấu trúc dữ liệu cơ bản" if i <= 22
                else "Giai đoạn 3 - Tìm kiếm, sắp xếp, xử lý danh sách" if i <= 34
                else "Giai đoạn 4 - Dự án demo và bảo vệ sản phẩm"
            ),
            "objectives": [
                f"Nắm chắc trọng tâm của buổi: {title.lower()}.",
                "Biết giải thích lại ý tưởng bằng lời trước khi code.",
                "Áp dụng nội dung buổi học vào một chương trình console nhỏ.",
            ],
            "theory": [
                theory,
                "Khi học phần này, học viên cần làm theo thứ tự: hiểu dữ liệu đang có, xác định thao tác cần làm, viết thuật toán bằng lời, sau đó mới chuyển thành code. Cách học này giúp tránh tình trạng chép code mà không hiểu.",
                "Mỗi ví dụ cần được chạy với ít nhất ba bộ dữ liệu: trường hợp bình thường, trường hợp biên và trường hợp dễ gây lỗi. Sau khi chương trình chạy đúng, học viên phải giải thích được từng biến chính dùng để làm gì.",
            ],
            "example_title": example,
            "code": code_for_more(i, title),
            "explanation": [
                "Đọc yêu cầu bài toán và xác định dữ liệu đầu vào.",
                "Chia chương trình thành các bước nhỏ trước khi viết code.",
                "Chạy thử với dữ liệu mẫu và sửa lỗi nếu output chưa đúng.",
                "Nói lại bằng lời vì sao chương trình cho ra kết quả đó.",
            ],
            "homework": homework,
        }
    )


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


STYLE = """
:root {
  --bg: #0b1020;
  --panel: #111827;
  --panel-2: #162033;
  --border: rgba(255,255,255,.1);
  --text: #eef2ff;
  --muted: #9ca3af;
  --primary: #06b6d4;
  --accent: #22c55e;
  --warn: #f59e0b;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Inter, Arial, sans-serif;
  background: radial-gradient(circle at top left, rgba(6,182,212,.12), transparent 35%), var(--bg);
  color: var(--text);
  line-height: 1.65;
}
a { color: inherit; text-decoration: none; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 32px 20px 56px; }
.topbar { display: flex; justify-content: space-between; gap: 16px; align-items: center; margin-bottom: 30px; }
.brand { font-weight: 800; color: var(--primary); }
.nav a { color: var(--muted); margin-left: 14px; font-size: 14px; }
.hero { background: linear-gradient(135deg, rgba(6,182,212,.12), rgba(99,102,241,.08)); border: 1px solid var(--border); border-radius: 18px; padding: 34px; margin-bottom: 24px; }
.badge { display: inline-flex; color: var(--primary); border: 1px solid rgba(6,182,212,.3); background: rgba(6,182,212,.08); border-radius: 999px; padding: 5px 12px; font-size: 13px; font-weight: 700; }
h1 { font-size: clamp(30px, 5vw, 48px); line-height: 1.12; margin: 18px 0 12px; }
h2 { font-size: 24px; margin: 0 0 14px; }
h3 { margin: 18px 0 8px; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 20px; }
.card, section { background: rgba(17,24,39,.82); border: 1px solid var(--border); border-radius: 16px; padding: 22px; margin-bottom: 18px; }
.card strong { color: var(--accent); display: block; margin-bottom: 6px; }
.two-col { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.mini-card { background: rgba(255,255,255,.04); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }
.mini-card h3 { margin-top: 0; color: var(--primary); font-size: 17px; }
.concept-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; margin-top: 14px; }
.concept { background: rgba(255,255,255,.04); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }
.concept strong { color: var(--primary); display: block; margin-bottom: 6px; }
.concept-detail { background: rgba(255,255,255,.035); border: 1px solid var(--border); border-radius: 14px; padding: 16px; margin-top: 14px; }
.concept-detail h4 { margin: 0 0 8px; color: var(--primary); font-size: 18px; }
.quick-table td:nth-child(2) { color: #bae6fd; font-family: Consolas, 'Courier New', monospace; }
.teacher-note { border-left: 3px solid var(--warn); background: rgba(245,158,11,.08); padding: 12px 14px; border-radius: 10px; margin-top: 12px; color: var(--text); }
.timeline { list-style: none; padding-left: 0; }
.timeline li { display: grid; grid-template-columns: 120px 1fr; gap: 14px; padding: 12px 0; border-bottom: 1px solid var(--border); }
.time { color: var(--warn); font-weight: 800; }
.example-block { border: 1px solid var(--border); border-radius: 14px; padding: 18px; background: rgba(255,255,255,.035); margin-top: 16px; }
.example-block h3 { margin-top: 0; color: var(--accent); }
.example-meta { margin: 10px 0 14px; }
.example-meta th { width: 120px; }
.example-explain { background: rgba(6,182,212,.06); border: 1px solid rgba(6,182,212,.18); border-radius: 12px; padding: 12px 16px; }
.practice-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.practice { background: rgba(255,255,255,.04); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }
.practice strong { color: var(--accent); display: block; margin-bottom: 6px; }
.checklist li { list-style: square; }
ul, ol { padding-left: 22px; }
li { margin-bottom: 8px; }
.theory li { margin-bottom: 14px; }
pre { background: #050816; border: 1px solid var(--border); border-radius: 14px; padding: 18px; overflow-x: auto; }
code { color: #bae6fd; font-family: Consolas, 'Courier New', monospace; }
.homework li { background: rgba(255,255,255,.04); border: 1px solid var(--border); border-radius: 10px; padding: 10px 12px; }
.pager { display: flex; justify-content: space-between; gap: 12px; margin-top: 24px; }
.pager a { padding: 10px 14px; border: 1px solid var(--border); border-radius: 10px; color: var(--text); background: rgba(255,255,255,.04); }
.note { color: var(--muted); }
table { width: 100%; border-collapse: collapse; }
th, td { border-bottom: 1px solid var(--border); padding: 12px; text-align: left; }
th { color: var(--primary); }
@media (max-width: 760px) {
  .grid, .two-col, .concept-grid, .practice-grid { grid-template-columns: 1fr; }
  .timeline li { grid-template-columns: 1fr; }
  .topbar, .pager { flex-direction: column; align-items: stretch; }
  .hero { padding: 24px; }
}
"""


def lesson_filename(index: int, title: str) -> str:
    return f"buoi-{index:02d}-{slugify(title)}.html"


def render_timeline(index: int, lesson: dict) -> str:
    title = html.escape(lesson["title"].lower())
    rows = [
        ("0-10 phút", "Khởi động: hỏi lại bài trước, xem nhanh bài tập về nhà, nêu mục tiêu buổi học bằng một ví dụ gần gũi."),
        ("10-30 phút", f"Lý thuyết trọng tâm: giải thích {title}, ghi công thức/mẫu code cần nhớ và chỉ ra lỗi thường gặp."),
        ("30-55 phút", "Live coding: giáo viên viết ví dụ từng bước, học viên dự đoán output trước khi chạy và sửa lỗi nhỏ ngay trên code."),
        ("55-75 phút", "Thực hành trên lớp: học viên làm bài mức 1 và mức 2, giáo viên quan sát cách nghĩ thay vì chỉ nhìn đáp án."),
        ("75-85 phút", "Review: chọn 1-2 lỗi phổ biến để sửa chung, yêu cầu học viên giải thích lại bằng lời."),
        ("85-90 phút", "Chốt buổi: nhắc lại 3 ý chính, giao bài về nhà và tiêu chí nộp bài."),
    ]
    return "".join(f'<li><span class="time">{time}</span><span>{text}</span></li>' for time, text in rows)


def quick_illustrations(index: int, lesson: dict) -> list[tuple[str, str, str, str]]:
    if index == 4:
        return [
            ("Chia nguyên", "17 / 5", "3", "Lấy số lần 5 đi trọn vẹn trong 17, bỏ phần dư."),
            ("Chia dư", "17 % 5", "2", "Sau khi lấy 5 * 3 = 15, còn lại 2."),
            ("Chẵn lẻ", "8 % 2 == 0", "true", "Số chia hết cho 2 là số chẵn."),
            ("Không chia hết", "10 % 3", "1", "Dư 1 nên 10 không chia hết cho 3."),
            ("Đổi phút", "135 / 60 và 135 % 60", "2 giờ 15 phút", "Chia nguyên lấy giờ, chia dư lấy phút còn lại."),
            ("Đổi giây", "3671 / 3600", "1 giờ, dư 71 giây", "Tiếp tục lấy 71 / 60 = 1 phút, 71 % 60 = 11 giây."),
        ]
    if index == 3:
        return [
            ("Cộng/trừ", "12 + 8 - 5", "15", "Cộng trừ cùng mức ưu tiên, tính từ trái sang phải."),
            ("Nhân trước cộng", "2 + 3 * 4", "14", "Nhân trước, sau đó mới cộng."),
            ("Dùng ngoặc", "(2 + 3) * 4", "20", "Ngoặc làm thay đổi thứ tự tính."),
            ("Chia thực", "5 / 2.0", "2.5", "Có số thực nên kết quả giữ phần thập phân."),
        ]
    if index in (5, 6):
        return [
            ("So sánh", "score >= 5", "true/false", "Điều kiện quyết định nhánh chạy."),
            ("Và", "age >= 14 && age <= 16", "true nếu đủ cả hai", "Dùng khi cần đồng thời nhiều điều kiện đúng."),
            ("Hoặc", "choice == 1 || choice == 2", "true nếu đúng một trong hai", "Dùng khi nhiều lựa chọn đều hợp lệ."),
            ("Biên", "score >= 8", "8.0 được tính", "Dùng >= khi mốc điểm được bao gồm."),
        ]
    return [
        ("Dữ liệu vào", "input → biến", "lưu tạm", "Mọi chương trình đều bắt đầu từ dữ liệu cần xử lý."),
        ("Xử lý", "biến + thuật toán", "kết quả trung gian", "Chia xử lý thành bước nhỏ để dễ debug."),
        ("Dữ liệu ra", "cout / file", "kết quả rõ ràng", "Output cần có nhãn để người dùng hiểu."),
        ("Kiểm thử", "3 bộ test", "tăng độ tin cậy", "Luôn thử bình thường, biên và dễ lỗi."),
    ]


def render_theory_expansion(index: int, lesson: dict) -> str:
    topic = html.escape(lesson["title"])
    pack = topic_pack(index, lesson)
    concepts = pack["concepts"]
    concept_html = "".join(
        f'<div class="concept"><strong>{html.escape(name)}</strong>{html.escape(desc)}</div>'
        for name, desc in concepts
    )
    concept_detail_html = "".join(
        f"""
        <div class="concept-detail">
          <h4>{html.escape(name)}</h4>
          <p><strong>Giải thích:</strong> {html.escape(desc)}</p>
          <ul>
            <li><strong>Minh họa:</strong> dùng một dữ liệu nhỏ để tự tính tay trước, sau đó đối chiếu với chương trình.</li>
            <li><strong>Cách áp dụng:</strong> xác định dữ liệu đầu vào, viết bước xử lý bằng lời, rồi mới chuyển thành câu lệnh C++.</li>
            <li><strong>Lỗi cần tránh:</strong> viết code khi chưa hiểu dữ liệu đang thay đổi như thế nào, hoặc chỉ chạy một test rồi kết luận là đúng.</li>
          </ul>
        </div>
        """
        for name, desc in concepts
    )
    if "concept_details" in pack:
        detail_map = pack["concept_details"]
        concept_detail_html = "".join(
            f"""
        <div class="concept-detail">
          <h4>{html.escape(name)}</h4>
          <p><strong>Giải thích:</strong> {html.escape(desc)}</p>
          <ul>{''.join(f'<li>{html.escape(item)}</li>' for item in detail_map.get(name, []))}</ul>
        </div>
        """
            for name, desc in concepts
        )
    illustration_rows = "".join(
        f"<tr><td>{html.escape(name)}</td><td>{html.escape(expr)}</td><td>{html.escape(result)}</td><td>{html.escape(why)}</td></tr>"
        for name, expr, result, why in pack.get("illustrations", quick_illustrations(index, lesson))
    )
    return f"""
      <div class="two-col">
        <div class="mini-card">
          <h3>Trọng tâm của buổi</h3>
          <p>Buổi này không học thuộc cú pháp một cách rời rạc. Học viên cần hiểu <strong>{topic}</strong> giải quyết vấn đề gì, khi nào nên dùng và dùng sai thì chương trình sẽ hỏng ở đâu.</p>
        </div>
        <div class="mini-card">
          <h3>Cách học trong 90 phút</h3>
          <p>Mỗi khái niệm đi theo chuỗi: đọc yêu cầu → dự đoán cách làm → viết code mẫu → chạy test → sửa lỗi → tự giải thích lại. Nếu chưa giải thích được, chưa coi là nắm chắc.</p>
        </div>
        <div class="mini-card">
          <h3>Lỗi thường gặp</h3>
          <p>Học viên thường sai ở tên biến khó hiểu, thiếu dấu chấm phẩy, nhầm điều kiện biên, hoặc chỉ chạy một test duy nhất. Trong buổi học cần cố tình thử dữ liệu dễ sai.</p>
        </div>
        <div class="mini-card">
          <h3>Tiêu chuẩn hoàn thành</h3>
          <p>Cuối buổi, học viên phải tự viết lại được phiên bản rút gọn của ví dụ, thay đổi được dữ liệu đầu vào và trả lời được câu hỏi: từng biến trong chương trình dùng để làm gì?</p>
        </div>
      </div>
      <h3>Kiến thức cần nắm chắc</h3>
      <div class="concept-grid">{concept_html}</div>
      <h3>Diễn giải chi tiết từng ý</h3>
      {concept_detail_html}
      <h3>Minh họa nhanh trước khi viết code</h3>
      <table class="quick-table">
        <thead><tr><th>Ý cần hiểu</th><th>Biểu thức / tình huống</th><th>Kết quả</th><th>Giải thích</th></tr></thead>
        <tbody>{illustration_rows}</tbody>
      </table>
      <div class="teacher-note">
        <strong>Gợi ý giảng dạy:</strong> sau mỗi minh họa, yêu cầu học viên tự tạo thêm một ví dụ tương tự và dự đoán kết quả trước khi chạy chương trình.
      </div>
    """


def render_example_analysis(lesson: dict) -> str:
    title = html.escape(lesson["example_title"])
    rows = [
        ("Bài toán", title),
        ("Đầu vào", "Dữ liệu người dùng nhập hoặc dữ liệu mẫu có sẵn trong chương trình."),
        ("Xử lý chính", "Áp dụng kiến thức của buổi học, chia thành các bước nhỏ và kiểm tra từng bước."),
        ("Đầu ra", "Kết quả in ra console phải rõ ràng, có nhãn, dễ đọc và dễ so sánh với kỳ vọng."),
        ("Test tối thiểu", "Một trường hợp bình thường, một trường hợp biên và một trường hợp dễ gây lỗi."),
    ]
    body = "".join(f"<tr><th>{label}</th><td>{text}</td></tr>" for label, text in rows)
    return f"<table><tbody>{body}</tbody></table>"


def topic_pack(index: int, lesson: dict) -> dict:
    title = lesson["title"]

    if index == 1:
        return {
            "concepts": [
                ("File .cpp và quá trình biên dịch", "Học viên cần hiểu mình đang viết mã nguồn trong file .cpp. Máy tính chưa chạy trực tiếp file này; compiler sẽ đọc code, kiểm tra cú pháp, rồi tạo chương trình có thể chạy. Nếu thiếu dấu ;, thiếu ngoặc hoặc viết sai tên lệnh, lỗi sẽ xuất hiện ở bước biên dịch."),
                ("Cấu trúc chương trình tối thiểu", "Một chương trình C++ cơ bản có #include <iostream> để dùng nhập xuất, using namespace std để viết cout gọn hơn, hàm int main() là điểm bắt đầu chạy, các lệnh nằm trong cặp ngoặc nhọn { } và thường kết thúc bằng dấu chấm phẩy."),
                ("In dữ liệu bằng cout", "cout dùng toán tử << để gửi chữ, số hoặc biến ra màn hình. Có thể dùng endl hoặc ký tự \\n để xuống dòng. Output cần có nhãn rõ ràng để người học tự kiểm tra kết quả, không chỉ in ra một dòng khó hiểu."),
                ("Đọc lỗi và tự sửa lỗi cơ bản", "Bài đầu tiên phải tập thói quen đọc thông báo lỗi: dòng nào lỗi, lỗi do thiếu ; hay thiếu ngoặc, lỗi do viết sai cout thành count. Học viên không cần hiểu hết mọi dòng lỗi, nhưng cần biết khoanh vùng và sửa từng lỗi một."),
            ],
            "concept_details": {
                "File .cpp và quá trình biên dịch": [
                    "Giáo viên cho học viên tạo file hello.cpp, gõ chương trình ngắn, sau đó bấm Run hoặc dùng lệnh biên dịch để thấy code được chuyển thành chương trình chạy được.",
                    "Phân biệt rõ ba trạng thái: đang viết code, đang biên dịch, đang chạy chương trình. Khi chương trình chưa biên dịch được thì chưa xét đúng sai logic.",
                    "Minh họa lỗi bằng cách xóa một dấu ; rồi chạy lại để học viên thấy compiler dừng trước khi chương trình chạy.",
                ],
                "Cấu trúc chương trình tối thiểu": [
                    "#include <iostream> đặt ở đầu file vì cout thuộc thư viện nhập xuất. Nếu bỏ dòng này, compiler không hiểu cout là gì.",
                    "int main() là nơi chương trình bắt đầu. Các lệnh trong cặp { } của main sẽ chạy theo thứ tự từ trên xuống dưới.",
                    "Dấu ; kết thúc một câu lệnh. Dấu { } gom nhiều câu lệnh thành một khối. Bài đầu cần luyện nhìn đủ cặp ngoặc trước khi sửa code.",
                ],
                "In dữ liệu bằng cout": [
                    "cout << \"Xin chao\" in một chuỗi chữ. Nếu muốn nối thêm số hoặc chữ khác, tiếp tục dùng << ở phía sau.",
                    "endl và \\n đều giúp xuống dòng. Với học sinh mới, nên dùng endl trước cho dễ đọc, sau đó giới thiệu \\n để viết gọn hơn.",
                    "Output nên có nhãn như Ho ten:, Lop:, Muc tieu: để khi chạy chương trình học viên biết mỗi dòng đang biểu diễn thông tin nào.",
                ],
                "Đọc lỗi và tự sửa lỗi cơ bản": [
                    "Khi có lỗi, không xóa lung tung. Đọc dòng compiler báo, kiểm tra dòng đó và dòng ngay phía trên vì lỗi thiếu ; thường làm dòng sau bị báo lỗi.",
                    "Các lỗi bài 01 nên luyện gồm thiếu ;, thiếu }, viết Cout thay cout, thiếu dấu nháy kép đóng chuỗi.",
                    "Sau mỗi lần sửa một lỗi, chạy lại ngay. Cách này giúp học viên biết lỗi nào đã được xử lý và tránh tạo thêm lỗi mới.",
                ],
            },
            "illustrations": [
                ("File nguồn", "hello.cpp", "mã C++", "Đây là file học viên gõ code, chưa phải chương trình đã chạy."),
                ("Biên dịch", "g++ hello.cpp -o hello", "tạo file chạy", "Compiler kiểm tra cú pháp trước khi cho chương trình chạy."),
                ("Dòng bắt đầu", "int main()", "điểm chạy đầu tiên", "Khi mở chương trình, máy bắt đầu thực hiện các lệnh trong main."),
                ("Xuống dòng", "cout << \"Hi\\n\";", "in Hi rồi xuống dòng", "\\n giúp trình bày nhiều dòng gọn hơn trong một câu lệnh cout."),
            ],
            "examples": [
                ("In hồ sơ học viên nhiều dòng", "Viết chương trình in thông tin cá nhân thành từng dòng rõ ràng.", r'''#include <iostream>
using namespace std;

int main() {
    cout << "Ho ten: Nguyen Minh Anh\n";
    cout << "Lop: 10A1\n";
    cout << "Muc tieu: hoc C++ de lam san pham demo\n";
    return 0;
}''', ["#include <iostream> giúp dùng cout.", "Mỗi câu cout in một ý riêng để dễ đọc.", "return 0 đặt cuối main để kết thúc chương trình bình thường."]),
                ("So sánh endl và \\n", "Cùng in 3 dòng nhưng dùng \\n để học viên thấy cách xuống dòng ngắn gọn.", r'''#include <iostream>
using namespace std;

int main() {
    cout << "Dong 1\nDong 2\nDong 3\n";
    return 0;
}''', ["Chuỗi có thể chứa nhiều ký tự xuống dòng \\n.", "Dòng code ngắn hơn nhưng vẫn phải kiểm tra output.", "Khi mới học, có thể dùng endl cho dễ nhìn rồi chuyển sang \\n."]),
                ("Sửa lỗi thiếu dấu chấm phẩy", "Cho học viên cố tình tạo lỗi để biết cách đọc lỗi compiler.", r'''#include <iostream>
using namespace std;

int main() {
    cout << "Xin chao C++" << endl
    cout << "Dong nay se bao loi" << endl;
    return 0;
}''', ["Dòng cout đầu tiên thiếu dấu ;.", "Compiler thường báo lỗi ở dòng hiện tại hoặc dòng ngay sau đó.", "Sửa từng lỗi rồi biên dịch lại, không sửa nhiều chỗ cùng lúc khi chưa chắc."]),
            ],
            "classwork": [
                ("Bài 1 - In thẻ giới thiệu", "In họ tên, lớp, trường, sở thích và mục tiêu học C++ thành 5 dòng có nhãn."),
                ("Bài 2 - In thời khóa biểu", "In lịch học 5 ngày trong tuần, mỗi ngày một dòng, trình bày thẳng hàng dễ đọc."),
                ("Bài 3 - Sửa chương trình lỗi", "Giáo viên đưa đoạn code thiếu ;, thiếu ngoặc }, viết sai cout; học viên sửa cho biên dịch được."),
                ("Bài 4 - Giải thích code", "Học viên chỉ ra #include, main, cout, return 0 nằm ở đâu và mỗi phần dùng để làm gì."),
            ],
        }

    if index == 2:
        return {
            "concepts": [
                ("Biến là nơi lưu dữ liệu", "Biến giống một hộp có tên trong bộ nhớ. Khi nhập tuổi, điểm hoặc tên, chương trình cần lưu vào biến để dùng lại ở bước xử lý và bước in kết quả."),
                ("Chọn đúng kiểu dữ liệu", "int dùng cho số nguyên như tuổi, số lượng; double dùng cho điểm số hoặc tiền có phần lẻ; string dùng cho họ tên; char dùng cho một ký tự; bool dùng cho đúng/sai. Chọn sai kiểu sẽ làm mất dữ liệu hoặc khiến code khó hiểu."),
                ("cin và getline khác nhau", "cin đọc đến khoảng trắng, phù hợp với số hoặc một từ. getline đọc cả dòng, phù hợp với họ tên có dấu cách. Khi dùng cin trước getline, cần xử lý ký tự xuống dòng còn lại bằng cin.ignore()."),
                ("Output có nhãn để kiểm tra", "Sau khi nhập, cần in lại dữ liệu có nhãn rõ ràng. Việc này giúp học viên phát hiện nhập thiếu, nhập sai kiểu hoặc biến chưa được gán giá trị."),
            ],
            "concept_details": {
                "Biến là nơi lưu dữ liệu": [
                    "Cho học viên nhập age = 15 rồi in lại age để thấy dữ liệu không tự biến mất sau khi nhập.",
                    "Giải thích bằng luồng: bàn phím đưa dữ liệu vào cin, cin đặt dữ liệu vào biến, cout lấy dữ liệu từ biến để in ra.",
                    "Nhấn mạnh biến phải có tên rõ nghĩa vì sau này một chương trình có thể có hàng chục biến.",
                ],
                "Chọn đúng kiểu dữ liệu": [
                    "Nếu dùng int cho điểm 8.5, phần .5 có thể bị mất hoặc không xử lý đúng như mong muốn.",
                    "Nếu dùng string cho số lượng, chương trình in được nhưng chưa thể tính tổng tiền trực tiếp như số.",
                    "Trước khi khai báo biến, học viên cần trả lời: dữ liệu này là số đếm, số có lẻ, chữ, một ký tự hay đúng/sai?",
                ],
                "cin và getline khác nhau": [
                    "cin >> name chỉ đọc đến khoảng trắng đầu tiên, nên Nguyen Van An có thể chỉ lấy Nguyen.",
                    "getline(cin, name) đọc cả dòng, phù hợp với họ tên, địa chỉ, mô tả sản phẩm.",
                    "Khi dùng cin trước getline, ký tự Enter còn trong bộ đệm; cin.ignore() giúp bỏ ký tự đó để getline đọc đúng dòng tiếp theo.",
                ],
                "Output có nhãn để kiểm tra": [
                    "Không nên chỉ in 15 hoặc 8.5 vì người xem không biết đó là tuổi hay điểm.",
                    "Mẫu tốt: cout << \"Tuoi: \" << age << endl; giúp tự kiểm tra dữ liệu đã vào đúng biến chưa.",
                    "Cuối bài, học viên cần chạy thử với họ tên có khoảng trắng và điểm thập phân để kiểm tra đủ các kiểu dữ liệu.",
                ],
            },
            "illustrations": [
                ("int", "age = 15", "số nguyên", "Tuổi không cần phần thập phân."),
                ("double", "score = 8.5", "số thực", "Điểm có thể có phần lẻ nên không dùng int."),
                ("string", "name = \"Nguyen An\"", "chuỗi", "Họ tên có nhiều ký tự và có thể có khoảng trắng."),
                ("getline", "getline(cin, name)", "đọc cả dòng", "Phù hợp khi nhập họ tên đầy đủ."),
            ],
            "examples": [
                ("Nhập sản phẩm và in hóa đơn", "Nhập tên sản phẩm, số lượng, đơn giá rồi in lại thông tin.", r'''#include <iostream>
#include <string>
using namespace std;

int main() {
    string productName;
    int quantity;
    double price;

    cout << "Nhap ten san pham: ";
    getline(cin, productName);
    cout << "Nhap so luong: ";
    cin >> quantity;
    cout << "Nhap don gia: ";
    cin >> price;

    cout << "San pham: " << productName << endl;
    cout << "So luong: " << quantity << endl;
    cout << "Don gia: " << price << endl;
    return 0;
}''', ["productName dùng string vì là chữ.", "quantity dùng int vì là số lượng đếm được.", "price dùng double vì tiền có thể có phần lẻ."]),
                ("Dùng cin.ignore trước getline", "Minh họa lỗi thường gặp khi nhập số trước rồi nhập họ tên.", r'''#include <iostream>
#include <string>
using namespace std;

int main() {
    int age;
    string fullName;

    cout << "Nhap tuoi: ";
    cin >> age;
    cin.ignore();

    cout << "Nhap ho ten: ";
    getline(cin, fullName);

    cout << fullName << " - " << age << " tuoi\n";
    return 0;
}''', ["cin >> age để lại ký tự xuống dòng trong bộ đệm.", "cin.ignore() bỏ ký tự đó trước khi gọi getline.", "Nếu thiếu cin.ignore(), getline có thể đọc dòng rỗng."]),
                ("Đặt tên biến rõ nghĩa", "So sánh cách đặt biến khó hiểu và cách đặt biến dễ đọc.", r'''int a = 15;
double b = 8.5;

int age = 15;
double mathScore = 8.5;''', ["a, b chạy được nhưng không nói rõ ý nghĩa.", "age và mathScore giúp người đọc hiểu ngay dữ liệu.", "Từ buổi này nên tập đặt tên biến theo nội dung bài toán."]),
            ],
            "classwork": [
                ("Bài 1 - Hồ sơ học viên", "Nhập họ tên, tuổi, lớp, điểm Toán; in lại thành bảng thông tin."),
                ("Bài 2 - Hóa đơn nhỏ", "Nhập tên món hàng, số lượng, đơn giá; in dữ liệu đã nhập có nhãn."),
                ("Bài 3 - Chọn kiểu dữ liệu", "Cho 10 loại dữ liệu thực tế, học viên chọn int/double/string/char/bool và giải thích."),
                ("Bài 4 - Lỗi getline", "Viết chương trình nhập tuổi trước, họ tên sau; thử bỏ cin.ignore rồi sửa lại."),
            ],
        }

    packs = {
        "modulo": {
            "concepts": [
                ("Chia nguyên", "Khi cả hai toán hạng là số nguyên, phép / lấy phần nguyên. Ví dụ 17 / 5 bằng 3, vì 5 đi được 3 lần trong 17."),
                ("Chia dư", "Toán tử % lấy phần còn lại sau phép chia nguyên. Ví dụ 17 % 5 bằng 2. Đây là công cụ chính để kiểm tra chẵn lẻ và chia hết."),
                ("Kiểm tra điều kiện", "Một biểu thức như n % 2 == 0 cho kết quả đúng/sai, nên thường đi cùng if/else để ra quyết định."),
                ("Dữ liệu biên", "Cần thử các số như 0, 1, số chia hết, số không chia hết và mẫu số bằng 0 nếu bài toán cho nhập mẫu số."),
            ],
            "examples": [
                ("Kiểm tra chẵn lẻ", "Nhập một số nguyên, dùng n % 2 để quyết định số đó chẵn hay lẻ.", r'''int n;
cout << "Nhap n: ";
cin >> n;

if (n % 2 == 0) {
    cout << "n la so chan\n";
} else {
    cout << "n la so le\n";
}''', ["n % 2 trả về 0 nếu n chia hết cho 2.", "Điều kiện == 0 là điều kiện số chẵn.", "Nên thử n = 0, 1, 2, 15."]),
                ("Kiểm tra chia hết", "Nhập a và b, kiểm tra a có chia hết cho b hay không, đồng thời xử lý b = 0.", r'''int a, b;
cout << "Nhap a b: ";
cin >> a >> b;

if (b == 0) {
    cout << "Khong the chia cho 0\n";
} else if (a % b == 0) {
    cout << a << " chia het cho " << b << endl;
} else {
    cout << a << " khong chia het cho " << b << endl;
}''', ["Luôn kiểm tra b == 0 trước khi dùng a % b.", "else-if chỉ chạy khi b khác 0.", "Bài này luyện thứ tự điều kiện an toàn."]),
                ("Tách giờ phút giây", "Dùng / và % nhiều lần để đổi tổng số giây thành giờ, phút, giây.", r'''int totalSeconds;
cin >> totalSeconds;

int hours = totalSeconds / 3600;
int remain = totalSeconds % 3600;
int minutes = remain / 60;
int seconds = remain % 60;

cout << hours << " gio "
     << minutes << " phut "
     << seconds << " giay\n";''', ["3600 giây tạo thành 1 giờ.", "remain giữ phần chưa đổi ra giờ.", "Sau đó tiếp tục chia cho 60 để lấy phút và giây."]),
            ],
            "classwork": [
                ("Bài 1 - Chẵn lẻ", "Nhập 5 số nguyên, in từng số là chẵn hay lẻ."),
                ("Bài 2 - Chia hết", "Nhập a, b, kiểm tra a có chia hết cho b không, bắt buộc xử lý b = 0."),
                ("Bài 3 - Đổi thời gian", "Nhập tổng số giây, đổi ra giờ - phút - giây."),
                ("Bài 4 - Nâng cao nhẹ", "Nhập một số, kiểm tra số đó có chia hết cho cả 3 và 5 hay không."),
            ],
        },
        "arithmetic": {
            "concepts": [
                ("Biểu thức", "Biểu thức kết hợp biến, hằng và toán tử để tạo ra giá trị mới. Nên dùng biến trung gian để code dễ đọc."),
                ("Thứ tự ưu tiên", "Nhân/chia được tính trước cộng/trừ. Khi công thức dài, dùng ngoặc để thể hiện rõ ý định."),
                ("Số nguyên và số thực", "int phù hợp với số đếm, double phù hợp với điểm số, tiền trung bình, diện tích hoặc kết quả có phần lẻ."),
                ("Kiểm tra kết quả", "Với bài tính toán, nên tự tính tay một ví dụ nhỏ rồi so sánh với output của chương trình."),
            ],
            "examples": [
                ("Tính hóa đơn", "Nhập số lượng, đơn giá, giảm giá và tính tổng tiền.", r'''int quantity;
double price, discount;
cin >> quantity >> price >> discount;

double total = quantity * price;
double finalTotal = total - total * discount / 100;
cout << "Thanh tien: " << finalTotal << endl;''', ["quantity là số nguyên vì là số lượng.", "price và discount dùng double.", "Công thức được tách thành total và finalTotal để dễ kiểm tra."]),
                ("Điểm trung bình có hệ số", "Bài kiểm tra cuối hệ số 2, nên tổng hệ số là 4.", r'''double a, b, finalTest;
cin >> a >> b >> finalTest;

double average = (a + b + finalTest * 2) / 4.0;
cout << "Diem TB: " << average << endl;''', ["Nhân finalTest với 2 trước khi cộng.", "Chia cho 4.0 để lấy kết quả số thực.", "Dùng ngoặc để công thức rõ ràng."]),
                ("Đổi đơn vị", "Đổi centimet sang mét và centimet còn lại.", r'''int cm;
cin >> cm;
int meters = cm / 100;
int remainCm = cm % 100;
cout << meters << "m " << remainCm << "cm\n";''', ["Phần mét lấy bằng chia nguyên.", "Phần centimet còn lại lấy bằng chia dư.", "Ví dụ này nối với kiến thức buổi chia dư."]),
            ],
            "classwork": [
                ("Bài 1 - Tính diện tích", "Nhập chiều dài, chiều rộng, tính chu vi và diện tích hình chữ nhật."),
                ("Bài 2 - Tính hóa đơn", "Nhập số lượng, đơn giá, phần trăm giảm giá, in số tiền cuối cùng."),
                ("Bài 3 - Điểm hệ số", "Nhập 3 điểm, trong đó điểm cuối hệ số 2, tính trung bình."),
                ("Bài 4 - Debug", "Sửa lỗi chương trình dùng int khiến kết quả trung bình bị mất phần thập phân."),
            ],
        },
        "condition": {
            "concepts": [
                ("Điều kiện đúng/sai", "if cần một biểu thức trả về true hoặc false. Điều kiện càng rõ, code càng dễ kiểm tra."),
                ("Nhánh loại trừ", "if/else-if/else dùng khi chỉ một nhánh được chọn. Thứ tự điều kiện quyết định kết quả."),
                ("Điều kiện kết hợp", "Có thể dùng && cho 'và', || cho 'hoặc', ! cho phủ định. Nên dùng ngoặc nếu điều kiện dài."),
                ("Dữ liệu biên", "Các mốc như 5.0, 6.5, 8.0 cần test kỹ vì rất dễ viết nhầm > và >=."),
            ],
            "examples": [
                ("Kiểm tra điểm hợp lệ", "Điểm phải nằm trong khoảng 0 đến 10.", r'''double score;
cin >> score;

if (score < 0 || score > 10) {
    cout << "Diem khong hop le\n";
} else {
    cout << "Diem hop le\n";
}''', ["Dùng || vì chỉ cần một điều kiện sai phạm là không hợp lệ.", "Điểm 0 và 10 vẫn hợp lệ.", "Nên test -1, 0, 10, 11."]),
                ("Xếp loại", "Sắp xếp điều kiện từ mức cao xuống thấp.", r'''if (score >= 8) {
    cout << "Gioi\n";
} else if (score >= 6.5) {
    cout << "Kha\n";
} else if (score >= 5) {
    cout << "Trung binh\n";
} else {
    cout << "Can co gang\n";
}''', ["Điểm 9 sẽ vào nhánh đầu tiên.", "Nếu đảo thứ tự sai, điểm cao có thể bị xếp thấp.", "else cuối xử lý mọi trường hợp còn lại."]),
                ("Menu bằng switch", "Dùng switch khi lựa chọn là các giá trị rời rạc.", r'''int choice;
cin >> choice;

switch (choice) {
    case 1: cout << "Them du lieu\n"; break;
    case 2: cout << "Xem danh sach\n"; break;
    case 0: cout << "Thoat\n"; break;
    default: cout << "Lua chon sai\n";
}''', ["Mỗi case cần break.", "default xử lý lựa chọn ngoài menu.", "Menu là nền tảng cho dự án console."]),
            ],
            "classwork": [
                ("Bài 1 - Điểm hợp lệ", "Nhập điểm, kiểm tra có nằm trong 0..10 không."),
                ("Bài 2 - Xếp loại", "Nhập điểm trung bình, in xếp loại và lời nhận xét."),
                ("Bài 3 - Menu", "Viết menu 1. Cộng 2. Trừ 3. Nhân 4. Chia 0. Thoát."),
                ("Bài 4 - Biên", "Tạo bảng test cho các điểm 4.9, 5.0, 6.5, 8.0, 10.0."),
            ],
        },
    }

    if index == 4:
        return packs["modulo"]
    if index in (3,):
        return packs["arithmetic"]
    if index in (5, 6):
        return packs["condition"]

    generic_examples = [
        ("Ví dụ biến thể", f"Áp dụng {title.lower()} vào một bài toán dữ liệu học sinh.", r'''// Bien the mau cho buoi hoc
// Giao vien co the thay doi du lieu theo bai dang hoc.
cout << "Nhap du lieu, xu ly, sau do in ket qua ro rang." << endl;''', ["Xác định đầu vào trước.", "Viết từng bước xử lý.", "In kết quả có nhãn rõ ràng."]),
        ("Ví dụ kiểm tra dữ liệu", "Thêm kiểm tra để chương trình không xử lý dữ liệu vô lý.", r'''if (n <= 0) {
    cout << "Du lieu khong hop le\n";
    return 0;
}''', ["Kiểm tra dữ liệu trước khi xử lý.", "Thông báo lỗi cần dễ hiểu.", "Không để chương trình tiếp tục với dữ liệu sai."]),
        ("Ví dụ tách bước", "Chia bài toán thành nhập, xử lý và xuất kết quả.", r'''// 1. Nhap du lieu
// 2. Xu ly theo kien thuc cua buoi hoc
// 3. In ket qua va test lai''', ["Tách bước giúp học viên không bị rối.", "Mỗi bước có thể kiểm tra riêng.", "Đây là cách chuẩn bị cho dự án cuối khóa."]),
    ]
    return {
        "concepts": [
            ("Bản chất", f"{title} cần được hiểu như một công cụ giải quyết bài toán, không chỉ là cú pháp cần nhớ."),
            ("Cách triển khai", "Luôn bắt đầu từ dữ liệu đầu vào, viết các bước xử lý bằng lời, rồi mới chuyển từng bước thành code."),
            ("Cách kiểm tra", "Sau khi code chạy, cần test dữ liệu bình thường, dữ liệu biên và dữ liệu dễ làm chương trình sai."),
            ("Liên hệ dự án", "Kiến thức buổi này sẽ được dùng lại trong sản phẩm demo cuối khóa, nên học viên cần giải thích được bằng lời."),
        ],
        "examples": generic_examples,
        "classwork": [
            ("Bài 1 - Làm lại ví dụ", "Gõ lại ví dụ chính, chạy đúng output và đổi dữ liệu đầu vào."),
            ("Bài 2 - Biến thể", f"Viết bài mới cùng chủ đề {title.lower()} với bối cảnh điểm số hoặc sản phẩm."),
            ("Bài 3 - Thêm kiểm tra", "Thêm kiểm tra dữ liệu nhập và thông báo lỗi rõ ràng."),
            ("Bài 4 - Giải thích", "Trình bày lại code theo 3 phần: đầu vào, xử lý, đầu ra."),
        ],
    }


def render_examples(index: int, lesson: dict, code: str, explanation: str) -> str:
    main_block = f"""
      <div class="example-block">
        <h3>Ví dụ 1 - {html.escape(lesson['example_title'])}</h3>
        {render_example_analysis(lesson)}
        <pre><code>{code}</code></pre>
        <div class="example-explain">
          <strong>Giải thích từng bước</strong>
          <ol>{explanation}</ol>
        </div>
      </div>
    """
    extra_blocks = []
    for idx, (title, desc, extra_code, steps) in enumerate(topic_pack(index, lesson)["examples"], start=2):
        step_html = "".join(f"<li>{html.escape(step)}</li>" for step in steps)
        extra_blocks.append(
            f"""
      <div class="example-block">
        <h3>Ví dụ {idx} - {html.escape(title)}</h3>
        <p>{html.escape(desc)}</p>
        <pre><code>{html.escape(extra_code)}</code></pre>
        <div class="example-explain">
          <strong>Điểm cần hiểu</strong>
          <ol>{step_html}</ol>
        </div>
      </div>
            """
        )
    return main_block + "".join(extra_blocks)


def render_classwork(index: int, lesson: dict) -> str:
    tasks = topic_pack(index, lesson)["classwork"]
    return "".join(f'<div class="practice"><strong>{level}</strong>{desc}</div>' for level, desc in tasks)


def render_checkpoint(index: int, lesson: dict) -> str:
    checks = [
        "Chạy được ví dụ mẫu không lỗi biên dịch.",
        "Tự sửa được ít nhất một lỗi nhỏ trong quá trình code.",
        "Nêu được mục đích của các biến/hàm chính.",
        "Hoàn thành ít nhất bài thực hành mức 1 và bắt đầu mức 2.",
        "Biết cần làm gì trong bài tập về nhà và tiêu chí nộp bài.",
    ]
    return "".join(f"<li>{item}</li>" for item in checks)


def render_lesson(index: int, lesson: dict) -> str:
    prev_link = lesson_filename(index - 1, LESSONS[index - 2]["title"]) if index > 1 else None
    next_link = lesson_filename(index + 1, LESSONS[index]["title"]) if index < len(LESSONS) else None
    code = html.escape(lesson["code"])
    goals = "".join(f"<li>{html.escape(item)}</li>" for item in lesson["objectives"])
    theory = "".join(f"<li>{html.escape(item)}</li>" for item in lesson["theory"])
    explanation = "".join(f"<li>{html.escape(item)}</li>" for item in lesson["explanation"])
    homework = "".join(f"<li>{html.escape(item)}</li>" for item in lesson["homework"])
    timeline = render_timeline(index, lesson)
    theory_expansion = render_theory_expansion(index, lesson)
    examples_html = render_examples(index, lesson, code, explanation)
    classwork = render_classwork(index, lesson)
    checkpoint = render_checkpoint(index, lesson)
    prev_html = f'<a href="{prev_link}">← Bài trước</a>' if prev_link else "<span></span>"
    next_html = f'<a href="{next_link}">Bài sau →</a>' if next_link else "<span></span>"
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Buổi {index:02d} - {html.escape(lesson['title'])}</title>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <meta name="theme-color" content="#06b6d4">
  <style>{STYLE}</style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <a class="brand" href="index.html">GiaSuTHT · Bài giảng C++</a>
      <div class="nav">
        <a href="../khoa-hoc-cpp-nentang.html">Trang khóa học</a>
        <a href="index.html">Mục lục</a>
      </div>
    </div>

    <header class="hero">
      <span class="badge">{html.escape(lesson['phase'])}</span>
      <h1>Buổi {index:02d}: {html.escape(lesson['title'])}</h1>
      <p class="note">Mục tiêu buổi học: học chắc lý thuyết, hiểu ví dụ, tự hoàn thành bài tập về nhà và giải thích được code.</p>
      <div class="grid">
        <div class="card"><strong>Lý thuyết</strong>Đọc hiểu khái niệm và cách áp dụng.</div>
        <div class="card"><strong>Ví dụ</strong>Code mẫu có giải thích từng bước.</div>
        <div class="card"><strong>Bài tập</strong>Tự luyện sau buổi học để giữ nhịp.</div>
      </div>
    </header>

    <section>
      <h2>1. Mục tiêu cần đạt</h2>
      <ul>{goals}</ul>
    </section>

    <section>
      <h2>2. Kịch bản buổi học 90 phút</h2>
      <ol class="timeline">{timeline}</ol>
    </section>

    <section>
      <h2>3. Bài giảng lý thuyết chi tiết</h2>
      {theory_expansion}
      <h3>Phần giảng chính</h3>
      <ol class="theory">{theory}</ol>
      <h3>Câu hỏi kiểm tra nhanh</h3>
      <ol>
        <li>Khái niệm chính của buổi này dùng để giải quyết vấn đề gì?</li>
        <li>Nếu nhập dữ liệu sai hoặc gặp trường hợp biên, chương trình có thể lỗi ở đâu?</li>
        <li>Em sẽ giải thích bài này cho một bạn chưa học bằng ví dụ đời thường nào?</li>
      </ol>
    </section>

    <section>
      <h2>4. Ví dụ minh họa cụ thể</h2>
      <p class="note">Mỗi buổi có 4 ví dụ: một ví dụ chính để học theo từng bước và ba ví dụ biến thể để thấy kiến thức được dùng trong nhiều bối cảnh.</p>
      {examples_html}
      <h3>Bộ test gợi ý</h3>
      <ol>
        <li>Test bình thường: nhập dữ liệu hợp lệ, kỳ vọng chương trình in kết quả đúng.</li>
        <li>Test biên: nhập giá trị nhỏ nhất/lớn nhất hợp lý trong phạm vi bài toán.</li>
        <li>Test dễ lỗi: nhập dữ liệu khiến điều kiện rẽ nhánh, vòng lặp hoặc chỉ số mảng dễ sai.</li>
      </ol>
    </section>

    <section>
      <h2>5. Bài tập thực hành trên lớp</h2>
      <div class="practice-grid">{classwork}</div>
    </section>

    <section>
      <h2>6. Checklist cuối buổi</h2>
      <ul class="checklist">{checkpoint}</ul>
    </section>

    <section>
      <h2>7. Bài tập về nhà</h2>
      <ol class="homework">{homework}</ol>
      <p class="note">Yêu cầu nộp: file .cpp chạy được, ảnh chụp output và 3 dòng tự nhận xét: phần dễ, phần khó, lỗi đã sửa.</p>
    </section>

    <div class="pager">
      {prev_html}
      {next_html}
    </div>
  </div>
</body>
</html>
"""


def render_index() -> str:
    rows = []
    for idx, lesson in enumerate(LESSONS, start=1):
        filename = lesson_filename(idx, lesson["title"])
        rows.append(
            f"<tr><td>Buổi {idx:02d}</td><td><a href=\"{filename}\">{html.escape(lesson['title'])}</a></td><td>{html.escape(lesson['phase'])}</td></tr>"
        )
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mục lục bài giảng C++</title>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <meta name="theme-color" content="#06b6d4">
  <style>{STYLE}</style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <a class="brand" href="../khoa-hoc-cpp-nentang.html">GiaSuTHT · Khóa C++</a>
      <div class="nav"><a href="../index.html">Trang chủ</a><a href="../khoa-hoc-cpp-nentang.html">Trang khóa học</a></div>
    </div>
    <header class="hero">
      <span class="badge">Bộ bài giảng HTML</span>
      <h1>Nền tảng C++ &amp; tư duy lập trình</h1>
      <p class="note">Bộ bài giảng chi tiết cho từng buổi học 90 phút, đi từ nền tảng C++ đến sản phẩm demo cuối khóa.</p>
    </header>
    <section>
      <h2>Mục lục</h2>
      <table>
        <thead><tr><th>Buổi</th><th>Bài học</th><th>Giai đoạn</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </section>
  </div>
</body>
</html>
"""


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    for idx, lesson in enumerate(LESSONS, start=1):
        (OUT_DIR / lesson_filename(idx, lesson["title"])).write_text(render_lesson(idx, lesson), encoding="utf-8")
    (OUT_DIR / "index.html").write_text(render_index(), encoding="utf-8")
    print(f"Generated {len(LESSONS)} lesson files in {OUT_DIR}")


if __name__ == "__main__":
    main()
