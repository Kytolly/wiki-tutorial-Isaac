# 配图资产目录（page/assets/images/）

本目录存放教程页面用到的本地图片（优先官方教程图/截图）。

## 使用方法

1. 把图片放到本目录，例如 official-isaaclab-arch.png。
2. 在页面 Markdown 里用相对路径引用（相对 page/ 根）：
   ![说明文字](assets/images/official-isaaclab-arch.png)
3. 每张图必须带 caption + 来源 + 访问日期，例如：
   > 图 1 Isaac Lab 架构总览（来源：https://isaac-sim.github.io/IsaacLab/ 官方文档，访问于 2026-09-01）

## 构建/发布说明

- 本地预览：script/build.py 会把 page/assets/** 复制到 build/preview/docs/assets/**，mkdocs 可直接渲染。
- GitHub Wiki：script/publish-wiki.sh 会把 page/assets/**（保持子目录）一并推送到 wiki 仓库，相对路径可正常显示。
- 找不到可靠官方图时按规范降级为 Mermaid（本地预览渲染；GitHub Wiki 显示为代码块）。
