/* ==========================================================================
   AgentScope Java 2.0 入门教程 — 站点脚本
   零依赖：语法高亮 / 复制 / 导航高亮 / 移动端菜单
   ========================================================================== */
(function () {
  'use strict';

  /* ---------------------------- 语法高亮 ---------------------------- */

  var JAVA_KW = ('abstract assert boolean break byte case catch char class const continue default do ' +
    'double else enum extends final finally float for goto if implements import instanceof int ' +
    'interface long native new package private protected public return short static strictfp ' +
    'super switch synchronized this throw throws transient try var void volatile while yield ' +
    'record sealed permits non-sealed true false null').split(' ');

  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /* 把整段代码切成占位符数组 + 文本数组，避免后续正则互相污染 */
  function tokenize(code, lang) {
    var out = [], buf = '', i = 0;
    function flush() { if (buf) { out.push({ t: 'txt', v: buf }); buf = ''; } }

    while (i < code.length) {
      var c = code[i], n = code[i + 1];

      /* 注释 */
      if (c === '/' && n === '/') {
        flush();
        var e = code.indexOf('\n', i); if (e < 0) e = code.length;
        out.push({ t: 'com', v: code.slice(i, e) }); i = e; continue;
      }
      if (c === '/' && n === '*') {
        flush();
        var e2 = code.indexOf('*/', i + 2); e2 = e2 < 0 ? code.length : e2 + 2;
        out.push({ t: 'com', v: code.slice(i, e2) }); i = e2; continue;
      }
      if (lang !== 'xml' && lang !== 'html' && c === '#') {
        flush();
        var e3 = code.indexOf('\n', i); if (e3 < 0) e3 = code.length;
        out.push({ t: 'com', v: code.slice(i, e3) }); i = e3; continue;
      }

      /* 字符串 */
      if (c === '"' || c === "'") {
        flush();
        var q = c, j = i + 1;
        while (j < code.length) {
          if (code[j] === '\\') { j += 2; continue; }
          if (code[j] === q) { j++; break; }
          if (code[j] === '\n') break;
          j++;
        }
        out.push({ t: 'str', v: code.slice(i, j) }); i = j; continue;
      }

      /* 注解 @Xxx */
      if (c === '@' && /[A-Za-z_]/.test(code[i + 1] || '')) {
        flush();
        var k = i + 1;
        while (k < code.length && /[A-Za-z0-9_.]/.test(code[k])) k++;
        out.push({ t: 'anno', v: code.slice(i, k) }); i = k; continue;
      }

      /* 数字 */
      if (/[0-9]/.test(c) && !/[A-Za-z0-9_$]/.test(code[i - 1] || '')) {
        flush();
        var m = i;
        while (m < code.length && /[0-9a-fA-FxX._Ll]/.test(code[m])) m++;
        out.push({ t: 'num', v: code.slice(i, m) }); i = m; continue;
      }

      /* 标识符 */
      if (/[A-Za-z_$]/.test(c)) {
        flush();
        var s = i;
        while (i < code.length && /[A-Za-z0-9_$]/.test(code[i])) i++;
        var w = code.slice(s, i);
        var lower = w.toLowerCase();
        var cls = 'txt';
        if (JAVA_KW.indexOf(w) >= 0) cls = 'kw';
        else if (i < code.length && code[i] === '(') cls = 'meth';
        else if (/^[A-Z]/.test(w)) cls = 'type';
        else if (lower === 'true' || lower === 'false' || lower === 'null') cls = 'kw';
        out.push({ t: cls, v: w });
        continue;
      }

      buf += c; i++;
    }
    flush();
    return out;
  }

  function render(tok, lang) {
    /* shell / yaml / properties 只做轻量着色 */
    if (lang === 'bash' || lang === 'shell') {
      return esc(tok)
        .replace(/(^|\n)([ \t]*)(#.*)/g, '$1$2<span class="tok-com">$3</span>')
        .replace(/(&quot;|")([^"&]*)(&quot;|")/g, '<span class="tok-str">"$2"</span>');
    }
    return tok.map(function (t) {
      if (t.t === 'txt') return esc(t.v);
      return '<span class="tok-' + t.t + '">' + esc(t.v) + '</span>';
    }).join('');
  }

  function highlight() {
    document.querySelectorAll('pre > code').forEach(function (code) {
      if (code.dataset.done) return;
      code.dataset.done = '1';
      var pre = code.parentNode;
      var wrap = pre.closest('.code-wrap');
      var lang = 'java';
      if (wrap) {
        var l = wrap.querySelector('.code-lang');
        if (l) lang = (l.textContent || 'java').trim().toLowerCase();
      }
      var raw = code.textContent.replace(/\n$/, '');

      if (lang === 'bash' || lang === 'shell' || lang === 'yaml' || lang === 'text' || lang === 'diff') {
        code.innerHTML = render(raw, lang);
        return;
      }

      var html = tokenize(raw, lang).map(function (t) { return render(t.v, lang); }).join('');
      code.innerHTML = html;

      /* 行号 */
      var lines = code.innerHTML.split('\n');
      if (lines.length > 3) {
        pre.classList.add('has-num');
        code.innerHTML = lines.map(function (l) {
          return '<span class="ln">' + l + '</span>';
        }).join('\n');
      }
    });
  }

  /* ---------------------------- 复制按钮 ---------------------------- */

  function copyAll() {
    document.querySelectorAll('.copy-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var wrap = btn.closest('.code-wrap');
        var code = wrap && wrap.querySelector('code');
        if (!code) return;
        var text = code.innerText.replace(/^\s*\d+\n/gm, '');
        var done = function () {
          var old = btn.textContent;
          btn.textContent = '已复制';
          setTimeout(function () { btn.textContent = old; }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done).catch(fallback);
        } else { fallback(); }

        function fallback() {
          var ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand('copy'); done(); } catch (e) { /* 忽略 */ }
          document.body.removeChild(ta);
        }
      });
    });
  }

  /* ---------------------------- 导航高亮 ---------------------------- */

  function navHighlight() {
    var links = Array.prototype.slice.call(document.querySelectorAll('.nav a.nav-link'));
    if (!links.length) return;
    var byHref = {};
    links.forEach(function (a) { byHref[a.getAttribute('href')] = a; });

    function setActive(href) {
      links.forEach(function (a) { a.classList.remove('active'); });
      var a = byHref[href];
      if (a) a.classList.add('active');
    }

    /* 当前页高亮 */
    var here = location.pathname.split('/').pop() || 'index.html';
    setActive(here);

    /* 滚动时高亮当前章节 */
    var heads = Array.prototype.slice.call(document.querySelectorAll('h2[id], h3[id]'));
    if (!heads.length || !('IntersectionObserver' in window)) return;

    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        visible[en.target.id] = en.isIntersecting;
      });
      for (var i = 0; i < heads.length; i++) {
        if (visible[heads[i].id]) {
          var a = byHref[here + '#' + heads[i].id];
          if (a) { setActive(here + '#' + heads[i].id); }
          return;
        }
      }
    }, { rootMargin: '-10% 0px -75% 0px', threshold: 0 });
    heads.forEach(function (h) { io.observe(h); });
  }

  /* ---------------------------- 移动端菜单 ---------------------------- */

  function mobileNav() {
    var btn = document.querySelector('.topbar button');
    if (!btn) return;
    btn.addEventListener('click', function () {
      document.body.classList.toggle('nav-open');
    });
    document.addEventListener('click', function (e) {
      if (!document.body.classList.contains('nav-open')) return;
      if (e.target.closest('.nav') || e.target.closest('.topbar')) return;
      document.body.classList.remove('nav-open');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') document.body.classList.remove('nav-open');
    });
  }

  /* ---------------------------- 启动 ---------------------------- */

  function boot() {
    highlight();
    copyAll();
    navHighlight();
    mobileNav();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();