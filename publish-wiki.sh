#!/usr/bin/env bash
# 一键把本目录下的 GitHub Wiki 页面发布到 <repo>.wiki.git
# 前置条件：该仓库的 Wikis 功能已开启（公开仓库免费可用；私有仓库需 Pro/Team/Enterprise 或转公开）
set -euo pipefail

WIKI_URL="https://github.com/Kytolly/wiki-tutorial-Isaac.wiki.git"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_DIR="$(mktemp -d)"

echo "==> 准备临时 wiki 仓库: $TMP_DIR"
git init -b master "$TMP_DIR" >/dev/null
cd "$TMP_DIR"

cp "$SRC_DIR"/Home.md .
cp "$SRC_DIR"/_Sidebar.md .
cp "$SRC_DIR"/_META.md .
cp "$SRC_DIR"/_Footer.md .
cp "$SRC_DIR"/L0-*.md .
cp "$SRC_DIR"/L1-*.md .

git add -A
git -c user.name="${GIT_AUTHOR_NAME:-kytolly}" \
    -c user.email="${GIT_AUTHOR_EMAIL:-1392875097@qq.com}" \
    commit -m "publish Isaac Lab & Isaac Sim tutorial wiki" >/dev/null

git remote add origin "$WIKI_URL"
echo "==> 推送到 $WIKI_URL"
git push -u origin master

echo "==> 完成。访问: https://github.com/Kytolly/wiki-tutorial-Isaac/wiki"
