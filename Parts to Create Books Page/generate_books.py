import re
from html import escape

INPUT_FILE = "books.txt"
OUTPUT_FILE = "books.html"

HTML_START = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catholic Library</title>

<style>
* {
  box-sizing: border-box; /* ✅ CRITICAL FIX */
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
  background: #ffe888;
  margin: 0;
  padding: 20px;
  color: #1c1c1e;
}

.container {
  max-width: 900px;
  margin: auto;
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 20px rgba(0,0,0,.08);
}

/* ✅ SEARCH BAR */
.search-wrapper {
  position: relative;
  margin-bottom: 16px;
}

.search-wrapper input {
  width: 100%;
  padding: 12px 42px 12px 14px;
  font-size: 15px;
  border-radius: 10px;
  border: 1px solid #ccc;
  outline: none;
}

.search-wrapper button {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: none;
  font-size: 20px;
  cursor: pointer;
  display: none;
  line-height: 1;
}

/* ✅ BOOK LIST */
.library {
  display: flex;
  flex-direction: column;
}

.book {
  display: block;
  background: #f2f2f7;
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 10px;
  text-decoration: none;
  color: #000;
}

.book:hover {
  background: #e6e6eb;
}

.title {
  font-size: 15px;
  font-weight: 600;
}

/* ✅ HIGHLIGHT */
mark {
  background: #ffeb3b;
  padding: 0;
}
</style>
</head>

<body>
<div class="container">
  <h1>Catholic Library</h1>

  <div class="search-wrapper">
    <input
      type="text"
      id="searchInput"
      placeholder="Search books..."
      oninput="filterBooks()"
    />
    <button id="clearBtn" onclick="clearSearch()">×</button>
  </div>

  <div class="library">
"""

HTML_END = """
  </div>
</div>

<script>
function filterBooks() {
  const input = document.getElementById("searchInput");
  const filter = input.value.toLowerCase();
  const books = document.getElementsByClassName("book");
  const clearBtn = document.getElementById("clearBtn");

  clearBtn.style.display = filter ? "block" : "none";

  for (let book of books) {
    const titleEl = book.querySelector(".title");
    const text = titleEl.textContent;
    titleEl.innerHTML = text;

    if (text.toLowerCase().includes(filter)) {
      book.style.display = "";
      if (filter) {
        const regex = new RegExp("(" + escapeRegExp(filter) + ")", "ig");
        titleEl.innerHTML = text.replace(regex, "<mark>$1</mark>");
      }
    } else {
      book.style.display = "none";
    }
  }
}

function clearSearch() {
  document.getElementById("searchInput").value = "";
  document.getElementById("clearBtn").style.display = "none";
  filterBooks();
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&");
}
</script>

</body>
</html>
"""

# ---------- PARSING ----------
url_re = re.compile(r"https?://[^\s\)\]]+")
html_tag_re = re.compile(r"<[^>]+>")

seen_urls = set()
books = []
current_title = "Unknown title"

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for raw_line in f:
        line = raw_line.strip()
        if not line:
            continue

        clean = html_tag_re.sub("", line)

        if not clean.startswith("http"):
            clean = url_re.sub("", clean).strip(" –:-")
            if clean:
                current_title = clean

        for url in url_re.findall(line):
            if url in seen_urls:
                continue
            seen_urls.add(url)
            books.append((escape(current_title), url))

# ---------- WRITE OUTPUT ----------
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write(HTML_START)
    for title, url in books:
        out.write(
            f'<a class="book" href="{url}" target="_blank">\n'
            f'  <div class="title">{title}</div>\n'
            f'</a>\n'
        )
    out.write(HTML_END)

print(f"✅ Generated {len(books)} unique books into {OUTPUT_FILE}")
