/* MCP 由浅入深教程 —— 交互脚本
   本文件仅做渐进增强：即使脚本不执行，正文、导航与代码同样完整可读。 */

(function () {
  "use strict";

  // ---------- 主题切换 ----------
  var root = document.documentElement;
  var toggle = document.querySelector(".theme-toggle");

  function applyTheme(theme) {
    if (theme === "dark" || theme === "light") {
      root.setAttribute("data-theme", theme);
    } else {
      root.removeAttribute("data-theme");
    }
    if (toggle) {
      toggle.textContent =
        theme === "dark" ? "切换到浅色" : "切换到深色";
    }
  }

  var saved = null;
  try {
    saved = localStorage.getItem("mcp-tutorial-theme");
  } catch (e) {
    saved = null;
  }
  applyTheme(saved);

  if (toggle) {
    toggle.addEventListener("click", function () {
      var isDark =
        root.getAttribute("data-theme") === "dark" ||
        (root.getAttribute("data-theme") === null &&
          window.matchMedia("(prefers-color-scheme: dark)").matches);
      var next = isDark ? "light" : "dark";
      applyTheme(next);
      try {
        localStorage.setItem("mcp-tutorial-theme", next);
      } catch (e) {
        /* 隐私模式下写入失败时忽略 */
      }
    });
  }

  // ---------- 阅读进度 ----------
  var progress = document.getElementById("read-progress");

  function updateProgress() {
    if (!progress) return;
    var doc = document.documentElement;
    var total = doc.scrollHeight - doc.clientHeight;
    var ratio = total > 0 ? doc.scrollTop / total : 0;
    progress.value = Math.min(1, Math.max(0, ratio));
  }

  window.addEventListener("scroll", updateProgress, { passive: true });
  window.addEventListener("resize", updateProgress);
  updateProgress();

  // ---------- 目录高亮 ----------
  var links = Array.prototype.slice.call(
    document.querySelectorAll("nav.toc a[href^='#']")
  );
  var sections = links
    .map(function (a) {
      return document.getElementById(a.getAttribute("href").slice(1));
    })
    .filter(Boolean);

  if ("IntersectionObserver" in window && sections.length) {
    var visible = new Set();
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            visible.add(entry.target.id);
          } else {
            visible.delete(entry.target.id);
          }
        });
        var current = sections
          .map(function (s) {
            return s.id;
          })
          .filter(function (id) {
            return visible.has(id);
          })[0];
        links.forEach(function (a) {
          a.classList.toggle(
            "active",
            a.getAttribute("href") === "#" + current
          );
        });
      },
      { rootMargin: "-80px 0px -70% 0px" }
    );
    sections.forEach(function (s) {
      observer.observe(s);
    });
  }

  // ---------- 代码复制 ----------
  document.querySelectorAll(".codeblock").forEach(function (block) {
    var pre = block.querySelector("pre");
    if (!pre) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "复制";
    btn.addEventListener("click", function () {
      var text = pre.innerText;
      function done(ok) {
        btn.textContent = ok ? "已复制" : "复制失败";
        window.setTimeout(function () {
          btn.textContent = "复制";
        }, 1600);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(
          function () {
            done(true);
          },
          function () {
            done(false);
          }
        );
      } else {
        done(false);
      }
    });
    block.appendChild(btn);
  });

  // ---------- 窄屏目录收起 ----------
  var tocDetails = document.querySelector("nav.toc details");
  if (tocDetails) {
    // 页面载入时窄屏默认收起目录，宽屏保持展开。
    if (window.innerWidth <= 900) {
      tocDetails.removeAttribute("open");
    }
    tocDetails.addEventListener("click", function (event) {
      var target = event.target;
      if (target && target.tagName === "A" && window.innerWidth <= 900) {
        tocDetails.removeAttribute("open");
      }
    });
  }
})();
