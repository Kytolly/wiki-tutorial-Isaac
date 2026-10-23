#!/usr/bin/env python3
# 本地预览构建脚本（版本化，放在 script/）：把 page/** 拍平并转换链接，
# 生成 mkdocs 可渲染的 build/preview/docs/。
import os
import shutil

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

:root {
  --md-code-wrap-icon: url('data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M3 6h18v2H3zm0 5h12.5a2.5 2.5 0 0 1 0 5H13v-2h2.5a.5.5 0 0 0 0-1H3zm0 5h6v2H3z"/></svg>');
}

.md-typeset .md-code__button[data-md-type=wrap]:after {
  -webkit-mask-image: var(--md-code-wrap-icon);
  mask-image: var(--md-code-wrap-icon);
}

.md-typeset .md-code__button[hidden] {
  display: none !important;
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

shutil.rmtree(DOCS, ignore_errors=True)   # 清掉旧产物，避免残留过期页面
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

# 复制本地图片资产（page/assets/** → docs/assets/**），供 Markdown 相对路径引用
asset_src = os.path.join(SRC, "assets")
if os.path.isdir(asset_src):
    shutil.copytree(asset_src, os.path.join(DOCS, "assets"), dirs_exist_ok=True)
    print("built assets/")

css_dir = os.path.join(DOCS, "stylesheets")
os.makedirs(css_dir, exist_ok=True)
open(os.path.join(css_dir, "extra.css"), "w", encoding="utf-8").write(EXTRA_CSS)
print("built stylesheets/extra.css")

# 复制自定义 JS（script/assets/** → docs/javascripts/**），供 extra_javascript 引用
js_src = os.path.join(HERE, "assets")
if os.path.isdir(js_src):
    shutil.copytree(js_src, os.path.join(DOCS, "javascripts"), dirs_exist_ok=True)
    print("built javascripts/")
