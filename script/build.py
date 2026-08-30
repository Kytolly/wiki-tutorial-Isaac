#!/usr/bin/env python3
# 本地预览构建脚本（版本化，放在 script/）：把 page/** 拍平并转换链接，
# 生成 mkdocs 可渲染的 build/preview/docs/。
import os

HERE = os.path.dirname(os.path.abspath(__file__))   # .../doc/wiki/script
ROOT = os.path.dirname(HERE)                        # .../doc/wiki
SRC = os.path.join(ROOT, "page")                    # 源页面（唯一真相）
DOCS = os.path.join(ROOT, "build", "preview", "docs")  # 生成的拍平 md（gitignore）
SKIP = {"_Sidebar.md", "_Footer.md"}

EXTRA_CSS = """.md-typeset .grid.cards > ul > li {
  border-radius: 0.5rem;
}

.md-typeset .wiki-meta {
  color: var(--md-default-fg-color--light);
  font-size: 0.82rem;
}
"""

def target_name(name):
    return "index.md" if name == "Home" else name + ".md"

def convert(text):
    out = []
    i, n = 0, len(text)
    while i < n:
        if text.startswith("[[", i):
            j = text.find("]]", i)
            if j != -1:
                name = text[i + 2:j].strip()
                out.append(f"[{name}]({target_name(name)})")
                i = j + 2
                continue
        out.append(text[i])
        i += 1
    return "".join(out)

os.makedirs(DOCS, exist_ok=True)
for root, _, files in os.walk(SRC):
    for f in files:
        if not f.endswith(".md") or f in SKIP:
            continue
        src = os.path.join(root, f)
        text = convert(open(src, encoding="utf-8").read())
        dst_name = "index.md" if f == "Home.md" else f
        open(os.path.join(DOCS, dst_name), "w", encoding="utf-8").write(text)
        print("built", dst_name)

css_dir = os.path.join(DOCS, "stylesheets")
os.makedirs(css_dir, exist_ok=True)
open(os.path.join(css_dir, "extra.css"), "w", encoding="utf-8").write(EXTRA_CSS)
print("built stylesheets/extra.css")
