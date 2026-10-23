/* 逐块代码自动换行：移植 Docusaurus WordWrapButton 到 mkdocs-material
 * - 每块独立状态，互不影响
 * - 仅在内容溢出（或已开启）时显示按钮
 * - 开启：给 <code> 打内联 white-space:pre-wrap + overflow-wrap:anywhere
 * - 关闭：移除内联样式，回落到 CSS
 */
(function () {
  "use strict";

  var CODE = "pre:not(.mermaid) > code";
  var blocks = [];
  var raf = 0;
  var bound = false;
  var ro = null;

  function makeButton() {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "md-code__button";
    btn.setAttribute("data-md-type", "wrap");
    btn.title = "Toggle word wrap";
    btn.setAttribute("aria-label", "Toggle word wrap");
    btn.hidden = true;
    return btn;
  }

  function ensureObservers() {
    if (!bound) {
      window.addEventListener("resize", scheduleSync, { passive: true });
      document.addEventListener("toggle", scheduleSync, true); // <details> 展开
      bound = true;
    }
    if (!ro && window.ResizeObserver) ro = new ResizeObserver(scheduleSync);
  }

  function mount(code) {
    var pre = code.parentElement;
    if (!pre) return;
    var nav = pre.querySelector(":scope > .md-code__nav");
    if (!nav) {                       // 兜底：content.code.copy 被关掉时自建
      nav = document.createElement("nav");
      nav.className = "md-code__nav";
      pre.insertBefore(nav, code);
    }
    if (nav.querySelector(':scope > [data-md-type="wrap"]')) return;  // 幂等：避免重复挂载

    var entry = { code: code, btn: makeButton(), on: false };

    entry.btn.addEventListener("click", function () {
      entry.on = !entry.on;
      if (entry.on) {
        code.style.whiteSpace = "pre-wrap";
        code.style.overflowWrap = "anywhere";
      } else {
        code.style.removeProperty("white-space");
        code.style.removeProperty("overflow-wrap");
      }
      entry.btn.classList.toggle("md-code__button--active", entry.on);
      sync();
    });

    nav.insertBefore(entry.btn, nav.firstChild);  // 排在「复制」左侧
    blocks.push(entry);
    if (ro) ro.observe(code);
  }

  function sync() {
    for (var i = 0; i < blocks.length; i++) {
      var e = blocks[i];
      // clientWidth 为 0 = 未布局（折叠的 details / 隐藏 tab），保持现状
      if (!e.code.clientWidth && !e.on) continue;
      var scrollable = e.code.scrollWidth > e.code.clientWidth;
      e.btn.hidden = !(e.on || scrollable);
    }
  }

  function scheduleSync() {
    if (raf) return;
    raf = requestAnimationFrame(function () {
      raf = 0;
      sync();
    });
  }

  function boot(root) {
    blocks.length = 0;
    ensureObservers();
    var nodes = (root || document).querySelectorAll(CODE);
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
    sync();
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(boot);   // 兼容将来开启 navigation.instant
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      boot(document);
    });
  } else {
    boot(document);
  }
})();
