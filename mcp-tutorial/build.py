#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""章节页面生成器：统一页头/页尾，正文从 chapters_src/*.html 片段读取。"""
import os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CH_DIR = ROOT / "chapters"
SRC_DIR = ROOT / "chapters_src"
CH_DIR.mkdir(exist_ok=True)

CHAPTERS = [
    ("01-what-is-mcp",   "1",  "MCP 是什么"),
    ("02-architecture",  "2",  "架构与核心概念"),
    ("03-first-server",  "3",  "第一个 MCP Server"),
    ("04-tools",         "4",  "Tools（工具）"),
    ("05-resources",     "5",  "Resources（资源）"),
    ("06-prompts",       "6",  "Prompts（提示模板）"),
    ("07-transport",     "7",  "传输层"),
    ("08-lifecycle",     "8",  "JSON-RPC 与连接生命周期"),
    ("09-advanced",      "9",  "进阶特性"),
    ("10-client",        "10", "自己写一个 MCP Client"),
    ("11-security",      "11", "安全加固"),
    ("12-practice",      "12", "实战案例"),
]
SLUG2IDX = {c[0]: i for i, c in enumerate(CHAPTERS)}


def nav(cur_slug):
    items = ['<a href="../index.html">目录</a>']
    for slug, num, _ in CHAPTERS:
        cls = ' class="current"' if slug == cur_slug else ""
        items.append(f'<a href="{slug}.html"{cls}>{num}</a>')
    return "\n      ".join(items)


def prevnext(idx):
    parts = ['<div class="prevnext">']
    if idx > 0:
        s, n, t = CHAPTERS[idx - 1]
        parts.append(f'  <a href="{s}.html">← 第 {n} 章</a>')
    else:
        parts.append('  <span class="spacer"></span>')
    if idx < len(CHAPTERS) - 1:
        s, n, t = CHAPTERS[idx + 1]
        parts.append(f'  <a href="{s}.html">第 {n} 章：{t} →</a>')
    parts.append("</div>")
    return "\n".join(parts)


def build(slug):
    idx = SLUG2IDX[slug]
    _, num, title = CHAPTERS[idx]
    body = (SRC_DIR / f"{slug}.html").read_text(encoding="utf-8")
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第 {num} 章：{title} · MCP 教程</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="../index.html">MCP<span> 教程</span></a>
    <nav class="site-nav">
      {nav(slug)}
    </nav>
  </div>
</header>

<main>
<div class="wrap">

{body}

{prevnext(idx)}

</div>
</main>

<footer class="site-footer">
  <div class="wrap"><a href="../index.html">← 返回目录</a></div>
</footer>
<script src="../assets/app.js"></script>
</body>
</html>
"""
    (CH_DIR / f"{slug}.html").write_text(html, encoding="utf-8")
    return len(html)


if __name__ == "__main__":
    import sys
    targets = sys.argv[1:] or [c[0] for c in CHAPTERS if (SRC_DIR / f"{c[0]}.html").exists()]
    for slug in targets:
        src = SRC_DIR / f"{slug}.html"
        if not src.exists():
            print(f"SKIP {slug} (无片段)")
            continue
        n = build(slug)
        print(f"OK   {slug}.html  ({n} bytes)")
