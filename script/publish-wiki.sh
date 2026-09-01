#!/usr/bin/env bash
# 一键把 page/ 下的 GitHub Wiki 页面拍平并发布到 <repo>.wiki.git
# 前置：仓库 Wikis 功能已开启（公开免费；私有需 Pro/Team/Enterprise 或转公开）
set -euo pipefail

WIKI_URL="https://github.com/Kytolly/wiki-tutorial-Isaac.wiki.git"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PAGE_DIR="$REPO_DIR/page"
TMP_DIR="$(mktemp -d)"

echo "==> 页面目录: $PAGE_DIR"
echo "==> 临时仓库: $TMP_DIR"
git init -b master "$TMP_DIR" >/dev/null

# 拍平：把 page/**/*.md 复制到临时仓库根目录（用 basename，GitHub Wiki 要求扁平结构）
while IFS= read -r f; do
  cp "$f" "$TMP_DIR/$(basename "$f")"
done < <(find "$PAGE_DIR" -type f -name '*.md' | sort)

# 复制本地图片资产（保持子目录，供相对路径引用）
if [ -d "$PAGE_DIR/assets" ]; then
  cp -r "$PAGE_DIR/assets" "$TMP_DIR/"
fi

cd "$TMP_DIR"
git add -A
git -c user.name="${GIT_AUTHOR_NAME:-kytolly}" \
    -c user.email="${GIT_AUTHOR_EMAIL:-1392875097@qq.com}" \
    commit -m "publish Isaac Lab & Isaac Sim tutorial wiki" >/dev/null

git remote add origin "$WIKI_URL"
echo "==> 推送到 $WIKI_URL"
git push -u origin master
echo "==> 完成。访问: https://github.com/Kytolly/wiki-tutorial-Isaac/wiki"
