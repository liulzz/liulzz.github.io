// 代码块复制按钮：仅在支持剪贴板接口的环境中显示。
document.addEventListener("DOMContentLoaded", function () {
  if (!navigator.clipboard) return;
  document.querySelectorAll("pre").forEach(function (pre) {
    var btn = document.createElement("button");
    btn.className = "copybtn";
    btn.type = "button";
    btn.textContent = "复制";
    btn.addEventListener("click", function () {
      var code = pre.querySelector("code");
      var text = code ? code.innerText : pre.innerText;
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = "已复制";
        setTimeout(function () { btn.textContent = "复制"; }, 1200);
      });
    });
    pre.appendChild(btn);
  });
});
