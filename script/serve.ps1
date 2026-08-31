# 本地 wiki 网页预览（版本化，放在 script/）：生成 docs 并用 mkdocs-material 启动。
# 产物（.venv/docs/site）都在 build/preview/，该目录已被 .gitignore 忽略。
$ROOT = Split-Path -Parent $PSScriptRoot   # doc/wiki
$env:NO_MKDOCS_2_WARNING=1

uv run python "$ROOT/script/build.py"
& "$ROOT/.venv/Scripts/mkdocs.exe" serve -f "$ROOT/script/mkdocs.yml" -a 127.0.0.1:8000
