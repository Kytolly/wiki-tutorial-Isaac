# wiki-tutorial-Isaac

A wiki repository about tutorials of IsaacLab and IsaacSim.

## 目录结构

- `page/` — Wiki 页面（Markdown），按层级分类到 `L0/`、`L1/` 子目录；根下保留 `Home.md`、`_Sidebar.md`、`_META.md`、`_Footer.md` 以兼容 GitHub Wiki。
- `plugin/` — 插件（规划中）。
- `script/` — 脚本（`publish-wiki.sh` 一键把 `page/**` 拍平发布到 GitHub Wiki）。
- `test/` — 测试（规划中）。

## 发布到 GitHub Wiki

```bash
./script/publish-wiki.sh
```

## 本地预览

本地网页预览见 `../wiki-preview`（mkdocs-material），执行 `../wiki-preview/serve.sh`。
