from __future__ import annotations

import html
import re
import sys
import unicodedata
from pathlib import Path

from generate_cpp_lessons import STYLE


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "Slide"
OUT_DIR = ROOT / "bai-giang-python-nentang"
LESSON_COUNT = 32
PROTECTED_FROM_LESSON = 5
SECURITY_CODE = "PYTHON"
LOCK_STORAGE_KEY = "giasutht_python_lessons_unlocked"

LESSON_RE = re.compile(r"^Buổi\s+(\d{2}):\s*(.+?)\s*$", re.MULTILINE)
SECTION_RE = re.compile(r"^([1-7])\.\s+(.+)$")
EXAMPLE_RE = re.compile(r"^(Ví dụ|Bước)\s+\d+[:：]\s*(.+)$", re.IGNORECASE)
NUMBERED_RE = re.compile(r"^(\d+)\.\s+(.+)$")

KNOWN_SECTION_PREFIXES = (
    "Mục tiêu",
    "Lý thuyết",
    "Ví dụ",
    "Lỗi",
    "Bài tập",
    "Học sinh",
    "Hướng dẫn",
    "Một số",
    "Thực hành",
    "Tổng kết",
    "Các bước",
    "Hoạt động",
    "Chuẩn bị",
)

SKIP_LINES = {
    "Mục đích",
    "Code Python",
    "Code Python mẫu",
    "Giải thích chi tiết",
    "Tác dụng",
    "Kỹ thuật",
}

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
  margin-top: 26px;
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
  background: radial-gradient(circle at top left, rgba(34,197,94,.16), transparent 38%), rgba(5,8,22,.96);
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
  border-color: rgba(34,197,94,.7);
  box-shadow: 0 0 0 3px rgba(34,197,94,.12);
}
.lock-form button {
  border: 0;
  border-radius: 10px;
  padding: 12px 14px;
  background: linear-gradient(135deg, #22c55e, #06b6d4);
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
.example-title {
  border-left: 3px solid var(--accent);
  background: rgba(34,197,94,.08);
  border-radius: 12px;
  padding: 12px 14px;
}
.project-note {
  border-left: 3px solid var(--warn);
  background: rgba(245,158,11,.08);
  border-radius: 12px;
  padding: 12px 14px;
}
.lesson-index-table td:first-child {
  width: 96px;
  color: var(--warn);
  font-weight: 800;
}
@media (max-width: 760px) {
  .summary-grid { grid-template-columns: 1fr; }
  .lesson-body { padding: 20px; }
  .lesson-index-table thead { display: none; }
  .lesson-index-table tr { display: block; padding: 12px 0; border-bottom: 1px solid var(--border); }
  .lesson-index-table td { display: block; border-bottom: 0; padding: 4px 0; }
}
"""


def phase_for(index: int) -> str:
    if index <= 8:
        return "Giai đoạn 1 - Làm quen Python và tư duy code"
    if index <= 16:
        return "Giai đoạn 2 - Dữ liệu, chuỗi, danh sách và Turtle"
    if index <= 24:
        return "Giai đoạn 3 - Game, dữ liệu và file cơ bản"
    return "Giai đoạn 4 - Mini app, sản phẩm demo và bảo vệ sản phẩm"


def slugify(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def lesson_filename(index: int, title: str) -> str:
    return f"buoi-{index:02d}-{slugify(title)}.html"


def source_files() -> list[Path]:
    files = [path for path in SOURCE_DIR.glob("*.txt") if "Giáo án" in path.name]

    def start_lesson(path: Path) -> int:
        text = path.read_text(encoding="utf-8")
        match = LESSON_RE.search(text)
        return int(match.group(1)) if match else 999

    return sorted(files, key=start_lesson)


def clean_text(text: str) -> str:
    text = re.sub(r"\s*\[cite(?::\s*[^\]]+)?\]", "", text)
    text = re.sub(r"(?m)^_{5,}\s*$", "", text)
    text = text.replace("\ufeff", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text


def extract_lessons(text: str) -> dict[int, dict[str, str]]:
    matches = list(LESSON_RE.finditer(text))
    lessons: dict[int, dict[str, str]] = {}
    for pos, match in enumerate(matches):
        index = int(match.group(1))
        title = match.group(2).strip()
        start = match.end()
        end = matches[pos + 1].start() if pos + 1 < len(matches) else len(text)
        lessons[index] = {"title": title, "body": text[start:end].strip()}
    return lessons


def is_section_heading(line: str) -> bool:
    match = SECTION_RE.match(line)
    if not match:
        return False
    title = match.group(2).strip()
    return title.startswith(KNOWN_SECTION_PREFIXES)


def is_code_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    code_prefixes = (
        "print(",
        "input(",
        "if ",
        "elif ",
        "else:",
        "for ",
        "while ",
        "def ",
        "return ",
        "import ",
        "try:",
        "except ",
        "break",
        "continue",
        "pass",
        "with open",
    )
    code_markers = (
        "=",
        ".append(",
        ".remove(",
        ".sort(",
        ".items(",
        ".write(",
        ".read(",
        ".close(",
        "random.",
        "json.",
        ".penup(",
        ".pendown(",
        ".goto(",
        ".circle(",
        ".forward(",
        ".left(",
        ".right(",
        ".begin_fill(",
        ".end_fill(",
    )
    if stripped.startswith("#"):
        return True
    if stripped.startswith(code_prefixes):
        return True
    if stripped in {"}", "]", ")"}:
        return True
    if stripped.startswith(("rua.", "turtle.", "so_tay.", "file.")):
        return True
    if any(marker in stripped for marker in code_markers):
        if not stripped.startswith(("*", "-", "Cách sửa", "Nguyên nhân", "Sai:", "Đúng:")):
            return True
    if re.match(r"^[a-zA-Z_][\w_]*\s*=\s*.+$", stripped):
        return True
    return False


def close_lists(parts: list[str], list_state: str | None) -> None:
    if list_state:
        parts.append(f"</{list_state}>")


def render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def render_body(markdownish: str) -> str:
    parts: list[str] = []
    list_state: str | None = None
    code_lines: list[str] = []

    def flush_code() -> None:
        nonlocal code_lines
        if code_lines:
            close_lists(parts, list_state)
            parts.append(f'<pre><code class="language-python">{html.escape("\n".join(code_lines).rstrip())}</code></pre>')
            code_lines = []

    def set_list(kind: str) -> None:
        nonlocal list_state
        if list_state != kind:
            close_lists(parts, list_state)
            parts.append(f"<{kind}>")
            list_state = kind

    for raw_line in markdownish.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_code()
            continue
        if stripped in SKIP_LINES:
            flush_code()
            close_lists(parts, list_state)
            list_state = None
            continue

        if is_code_line(line):
            close_lists(parts, list_state)
            list_state = None
            code_lines.append(stripped)
            continue

        flush_code()

        if is_section_heading(stripped):
            close_lists(parts, list_state)
            list_state = None
            match = SECTION_RE.match(stripped)
            assert match
            parts.append(f"<h2>{html.escape(match.group(1))}. {html.escape(match.group(2).strip())}</h2>")
            continue

        example_match = EXAMPLE_RE.match(stripped)
        if example_match:
            close_lists(parts, list_state)
            list_state = None
            parts.append(f'<h3 class="example-title">{html.escape(stripped)}</h3>')
            continue

        if stripped.startswith("* "):
            set_list("ul")
            parts.append(f"<li>{render_inline(stripped[2:].strip())}</li>")
            continue

        if stripped.startswith("- "):
            set_list("ul")
            parts.append(f"<li>{render_inline(stripped[2:].strip())}</li>")
            continue

        numbered_match = NUMBERED_RE.match(stripped)
        if numbered_match:
            set_list("ol")
            parts.append(f"<li>{render_inline(numbered_match.group(2).strip())}</li>")
            continue

        close_lists(parts, list_state)
        list_state = None
        class_name = ' class="project-note"' if stripped.startswith(("Bước ", "Nguyên tắc", "Thực hành cá nhân", "Kiểm tra chéo")) else ""
        parts.append(f"<p{class_name}>{render_inline(stripped)}</p>")

    flush_code()
    close_lists(parts, list_state)
    return "\n".join(parts)


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


def render_lesson(index: int, title: str, body_html: str, titles: dict[int, str]) -> str:
    prev_link = lesson_filename(index - 1, titles[index - 1]) if index > 1 else None
    next_link = lesson_filename(index + 1, titles[index + 1]) if index < LESSON_COUNT else None
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
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <meta name="theme-color" content="#22c55e">
  <style>{STYLE}{EXTRA_STYLE}</style>
</head>
<body{body_class}>
{lock_screen}
  <div class="wrap">
    <div class="topbar">
      <a class="brand" href="index.html">GiaSuTHT · Bài giảng Python</a>
      <div class="nav">
        <a href="../index.html#pathways">Khóa Python</a>
        <a href="index.html">Mục lục</a>
      </div>
    </div>

    <header class="hero">
      <span class="badge">{html.escape(phase_for(index))}</span>
      <h1>Buổi {index:02d}: {html.escape(title)}</h1>
      <p class="note">Bài giảng chi tiết cho tiết học 90 phút: lý thuyết dễ hiểu, ví dụ code Python, lỗi thường gặp, thực hành trên lớp và bài tập về nhà.</p>
      <div class="summary-grid">
        <div class="card"><strong>Lý thuyết</strong>Diễn giải bằng ngôn ngữ gần gũi cho học sinh mới học lập trình.</div>
        <div class="card"><strong>Code mẫu</strong>Ví dụ Python 3 có giải thích từng bước, ưu tiên rõ ràng và dễ sửa.</div>
        <div class="card"><strong>Thực hành</strong>Bài tập trên lớp, bài tập về nhà và mục học sinh tự nói lại.</div>
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


def render_index(titles: dict[int, str]) -> str:
    rows = []
    for index in range(1, LESSON_COUNT + 1):
        title = titles[index]
        filename = lesson_filename(index, title)
        rows.append(
            f'<tr><td>Buổi {index:02d}</td><td><a href="{filename}">{html.escape(title)}</a></td><td>{html.escape(phase_for(index))}</td></tr>'
        )

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mục lục bài giảng Python tư duy</title>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <meta name="theme-color" content="#22c55e">
  <style>{STYLE}{EXTRA_STYLE}</style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <a class="brand" href="../index.html#pathways">GiaSuTHT · Khóa Python</a>
      <div class="nav">
        <a href="../index.html">Trang chủ</a>
        <a href="../index.html#pathways">Khóa học</a>
      </div>
    </div>
    <header class="hero">
      <span class="badge">Bộ bài giảng HTML</span>
      <h1>Lập Trình Python Tư Duy</h1>
      <p class="note">Bộ 32 bài giảng chi tiết, đi từ những dòng Python đầu tiên đến mini app và sản phẩm demo cuối khóa.</p>
    </header>
    <section>
      <h2>Mục lục</h2>
      <table class="lesson-index-table">
        <thead><tr><th>Buổi</th><th>Bài học</th><th>Giai đoạn</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </section>
  </div>
</body>
</html>
"""


def main() -> None:
    text = "\n\n".join(path.read_text(encoding="utf-8") for path in source_files())
    lessons = extract_lessons(clean_text(text))
    missing = [index for index in range(1, LESSON_COUNT + 1) if index not in lessons]
    if missing:
        raise SystemExit(f"Missing lesson content for: {missing}")

    OUT_DIR.mkdir(exist_ok=True)
    for old_html in OUT_DIR.glob("*.html"):
        old_html.unlink()

    titles = {index: lessons[index]["title"] for index in range(1, LESSON_COUNT + 1)}
    for index in range(1, LESSON_COUNT + 1):
        body_html = render_body(lessons[index]["body"])
        filename = lesson_filename(index, titles[index])
        (OUT_DIR / filename).write_text(render_lesson(index, titles[index], body_html, titles), encoding="utf-8")

    (OUT_DIR / "index.html").write_text(render_index(titles), encoding="utf-8")
    print(f"Imported {LESSON_COUNT} Python lessons into {OUT_DIR}")


if __name__ == "__main__":
    sys.exit(main())
