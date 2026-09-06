# wiki-tutorial-Isaac

A wiki repository about tutorials of IsaacLab and IsaacSim.

## 目录结构

- `page/` — Wiki 页面（Markdown），按学习分级和 StackForce 工程结构分类；根下保留 `Home.md`、`_Sidebar.md`、`_META.md`、`_Footer.md` 以兼容 GitHub Wiki。StackForce 页面位于 `page/stackforce/`：`milestone/` 是仪表盘，`gate/` 是原子验收任务，`topic/` 是技术主题，`evidence/` 是当前证据，`archive/` 是历史材料。
- `plugin/` — 插件（规划中）。
- `script/` — 脚本（`publish-wiki.sh` 一键把 `page/**` 拍平发布到 GitHub Wiki）。
- `test/` — 测试（规划中）。

## 发布到 GitHub Wiki

```bash
./script/publish-wiki.sh
```

## 本地预览

本地网页预览使用 mkdocs-material：

- 脚本（版本化）：`script/serve.sh`、`script/build.py`、`script/mkdocs.yml`
- 构建产物（已 gitignore）：`build/preview/`（`.venv`、`docs`、`site`、日志）

```bash
./script/serve.sh
```

浏览器打开 `http://127.0.0.1:8001/`。
