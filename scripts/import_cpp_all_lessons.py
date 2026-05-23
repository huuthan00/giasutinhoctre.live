from __future__ import annotations

import html
import re
from pathlib import Path

from generate_cpp_lessons import LESSONS, STYLE, lesson_filename


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "c++all.txt"
OUT_DIR = ROOT / "bai-giang-cpp-15tuoi"
PROTECTED_FROM_LESSON = 10
SECURITY_CODE = "CPP15"
LOCK_STORAGE_KEY = "giasutht_cpp_lesson_access_v2"

LESSON_HEADING_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:\*\*)?Bu\u1ed5i\s+(\d{1,2})\s*-\s*(.+?)(?:\*\*)?\s*$",
    re.MULTILINE,
)
SECTION_HEADING_RE = re.compile(r"^\*{0,2}(\d+)\.\s*(.+?)\*{0,2}\s*$")
ORDERED_ITEM_RE = re.compile(r"^(\d+)\.\s+(.+)$")
IMAGE_NOTE_RE = re.compile(r"\[\s*📸\s*Hình ảnh ví dụ:\s*(.+?)\s*\]")


EXTRA_STYLE = """
.lesson-body {
  padding: 28px;
}
.lesson-body h2 {
  margin-top: 34px;
  padding-top: 18px;
  border-top: 1px solid var(--border);
  color: var(--primary);
}
.lesson-body h2:first-child {
  margin-top: 0;
  padding-top: 0;
  border-top: 0;
}
.lesson-body h3 {
  color: var(--accent);
  margin-top: 24px;
}
.lesson-body h4 {
  color: #bae6fd;
  margin: 20px 0 8px;
}
.lesson-body p {
  margin: 10px 0 14px;
}
.lesson-body ul,
.lesson-body ol {
  margin: 10px 0 18px;
}
.lesson-body li {
  margin-bottom: 10px;
}
.task-list {
  list-style: none;
  padding-left: 0;
}
.task-item {
  list-style: none;
  margin-bottom: 14px;
}
.task-item strong {
  color: #eef2ff;
}
.check-item {
  list-style: none;
  margin-left: -4px;
}
.check-box {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 1px solid rgba(238,242,255,.7);
  border-radius: 3px;
  margin-right: 8px;
  transform: translateY(2px);
}
.lesson-body blockquote,
.image-note {
  border-left: 3px solid var(--warn);
  background: rgba(245,158,11,.08);
  padding: 12px 14px;
  border-radius: 10px;
  margin: 14px 0;
}
.image-note > strong {
  display: block;
  color: var(--warn);
  margin-bottom: 8px;
}
.image-note p {
  margin: 8px 0;
}
.image-note ul {
  margin-bottom: 0;
}
.image-note li strong {
  color: #fde68a;
}
.lesson-body pre {
  margin: 14px 0 18px;
}
.lesson-body code {
  white-space: pre-wrap;
}
.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin-top: 20px;
}
.lesson-locked {
  overflow: hidden;
}
.lesson-locked .wrap {
  display: none;
}
.lock-screen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: grid;
  place-items: center;
  padding: 24px;
  background: radial-gradient(circle at top left, rgba(6,182,212,.16), transparent 38%), rgba(5,8,22,.96);
}
.lock-card {
  width: min(460px, 100%);
  background: rgba(17,24,39,.96);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 26px;
  box-shadow: 0 24px 80px rgba(0,0,0,.34);
}
.lock-card h1 {
  font-size: 28px;
  margin: 10px 0 8px;
}
.lock-card p {
  color: var(--muted);
  margin: 0 0 16px;
}
.lock-form {
  display: grid;
  gap: 12px;
}
.lock-form label {
  color: var(--text);
  font-weight: 700;
}
.lock-form input {
  width: 100%;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px 14px;
  background: rgba(255,255,255,.06);
  color: var(--text);
  font: inherit;
  outline: none;
}
.lock-form input:focus {
  border-color: rgba(6,182,212,.7);
  box-shadow: 0 0 0 3px rgba(6,182,212,.12);
}
.lock-form button {
  border: 0;
  border-radius: 10px;
  padding: 12px 14px;
  background: linear-gradient(135deg, #06b6d4, #6366f1);
  color: white;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
}
.lock-error {
  min-height: 22px;
  color: #fca5a5;
  font-size: 14px;
}
.lesson-protected:not(.lesson-locked) .lock-screen {
  display: none;
}
@media (max-width: 760px) {
  .summary-grid { grid-template-columns: 1fr; }
  .lesson-body { padding: 20px; }
}
"""


SKIP_PREFIXES = (
    "Dưới đây là nội dung",
    "Ghi chú cho người dùng",
    "*Ghi chú cho người dùng",
    "Toàn bộ 40 buổi",
)


def clean_title(title: str) -> str:
    return title.strip().strip("*").strip()


def clean_artifacts(text: str) -> str:
    text = text.replace("[cite_start]", "")
    text = re.sub(r"\s*\[cite:\s*[^\]]+\]", "", text)
    return text


def should_skip_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if re.fullmatch(r"[-_*]{3,}", stripped):
        return True
    return any(stripped.startswith(prefix) for prefix in SKIP_PREFIXES)


def extract_lessons(text: str) -> dict[int, str]:
    matches = list(LESSON_HEADING_RE.finditer(text))
    lessons: dict[int, str] = {}

    for index, match in enumerate(matches):
        lesson_no = int(match.group(1))
        if lesson_no in lessons:
            continue

        start = text.find("\n", match.end())
        if start == -1:
            start = match.end()
        else:
            start += 1

        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        raw_body = text[start:end]
        lines = [line.rstrip() for line in raw_body.splitlines() if not should_skip_line(line)]
        lessons[lesson_no] = "\n".join(lines).strip()

    return lessons


def inline_markdown(text: str) -> str:
    parts = re.split(r"(`[^`]*`)", text)
    rendered: list[str] = []

    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            rendered.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue

        escaped = html.escape(part)
        escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
        escaped = re.sub(r"(?<!\*)\*([^\s*\n](?:[^*\n]*?[^\s*\n])?)\*(?!\*)", r"<em>\1</em>", escaped)
        escaped = escaped.replace(" * <em>", " <em>")
        rendered.append(escaped)

    return "".join(rendered).replace("**", "")


def illustration_details(note: str) -> tuple[str, str, str, str]:
    lower = note.lower()

    rules: list[tuple[tuple[str, ...], tuple[str, str, str, str]]] = [
        (("file .cpp", "trình biên dịch"), (
            "Vẽ 3 ô lớn theo chiều trái sang phải: `hello.cpp` -> `Compiler` -> `hello.exe / Console`. Cho học sinh tự điền mũi tên `Viết code`, `Biên dịch`, `Chạy`.",
            "Dùng chương trình `cout << \"Xin chao\";`, sau đó cố tình xóa dấu `;` để chỉ ra lỗi nằm ở bước biên dịch, chưa phải lỗi khi chạy.",
            "Chốt rằng C++ không chạy trực tiếp file `.cpp`; code phải qua compiler trước.",
            "Nếu chương trình báo lỗi trước khi hiện màn hình console, lỗi đang ở giai đoạn nào?",
        )),
        (("endl", "console"), (
            "Vẽ hai khung console đặt cạnh nhau: khung 1 in ba câu dính liền, khung 2 in ba câu mỗi câu một dòng.",
            "So sánh `cout << \"A\" << \"B\";`, `cout << \"A\\nB\";` và `cout << \"A\" << endl << \"B\";`.",
            "Chốt rằng `endl` và `\\n` đều giúp xuống dòng, nhưng phải đặt đúng vị trí trong output.",
            "Nếu muốn in họ tên ở dòng 1, lớp ở dòng 2, cần thêm gì vào câu lệnh `cout`?",
        )),
        (("chiếc hộp", "tuổi", "điểm", "tên"), (
            "Vẽ các hộp có nhãn `age`, `score`, `name`. Bên trong mỗi hộp ghi đúng kiểu dữ liệu: `15`, `8.5`, `\"Nam\"`.",
            "Cho học sinh thử đặt sai: `int score = 8.5;` rồi hỏi phần `.5` có còn ý nghĩa không.",
            "Chốt rằng biến phải có tên, có kiểu và có giá trị; kiểu dữ liệu quyết định biến chứa được loại thông tin nào.",
            "Dữ liệu `Nguyen Van An` nên để trong kiểu nào, và nhập bằng `cin` hay `getline`?",
        )),
        (("bộ đệm", "cin.ignore"), (
            "Vẽ hàng chờ bàn phím gồm `15`, `Enter`, `Nguyen Van A`. Khoanh ký tự `Enter` còn sót lại sau `cin >> age`.",
            "Chạy ví dụ nhập tuổi trước, họ tên sau. Lần 1 bỏ `cin.ignore()`, lần 2 thêm `cin.ignore()` để học sinh thấy khác biệt.",
            "Chốt rằng `getline` đọc cả dòng, nên ký tự Enter còn trong bộ đệm có thể làm nó đọc dòng rỗng.",
            "Khi nào cần đặt `cin.ignore()` trước `getline`?",
        )),
        (("thứ tự ưu tiên", "nhân/chia", "cộng/trừ"), (
            "Vẽ tháp ưu tiên 3 tầng: tầng 1 `()`, tầng 2 `* / %`, tầng 3 `+ -`. Mũi tên đi từ tầng trên xuống tầng dưới.",
            "Cho học sinh tính tay 3 biểu thức: `2 + 3 * 4`, `(2 + 3) * 4`, `20 / 5 + 6 * 2`. Gạch chân phép được tính trước ở từng bước.",
            "Chốt rằng dấu ngoặc có quyền ưu tiên cao nhất; nhân/chia/chia dư làm trước cộng/trừ; cùng mức thì thường tính từ trái sang phải.",
            "Trong biểu thức `10 - 2 * 3 + 4`, phép nào được thực hiện đầu tiên và vì sao?",
        )),
        (("thương", "số dư", "dấu %"), (
            "Vẽ phép chia tiểu học `17 : 5 = 3 dư 2`, tô màu `3` là thương và `2` là số dư.",
            "Đặt cạnh biểu thức C++: `17 / 5 == 3` và `17 % 5 == 2`. Sau đó thử thêm `20 / 5` và `20 % 5`.",
            "Chốt rằng `/` với số nguyên lấy phần nguyên, `%` lấy phần dư; `%` rất hữu ích để kiểm tra chẵn lẻ và chia hết.",
            "Nếu `n % 2 == 0`, ta kết luận được điều gì về `n`?",
        )),
        (("flowchart", "lệnh if"), (
            "Vẽ hình thoi `Điều kiện đúng?`, nhánh trái `true`, nhánh phải `false`, mỗi nhánh đi tới một hành động khác nhau.",
            "Dùng tình huống `score >= 5`: đúng thì in `Dat`, sai thì in `Chua dat`. Cho học sinh thử với `4.9`, `5.0`, `8.0`.",
            "Chốt rằng `if` không phải phép tính, mà là điểm ra quyết định dựa trên điều kiện đúng/sai.",
            "Tại sao bài kiểm tra điểm phải thử đúng mốc `5.0`, không chỉ thử `4` và `8`?",
        )),
        (("menu nhà hàng", "switch"), (
            "Vẽ menu nhà hàng: `1. Com`, `2. Pho`, `3. Bun`, `0. Thoat`. Nối từng số với một `case` tương ứng.",
            "Cho học sinh nhập `choice = 2`, lần theo code để thấy chương trình nhảy đúng vào `case 2`.",
            "Chốt rằng `switch` phù hợp khi lựa chọn là các giá trị rời rạc, và `break` giúp dừng sau khi xử lý xong một case.",
            "Nếu quên `break` sau `case 1`, điều gì có thể xảy ra?",
        )),
        (("vòng lặp for", "khởi tạo"), (
            "Vẽ vòng tròn gồm 4 bước: `i = 1` -> `i <= n?` -> `thân vòng lặp` -> `i++` -> quay lại kiểm tra.",
            "Minh họa với `for (int i = 1; i <= 5; i++)`, ghi bảng giá trị `i` qua từng lượt: 1, 2, 3, 4, 5.",
            "Chốt rằng `for` dùng tốt khi biết trước số lần lặp, và cần kiểm tra kỹ điều kiện dừng.",
            "Muốn in từ 1 đến 10 thì điều kiện là `i < 10` hay `i <= 10`?",
        )),
        (("while", "do-while"), (
            "Vẽ hai luồng cạnh nhau: `while` kiểm tra điều kiện trước khi làm, `do-while` làm một lần rồi mới kiểm tra.",
            "Dùng bài nhập mật khẩu: `while` có thể không chạy nếu điều kiện sai từ đầu; `do-while` luôn hỏi người dùng ít nhất một lần.",
            "Chốt rằng `while` hợp với lặp chưa biết số lần, còn `do-while` hợp với menu hoặc nhập liệu cần chạy tối thiểu một lần.",
            "Vì sao menu chương trình thường dùng `do-while`?",
        )),
        (("ngăn kéo", "mảng"), (
            "Vẽ một tủ có các ngăn đánh số `0, 1, 2, 3, 4`. Mỗi ngăn chứa một điểm số.",
            "Cho học sinh truy cập `scores[0]`, `scores[2]`, rồi hỏi vì sao phần tử đầu tiên không phải `scores[1]`.",
            "Chốt rằng mảng lưu nhiều giá trị cùng kiểu và chỉ số bắt đầu từ 0.",
            "Nếu mảng có 5 phần tử, chỉ số cuối cùng là bao nhiêu?",
        )),
        (("máy xay sinh tố", "tham số", "return"), (
            "Vẽ máy xay: nguyên liệu đi vào là tham số, thân máy là phần xử lý, ly sinh tố đi ra là giá trị `return`.",
            "So sánh hàm `int tong(int a, int b)` với máy nhận `a`, `b`, xử lý `a + b`, trả về kết quả.",
            "Chốt rằng hàm nên làm một nhiệm vụ rõ ràng, có đầu vào và đầu ra dễ hiểu.",
            "Hàm kiểm tra số chẵn nên trả về kiểu dữ liệu nào?",
        )),
        (("lưới excel", "dòng", "cột"), (
            "Vẽ bảng 3 dòng 4 cột, ghi chỉ số dòng bên trái và chỉ số cột phía trên.",
            "Cho học sinh xác định ô `a[1][2]` bằng cách đi tới dòng 1, cột 2. Sau đó duyệt bằng hai vòng lặp lồng nhau.",
            "Chốt rằng mảng hai chiều phù hợp với dữ liệu dạng bảng: điểm nhiều học sinh, nhiều môn.",
            "Muốn tính tổng một dòng trong ma trận, vòng lặp nào giữ nguyên và vòng lặp nào thay đổi?",
        )),
        (("array", "vector", "túi cao su"), (
            "Vẽ mảng như hộp cố định có 5 ô, vector như túi có thể thêm đồ vào cuối.",
            "Minh họa `push_back`: mỗi lần thêm một điểm, vector tăng `size()` thêm 1.",
            "Chốt rằng vector linh hoạt hơn mảng khi chưa biết trước số lượng dữ liệu.",
            "Nếu không biết học sinh sẽ nhập bao nhiêu điểm, nên dùng mảng cố định hay vector?",
        )),
        (("bong bóng", "bubble"), (
            "Vẽ dãy số thành các bong bóng. Mỗi lượt chỉ so sánh hai bong bóng đứng cạnh nhau.",
            "Dùng dãy `5, 2, 8, 1`. Cho học sinh đổi chỗ từng cặp sai thứ tự và quan sát số lớn nổi dần về cuối.",
            "Chốt rằng Bubble Sort dễ hiểu vì chỉ cần so sánh cặp liền kề, nhưng không phải cách nhanh nhất cho dữ liệu lớn.",
            "Sau lượt duyệt đầu tiên của Bubble Sort tăng dần, phần tử nào thường nằm đúng ở cuối dãy?",
        )),
        (("linear search", "mở cửa từng tủ"), (
            "Vẽ một dãy tủ, người tìm kiếm mở lần lượt từ trái sang phải.",
            "Dùng danh sách `An, Binh, Chi, Dung`, tìm `Chi`: kiểm tra An, Binh, rồi mới thấy Chi.",
            "Chốt rằng Linear Search không cần dữ liệu sắp xếp, nhưng có thể phải duyệt hết danh sách.",
            "Nếu tìm phần tử không tồn tại, Linear Search sẽ kiểm tra bao nhiêu phần tử?",
        )),
        (("hello world", "ô vuông", "chỉ số"), (
            "Vẽ chuỗi thành các ô ký tự: `H`, `E`, `L`, `L`, `O`, khoảng trắng, `W`... bên dưới ghi chỉ số 0, 1, 2...",
            "Cho học sinh đọc `s[0]`, `s[4]`, `s.length()`, rồi thử duyệt từng ký tự bằng vòng lặp.",
            "Chốt rằng string có thể xem như một dãy ký tự, truy cập được bằng chỉ số.",
            "Trong chuỗi `CODE`, ký tự ở chỉ số 2 là gì?",
        )),
        (("caesar", "bảng chữ cái"), (
            "Vẽ hai vòng chữ cái: vòng ngoài là chữ gốc, vòng trong lệch 3 vị trí là chữ sau mã hóa.",
            "Mã hóa `A -> D`, `B -> E`, `C -> F`, rồi thử từ `CAT` thành `FDW`.",
            "Chốt rằng Caesar Cipher là dịch ký tự theo một số bước cố định trong bảng chữ cái.",
            "Nếu dịch 3 bước, chữ `Z` cần quay vòng về chữ nào?",
        )),
        (("prototype", "hàm main", "hàm con"), (
            "Vẽ bố cục file C++ như mục lục sách: include ở đầu, prototype như mục lục, `main` là phần điều phối, các hàm con là chương chi tiết.",
            "Cho học sinh nhìn một file có `void menu();` trước `main`, thân hàm `menu()` viết sau `main`.",
            "Chốt rằng prototype giúp compiler biết trước tên hàm và kiểu tham số trước khi gặp phần định nghĩa thật.",
            "Nếu gọi một hàm trước khi định nghĩa mà không có prototype, compiler có thể báo gì?",
        )),
        (("hiện menu", "switch", "quay lại"), (
            "Vẽ luồng: Start -> hiện menu -> nhập lựa chọn -> `switch` -> gọi hàm xử lý -> quay lại menu hoặc thoát.",
            "Dùng menu 1 thêm, 2 xem, 0 thoát. Lần theo lựa chọn `1` để thấy chương trình chạy hàm thêm rồi quay lại menu.",
            "Chốt rằng menu console thường kết hợp `do-while` và `switch-case`.",
            "Biến nào nên dùng để lưu lựa chọn của người dùng trong menu?",
        )),
        (("tham trị", "tham chiếu"), (
            "Vẽ hai cảnh: tham trị là bản photocopy, tham chiếu là cùng sửa một tài liệu gốc.",
            "Chạy hàm `tang(x)` bản tham trị và bản tham chiếu `tang(int &x)` để so sánh giá trị `x` sau khi gọi hàm.",
            "Chốt rằng tham trị không làm đổi biến gốc, tham chiếu có thể làm đổi biến gốc.",
            "Khi muốn hàm hoán đổi hai biến thật sự, cần truyền tham trị hay tham chiếu?",
        )),
        (("v.erase", "trượt lên"), (
            "Vẽ vector như hàng gạch. Khi xóa viên ở giữa, các viên phía sau trượt lên lấp chỗ trống.",
            "Dùng vector `{10, 20, 30, 40}`, xóa phần tử chỉ số 1, kết quả còn `{10, 30, 40}`.",
            "Chốt rằng sau khi xóa, kích thước vector giảm và chỉ số các phần tử phía sau thay đổi.",
            "Sau khi xóa `v[1]`, phần tử cũ ở `v[2]` sẽ chuyển về chỉ số nào?",
        )),
        (("id card", "struct"), (
            "Vẽ thẻ học sinh gồm nhiều ô: mã, họ tên, tuổi, điểm. Tất cả nằm trong một khung duy nhất.",
            "Ánh xạ sang `struct Student { string id; string name; double score; };`.",
            "Chốt rằng struct đóng gói nhiều dữ liệu liên quan vào một kiểu mới dễ quản lý.",
            "Vì sao danh sách học sinh nên dùng `vector<Student>` thay vì nhiều vector rời rạc?",
        )),
        (("ofstream", "file .txt", "đóng van"), (
            "Vẽ dữ liệu từ RAM chảy qua ống `ofstream` vào file `.txt`; chiều ngược lại dùng `ifstream`.",
            "Minh họa ghi một danh sách 3 học sinh ra file rồi đọc lại để in lên console.",
            "Chốt rằng file giúp dữ liệu không mất sau khi tắt chương trình, nhưng phải kiểm tra mở file thành công.",
            "Nếu file không mở được, chương trình nên tiếp tục xử lý hay báo lỗi?",
        )),
        (("mindmap", "quản lý cửa hàng"), (
            "Vẽ mindmap từ bài toán lớn -> đối tượng -> trường dữ liệu -> chức năng.",
            "Ví dụ `Quản lý cửa hàng` -> `Sản phẩm` -> `mã, tên, giá, số lượng` -> `thêm, sửa, xóa, tìm, thống kê`.",
            "Chốt rằng thiết kế dữ liệu trước giúp code ít sửa lại và dễ bảo vệ sản phẩm.",
            "Với đề tài quản lý thư viện, đối tượng chính và các trường dữ liệu là gì?",
        )),
        (("robot", "sửa", "xóa"), (
            "Vẽ robot đi dọc vector, quét từng mã. Khi mã khớp, robot dừng lại để sửa nhãn hoặc gắp phần tử ra.",
            "Minh họa tìm `id = 103` trong danh sách sản phẩm rồi cho phép sửa `price` hoặc xóa sản phẩm.",
            "Chốt rằng sửa/xóa thường bắt đầu bằng bước tìm vị trí phần tử cần thao tác.",
            "Nếu không tìm thấy mã, chương trình nên in thông báo gì?",
        )),
        (("id", "tên", "3 người"), (
            "Vẽ bảng hai cột: tìm theo ID trả về một người duy nhất, tìm theo tên có thể trả về nhiều người.",
            "Cho ví dụ `id = SV03` chỉ có một kết quả, nhưng tên `An` có thể có `Nguyen An`, `Le An`, `Tran An`.",
            "Chốt rằng tìm theo mã thường là chính xác, tìm theo tên cần chuẩn bị trường hợp nhiều kết quả.",
            "Hàm tìm theo mã nên trả về một vị trí hay một danh sách vị trí?",
        )),
        (("min/max", "bục"), (
            "Vẽ một bục `max hiện tại`. Đặt phần tử đầu tiên lên bục, sau đó từng phần tử còn lại thách đấu.",
            "Dùng dãy `7, 3, 9, 5`: bắt đầu max = 7, gặp 9 thì thay max, gặp 5 thì giữ nguyên.",
            "Chốt rằng tìm min/max cần một biến lưu ứng viên tốt nhất hiện tại.",
            "Vì sao không nên khởi tạo max bằng 0 nếu dữ liệu có thể toàn số âm?",
        )),
        (("khối hộp", "struct", "hoán đổi"), (
            "Vẽ mỗi struct là một khối gồm mã, tên, điểm. Khi sắp xếp, đổi cả khối chứ không chỉ đổi điểm.",
            "Cho hai học sinh `A - 9.0` và `B - 7.5`; nếu sắp xếp giảm dần thì cả record của A đứng trước B.",
            "Chốt rằng sắp xếp struct phải giữ dữ liệu của một đối tượng đi cùng nhau.",
            "Nếu chỉ đổi trường điểm mà không đổi tên, dữ liệu sẽ sai như thế nào?",
        )),
        (("tiến lên", "insertion"), (
            "Vẽ tay bài đã xếp `3, 5, 8`, rút lá `6`, trượt qua `8` rồi chèn giữa `5` và `8`.",
            "Ánh xạ sang Insertion Sort: phần bên trái đã sắp xếp, phần tử mới được chèn vào đúng vị trí.",
            "Chốt rằng Insertion Sort dễ hiểu khi tưởng tượng sắp xếp bài trên tay.",
            "Khi chèn số `4` vào dãy đã xếp `1, 3, 5, 7`, những số nào phải dịch sang phải?",
        )),
        (("binary search", "left", "right", "mid"), (
            "Vẽ một dãy đã sắp xếp, đánh dấu `left`, `right`, `mid`. Sau mỗi lần so sánh, gạch bỏ nửa không thể chứa đáp án.",
            "Tìm `40` trong `{10, 20, 30, 40, 50, 60}`: tính `mid`, so sánh, rồi thu hẹp phạm vi.",
            "Chốt rằng Binary Search chỉ đúng khi dữ liệu đã sắp xếp.",
            "Nếu dữ liệu chưa sắp xếp, vì sao không thể bỏ nửa trái hoặc nửa phải một cách chắc chắn?",
        )),
        (("comparator", "cân"), (
            "Vẽ chiếc cân nhận hai học sinh A và B, nhưng chỉ nhìn vào trường `score` hoặc `name` theo luật lập trình viên viết.",
            "Minh họa comparator `return a.score > b.score;` nghĩa là học sinh điểm cao được đứng trước.",
            "Chốt rằng comparator là quy tắc trả lời câu hỏi: phần tử nào nên đứng trước?",
            "Muốn sắp xếp giá tăng dần, comparator cần dùng dấu `<` hay `>`?",
        )),
        (("dashboard", "tổng doanh thu"), (
            "Vẽ màn hình console có tiêu đề, đường kẻ, các dòng thống kê canh hàng: tổng, số lượng, trung bình.",
            "Dùng `setw` để căn cột khi in `Ten`, `So luong`, `Gia`, `Thanh tien`.",
            "Chốt rằng output đẹp giúp demo sản phẩm dễ hiểu và chuyên nghiệp hơn.",
            "Thông tin thống kê nào nên đặt ở đầu báo cáo để người xem nắm nhanh tình hình?",
        )),
        (("nhiều tiêu chí", "so sánh điểm"), (
            "Vẽ flowchart: so sánh tiêu chí 1, nếu khác thì quyết định; nếu bằng nhau mới chuyển sang tiêu chí 2.",
            "Ví dụ sắp xếp điểm giảm dần, nếu bằng điểm thì tên tăng dần.",
            "Chốt rằng comparator nhiều tiêu chí phải xử lý rõ trường hợp bằng nhau.",
            "Nếu hai học sinh cùng điểm 8.5, tiêu chí phụ nào sẽ quyết định thứ tự?",
        )),
        (("robot", "hàm thêm", "hàm xóa", "hàm main"), (
            "Vẽ mini app như robot: `main` là thân chính, các hàm thêm/xóa/thống kê là bộ phận được gắn vào.",
            "Cho học sinh đánh dấu mỗi chức năng trong menu đang gọi hàm nào.",
            "Chốt rằng tích hợp app là ghép các hàm đã học thành một luồng sử dụng hoàn chỉnh.",
            "Nếu menu chọn 3 là tìm kiếm, hàm nào nên được gọi và dữ liệu nào được truyền vào?",
        )),
        (("thám tử", "bug", "cout"), (
            "Vẽ đường ống dữ liệu có điểm bị tắc. Kính lúp `cout` được đặt ở các bước trung gian để xem dữ liệu đang biến đổi ra sao.",
            "Chèn `cout << \"i = \" << i << endl;` hoặc `cout << \"size = \" << v.size() << endl;` để tìm lỗi logic.",
            "Chốt rằng lỗi logic không làm chương trình dừng, nhưng kết quả sai; cần in trung gian và test nhỏ để khoanh vùng.",
            "Khi kết quả tổng bị sai, nên in biến nào để kiểm tra từng bước?",
        )),
        (("canvas", "người dùng", "dữ liệu", "tính năng"), (
            "Vẽ bảng 3 cột: người dùng là ai, dữ liệu cần quản lý là gì, tính năng cần có là gì.",
            "Ví dụ app quản lý sách: người dùng là học sinh, dữ liệu là sách, tính năng là thêm/tìm/mượn/trả/thống kê.",
            "Chốt rằng dự án cuối khóa phải bắt đầu từ nhu cầu và dữ liệu, không bắt đầu bằng code ngay.",
            "Sản phẩm của em giải quyết vấn đề cụ thể nào cho người dùng?",
        )),
        (("cấu trúc file code", "libraries", "main menu"), (
            "Vẽ ba tầng: thư viện và struct ở trên, các hàm xử lý ở giữa, `main` và menu ở dưới điều phối.",
            "Cho học sinh đặt từng đoạn code của dự án vào đúng tầng để tránh file lộn xộn.",
            "Chốt rằng cấu trúc file rõ giúp dễ sửa, dễ demo và dễ trả lời khi bảo vệ.",
            "Hàm `themSach()` nên nằm trong phần nào của file?",
        )),
        (("tên biến", "soTien", "hoTen"), (
            "Đặt hai đoạn code cạnh nhau: bên trái `a, b, c`, bên phải `soTien, hoTen, diemTrungBinh`.",
            "Cho học sinh đọc từng đoạn và hỏi đoạn nào dễ hiểu hơn khi quay lại sau một tuần.",
            "Chốt rằng tên biến rõ nghĩa là một phần của chất lượng sản phẩm, không chỉ là thẩm mỹ.",
            "Biến lưu số lượng sách nên đặt tên là `x` hay `soLuongSach`?",
        )),
        (("bảng excel", "dấu sổ dọc"), (
            "Vẽ output console dạng bảng với đường kẻ ngang và cột `Ma`, `Ten`, `Diem`.",
            "Minh họa dùng `setw` để các cột không bị lệch khi tên dài/ngắn khác nhau.",
            "Chốt rằng làm đẹp output giúp người xem demo hiểu dữ liệu nhanh hơn.",
            "Cột nào nên canh trái, cột nào nên canh phải trong bảng sản phẩm?",
        )),
        (("kịch bản demo", "máy chiếu"), (
            "Vẽ trình tự demo 5 bước: giới thiệu bài toán, mở app, chạy chức năng chính, xử lý tình huống lỗi, kết luận.",
            "Cho học sinh tập nói thử trong 3 phút với dữ liệu mẫu đã chuẩn bị sẵn.",
            "Chốt rằng demo tốt không chỉ là code chạy, mà còn là biết dẫn người xem qua sản phẩm.",
            "Trong 5 phút demo, em sẽ chọn 3 chức năng nào để trình bày?",
        )),
        (("rubric", "kỹ năng lập trình"), (
            "Vẽ bảng chấm điểm gồm 3 cột: lập trình, trình bày, hỏi đáp; mỗi cột có thang điểm và tiêu chí rõ.",
            "Cho học sinh tự chấm thử sản phẩm của mình trước khi bảo vệ thật.",
            "Chốt rằng bảo vệ sản phẩm đánh giá cả code chạy, cách giải thích và khả năng trả lời câu hỏi.",
            "Nếu app chạy được nhưng học sinh không giải thích được code, phần điểm nào sẽ bị ảnh hưởng?",
        )),
    ]

    for keywords, detail in rules:
        if all(keyword in lower for keyword in keywords):
            return detail

    return (
        "Chuyển mô tả này thành một sơ đồ đơn giản trên bảng: chia thành các khối, mũi tên và nhãn ngắn để học sinh nhìn được luồng xử lý.",
        "Sau khi vẽ, gắn ngay với một đoạn code hoặc một bộ dữ liệu nhỏ trong bài để học sinh không chỉ nhìn hình mà còn biết áp dụng.",
        "Chốt lại bằng một câu: minh họa này tương ứng với khái niệm nào trong C++ và khi nào cần dùng.",
        "Yêu cầu học sinh tự tạo thêm một ví dụ tương tự rồi giải thích lại bằng lời.",
    )


def render_image_note(note: str) -> str:
    draw, example, takeaway, question = illustration_details(note)
    return f"""
<div class="image-note">
  <strong>Minh họa chi tiết</strong>
  <p><em>Ý tưởng trực quan:</em> {inline_markdown(note)}</p>
  <ul>
    <li><strong>Cách trình bày:</strong> {inline_markdown(draw)}</li>
    <li><strong>Ví dụ thao tác:</strong> {inline_markdown(example)}</li>
    <li><strong>Điểm cần chốt:</strong> {inline_markdown(takeaway)}</li>
    <li><strong>Câu hỏi kiểm tra nhanh:</strong> {inline_markdown(question)}</li>
  </ul>
</div>
"""


def section_heading(line: str) -> tuple[int, str] | None:
    match = SECTION_HEADING_RE.match(line.strip())
    if not match:
        return None

    title = match.group(2).strip()
    known = (
        "Mục tiêu",
        "Lý thuyết",
        "Ví dụ",
        "Bài tập",
        "Checklist",
        "Nội dung",
        "Tiêu chí",
        "Khung",
        "Lời kết",
    )
    if not title.startswith(known):
        return None

    return int(match.group(1)), title


def flush_paragraph(output: list[str], paragraph: list[str]) -> None:
    if not paragraph:
        return
    output.append("<p>" + "<br>".join(inline_markdown(line) for line in paragraph) + "</p>")
    paragraph.clear()


def list_tag(list_type: str) -> str:
    return list_type.split(":", 1)[0]


def close_list(output: list[str], list_type: str | None) -> None:
    if list_type:
        output.append(f"</{list_tag(list_type)}>")


def render_markdownish(body: str) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None
    in_code = False
    code_lang = ""
    code_lines: list[str] = []

    def open_list(kind: str, class_name: str | None = None) -> None:
        nonlocal list_type
        flush_paragraph(output, paragraph)
        next_type = f"{kind}:{class_name or ''}"
        if list_type == next_type:
            return
        close_list(output, list_type)
        list_type = next_type
        class_attr = f' class="{class_name}"' if class_name else ""
        output.append(f"<{kind}{class_attr}>")

    for raw_line in body.splitlines():
        line = clean_artifacts(raw_line.rstrip())
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                output.append(
                    f'<pre><code class="language-{html.escape(code_lang)}">'
                    + html.escape("\n".join(code_lines))
                    + "</code></pre>"
                )
                code_lines = []
                code_lang = ""
                in_code = False
            else:
                flush_paragraph(output, paragraph)
                close_list(output, list_type)
                list_type = None
                code_lang = stripped.strip("`").strip()
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not stripped:
            flush_paragraph(output, paragraph)
            close_list(output, list_type)
            list_type = None
            continue

        if stripped in {"*", "* "}:
            continue

        note_match = IMAGE_NOTE_RE.search(stripped)
        if note_match:
            flush_paragraph(output, paragraph)
            close_list(output, list_type)
            list_type = None
            output.append(render_image_note(note_match.group(1)))
            continue

        if stripped.startswith(">"):
            flush_paragraph(output, paragraph)
            close_list(output, list_type)
            list_type = None
            quote = stripped.lstrip(">").strip()
            output.append("<blockquote>" + inline_markdown(quote) + "</blockquote>")
            continue

        heading = section_heading(stripped)
        if heading:
            flush_paragraph(output, paragraph)
            close_list(output, list_type)
            list_type = None
            number, title = heading
            output.append(f"<h2>{number}. {inline_markdown(title)}</h2>")
            continue

        if stripped.startswith("#"):
            flush_paragraph(output, paragraph)
            close_list(output, list_type)
            list_type = None
            level = min(len(stripped) - len(stripped.lstrip("#")), 4)
            title = stripped.lstrip("#").strip()
            if title:
                output.append(f"<h{level}>{inline_markdown(title)}</h{level}>")
            continue

        bullet = re.match(r"^[*-]\s+(.+)$", stripped)
        if bullet:
            content = bullet.group(1).strip()
            if content.startswith("**Ví dụ"):
                flush_paragraph(output, paragraph)
                close_list(output, list_type)
                list_type = None
                output.append("<h3>" + inline_markdown(content) + "</h3>")
            else:
                checkbox = re.match(r"^\[\s*\]\s*(.+)$", content)
                if checkbox:
                    open_list("ul")
                    output.append(
                        '<li class="check-item"><span class="check-box"></span>'
                        + inline_markdown(checkbox.group(1).strip())
                        + "</li>"
                    )
                elif re.match(r"^\*\*Bài\s+\d+\s*:", content):
                    open_list("ul", "task-list")
                    output.append('<li class="task-item">' + inline_markdown(content) + "</li>")
                else:
                    open_list("ul")
                    output.append("<li>" + inline_markdown(content) + "</li>")
            continue

        ordered = ORDERED_ITEM_RE.match(stripped)
        if ordered:
            open_list("ol")
            output.append("<li>" + inline_markdown(ordered.group(2)) + "</li>")
            continue

        if re.match(r"^\*\*Bài\s+\d+\s*:", stripped):
            open_list("ul", "task-list")
            output.append('<li class="task-item">' + inline_markdown(stripped) + "</li>")
            continue

        if stripped.startswith("**Ví dụ") or stripped.startswith("Ví dụ "):
            flush_paragraph(output, paragraph)
            close_list(output, list_type)
            list_type = None
            output.append("<h3>" + inline_markdown(stripped) + "</h3>")
            continue

        if stripped.startswith("**") and stripped.endswith("**") and len(stripped) < 100:
            flush_paragraph(output, paragraph)
            close_list(output, list_type)
            list_type = None
            output.append("<h3>" + inline_markdown(stripped.strip("*")) + "</h3>")
            continue

        if list_type:
            close_list(output, list_type)
            list_type = None
        paragraph.append(stripped)

    if in_code:
        output.append(
            f'<pre><code class="language-{html.escape(code_lang)}">'
            + html.escape("\n".join(code_lines))
            + "</code></pre>"
        )
    flush_paragraph(output, paragraph)
    close_list(output, list_type)
    rendered = "\n".join(output)
    rendered = re.sub(r"</ul>\s*<ul>", "\n", rendered)
    rendered = re.sub(r"</ul>\s*<ul class=\"task-list\">", "\n", rendered)
    rendered = re.sub(r"</ul>\s*<ul class=\"task-list\">", "\n", rendered)
    rendered = re.sub(r"</ol>\s*<ol>", "\n", rendered)
    rendered = re.sub(r"\n{3,}", "\n", rendered)
    return rendered


def phase_for(index: int) -> str:
    return LESSONS[index - 1]["phase"]


def canonical_title(index: int) -> str:
    return clean_title(LESSONS[index - 1]["title"])


def is_protected(index: int) -> bool:
    return index >= PROTECTED_FROM_LESSON


def render_lock_screen(index: int, title: str) -> str:
    if not is_protected(index):
        return ""

    return f"""
  <div class="lock-screen" role="dialog" aria-modal="true" aria-labelledby="lock-title">
    <div class="lock-card">
      <span class="badge">Nội dung bảo mật</span>
      <h1 id="lock-title">Nhập mã để xem bài {index:02d}</h1>
      <p>{html.escape(title)} thuộc phần bài giảng cần mã truy cập.</p>
      <form class="lock-form" data-lock-form>
        <label for="lesson-passcode">Mã bảo mật</label>
        <input id="lesson-passcode" data-lock-input type="password" autocomplete="current-password" placeholder="Nhập mã bảo mật">
        <button type="submit">Mở bài học</button>
        <div class="lock-error" data-lock-error aria-live="polite"></div>
      </form>
    </div>
  </div>
"""


def render_lock_script(index: int) -> str:
    if not is_protected(index):
        return ""

    return f"""
  <script>
    (() => {{
      const ACCESS_KEY = "{html.escape(LOCK_STORAGE_KEY)}";
      const SECURITY_CODE = "{html.escape(SECURITY_CODE)}";

      const unlock = () => {{
        try {{
          localStorage.setItem(ACCESS_KEY, "unlocked");
        }} catch (error) {{}}
        document.body.classList.remove("lesson-locked");
      }};

      const initLessonLock = () => {{
        try {{
          if (localStorage.getItem(ACCESS_KEY) === "unlocked") {{
            unlock();
            return;
          }}
        }} catch (error) {{}}

        const form = document.querySelector("[data-lock-form]");
        const input = document.querySelector("[data-lock-input]");
        const error = document.querySelector("[data-lock-error]");

        if (input) input.focus();
        if (!form || !input || !error) return;

        form.addEventListener("submit", (event) => {{
          event.preventDefault();
          if (input.value.trim() === SECURITY_CODE) {{
            unlock();
            return;
          }}

          error.textContent = "Mã bảo mật không đúng. Vui lòng thử lại.";
          input.value = "";
          input.focus();
        }});
      }};

      if (document.readyState === "loading") {{
        document.addEventListener("DOMContentLoaded", initLessonLock);
      }} else {{
        initLessonLock();
      }}
    }})();
  </script>
"""


def render_lesson(index: int, body_html: str) -> str:
    title = canonical_title(index)
    prev_link = lesson_filename(index - 1, canonical_title(index - 1)) if index > 1 else None
    next_link = lesson_filename(index + 1, canonical_title(index + 1)) if index < len(LESSONS) else None
    prev_html = f'<a href="{prev_link}">← Bài trước</a>' if prev_link else "<span></span>"
    next_html = f'<a href="{next_link}">Bài sau →</a>' if next_link else "<span></span>"
    body_class = ' class="lesson-protected lesson-locked"' if is_protected(index) else ""
    lock_screen = render_lock_screen(index, title)
    lock_script = render_lock_script(index)

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Buổi {index:02d} - {html.escape(title)}</title>
  <style>{STYLE}{EXTRA_STYLE}</style>
</head>
<body{body_class}>
{lock_screen}
  <div class="wrap">
    <div class="topbar">
      <a class="brand" href="index.html">GiaSuTHT · Bài giảng C++</a>
      <div class="nav">
        <a href="../khoa-hoc-cpp-nentang.html">Trang khóa học</a>
        <a href="index.html">Mục lục</a>
      </div>
    </div>

    <header class="hero">
      <span class="badge">{html.escape(phase_for(index))}</span>
      <h1>Buổi {index:02d}: {html.escape(title)}</h1>
      <p class="note">Bài giảng chi tiết cho tiết học 90 phút: lý thuyết, ví dụ code, giải thích từng bước, bài tập trên lớp và bài tập về nhà.</p>
      <div class="summary-grid">
        <div class="card"><strong>Lý thuyết</strong>Nội dung được triển khai chi tiết theo từng khái niệm.</div>
        <div class="card"><strong>Code mẫu</strong>Các ví dụ C++ console có giải thích từng bước.</div>
        <div class="card"><strong>Thực hành</strong>Bài tập trên lớp và bài tập về nhà rõ yêu cầu.</div>
      </div>
    </header>

    <section class="lesson-body">
      {body_html}
    </section>

    <div class="pager">
      {prev_html}
      {next_html}
    </div>
  </div>
{lock_script}
</body>
</html>
"""


def render_index() -> str:
    rows = []
    for index, lesson in enumerate(LESSONS, start=1):
        title = clean_title(lesson["title"])
        filename = lesson_filename(index, title)
        rows.append(
            f"<tr><td>Buổi {index:02d}</td><td><a href=\"{filename}\">{html.escape(title)}</a></td><td>{html.escape(lesson['phase'])}</td></tr>"
        )

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mục lục bài giảng C++</title>
  <style>{STYLE}{EXTRA_STYLE}</style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <a class="brand" href="../khoa-hoc-cpp-nentang.html">GiaSuTHT · Khóa C++</a>
      <div class="nav">
        <a href="../index.html">Trang chủ</a>
        <a href="../khoa-hoc-cpp-nentang.html">Trang khóa học</a>
      </div>
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
    source_text = SOURCE.read_text(encoding="utf-8")
    extracted = extract_lessons(source_text)
    missing = [index for index in range(1, len(LESSONS) + 1) if index not in extracted]
    if missing:
        raise SystemExit(f"Missing lesson content for: {missing}")

    OUT_DIR.mkdir(exist_ok=True)
    for index in range(1, len(LESSONS) + 1):
        body_html = render_markdownish(extracted[index])
        filename = lesson_filename(index, canonical_title(index))
        (OUT_DIR / filename).write_text(render_lesson(index, body_html), encoding="utf-8")

    (OUT_DIR / "index.html").write_text(render_index(), encoding="utf-8")
    print(f"Imported {len(LESSONS)} lessons from {SOURCE.name} into {OUT_DIR}")


if __name__ == "__main__":
    main()
