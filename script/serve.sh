#!/usr/bin/env bash
# 本地 wiki 网页预览（版本化，放在 script/）：生成 docs 并用 mkdocs-material 启动。
# 产物（.venv/docs/site）都在 build/preview/，该目录已被 .gitignore 忽略。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"   # doc/wiki

python3 "$ROOT/script/build.py"
exec "$ROOT/build/preview/.venv/bin/mkdocs" serve -f "$ROOT/script/mkdocs.yml" -a 127.0.0.1:8000
