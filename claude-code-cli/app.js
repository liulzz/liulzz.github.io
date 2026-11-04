(function () {
  var toggle = document.getElementById("nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("click", function (e) {
      if (e.target.closest(".sidebar a")) {
        document.body.classList.remove("nav-open");
      }
    });
  }

  var page = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".sidebar a").forEach(function (link) {
    var href = link.getAttribute("href");
    if (href === page) link.classList.add("active");
  });

  document.querySelectorAll(".cmd").forEach(function (block) {
    var btn = block.querySelector("button");
    var code = block.querySelector("pre code");
    if (!btn || !code) return;
    btn.addEventListener("click", function () {
      var text = code.innerText;
      function ok() {
        btn.textContent = "已复制";
        setTimeout(function () {
          btn.textContent = "复制";
        }, 1400);
      }
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(ok).catch(fallback);
      } else {
        fallback();
      }
      function fallback() {
        var area = document.createElement("textarea");
        area.value = text;
        area.style.position = "fixed";
        area.style.opacity = "0";
        document.body.appendChild(area);
        area.select();
        try {
          document.execCommand("copy");
          ok();
        } catch (err) {
          btn.textContent = "复制失败";
        }
        document.body.removeChild(area);
      }
    });
  });
})();
