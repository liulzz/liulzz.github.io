#!/usr/bin/env python3
"""AgentScope Java 2.0 教程站点构建脚本。

用法：python3 build.py
读取 _src/chapters/*.html 片段，套用模板生成站点根目录下的 HTML 页面。
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "_src"
CH = SRC / "chapters"

# 章节清单：(文件名, 章节编号显示, 标题, 侧栏短标题, 分组)
CHAPTERS = [
    ("01-overview",      "第 1 章",  "认识 AgentScope 2.0",              "认识 AgentScope 2.0",    "第一部分 · 理论筑基"),
    ("02-quickstart",    "第 2 章",  "环境搭建与第一个智能体",           "环境搭建与第一个智能体", "第一部分 · 理论筑基"),
    ("03-message-model", "第 3 章",  "消息、多模态与模型接入",           "消息与模型接入",         "第一部分 · 理论筑基"),
    ("04-agent",         "第 4 章",  "ReActAgent 深入",                  "ReActAgent 深入",        "第二部分 · 核心构件"),
    ("05-tool",          "第 5 章",  "工具：让智能体行动",               "工具",                   "第二部分 · 核心构件"),
    ("06-permission",    "第 6 章",  "权限系统与人机协同（HITL）",       "权限系统与 HITL",        "第二部分 · 核心构件"),
    ("07-middleware",    "第 7 章",  "中间件：六阶段生命周期",           "中间件",                 "第二部分 · 核心构件"),
    ("08-harness",       "第 8 章",  "HarnessAgent 与工作区",            "Harness 与工作区",       "第三部分 · Harness 能力"),
    ("09-memory",        "第 9 章",  "记忆与上下文压缩",                 "记忆与上下文压缩",       "第三部分 · Harness 能力"),
    ("10-subagent-plan", "第 10 章", "子智能体与计划模式",               "子智能体与计划模式",     "第三部分 · Harness 能力"),
    ("11-skill",         "第 11 章", "技能系统",                         "技能系统",               "第三部分 · Harness 能力"),
    ("12-sandbox",       "第 12 章", "文件系统与沙箱",                   "文件系统与沙箱",         "第三部分 · Harness 能力"),
    ("13-channel",       "第 13 章", "Channel 与 Gateway：对外服务",     "Channel 与 Gateway",     "第四部分 · 工程化"),
    ("14-production",    "第 14 章", "上生产：分布式与多租户",           "上生产",                 "第四部分 · 工程化"),
    ("15-project",       "结业",     "综合实战：智能客服工单系统",       "综合实战项目",           "第四部分 · 工程化"),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · AgentScope Java 2.0 新手入门教程</title>
<meta name="description" content="场景驱动的 AgentScope Java 2.0 中文新手教程：由浅入深，先理论后实践，Java 代码示例。">
<link rel="stylesheet" href="{base}style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/java.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/xml.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/markdown.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/yaml.min.js"></script>
</head>
<body>
<header class="site-header">
  <button id="nav-toggle" aria-label="打开目录">☰</button>
  <a class="logo" href="{base}index.html"><span class="dot"></span>AgentScope Java 2.0 入门教程</a>
  <span class="tagline">{tagline}</span>
  <span class="spacer"></span>
  <a class="gh-link" href="https://github.com/agentscope-ai/agentscope-java" target="_blank" rel="noopener">GitHub ↗</a>
</header>
<div class="layout">
<nav class="sidebar" id="sidebar">
  <div class="group">
    <div class="group-title">开始</div>
    <a class="item{active_home}" href="{base}index.html"><span class="no">序</span>教程导读与特性全景</a>
  </div>
{nav}
</nav>
<main class="content">
{body}
<nav class="pager">
{pager}
</nav>
</main>
</div>
<footer class="site-footer">
  AgentScope Java 2.0 新手入门教程 · 基于 AgentScope Java v2.0.3 官方文档编写 · {year}
  <br>官网 <a href="https://java.agentscope.io" target="_blank" rel="noopener">java.agentscope.io</a>
  ｜仓库 <a href="https://github.com/agentscope-ai/agentscope-java" target="_blank" rel="noopener">agentscope-ai/agentscope-java</a>
</footer>
<script>
document.getElementById('nav-toggle').addEventListener('click', function () {{
  document.getElementById('sidebar').classList.toggle('open');
}});
window.addEventListener('DOMContentLoaded', function () {{
  document.querySelectorAll('pre code').forEach(function (el) {{
    try {{ hljs.highlightElement(el); }} catch (e) {{}}
  }});
}});
</script>
</body>
</html>
"""


def build():
    pages = []  # (fname, title, prev, next)
    for i, (fname, _no, title, _short, _group) in enumerate(CHAPTERS):
        prev = pages[-1] if pages else None
        nxt = (CHAPTERS[i + 1][0], CHAPTERS[i + 1][2]) if i + 1 < len(CHAPTERS) else None
        pages.append((fname, title, prev, nxt))

    # ---- 生成侧栏（按分组）----
    nav_parts = []
    seen_groups = []
    for fname, no, title, short, group in CHAPTERS:
        if group not in seen_groups:
            if seen_groups:
                nav_parts.append("  </div>")
            seen_groups.append(group)
            nav_parts.append(f'  <div class="group">\n    <div class="group-title">{group}</div>')
        nav_parts.append(f'    <a class="item{{active_{fname}}}" href="{{base}}{fname}.html"><span class="no">{no.replace(" ", "")}</span>{short}</a>')
    nav_parts.append("  </div>")
    nav_html = "\n".join(nav_parts).replace("{base}", "")

    # ---- 首页 ----
    home_frag = (SRC / "home.html").read_text(encoding="utf-8")
    nav_items = [
        f'<a class="item{{active_home}}" href="{{base}}index.html"><span class="no">序</span>教程导读与特性全景</a>'
    ] + nav_parts
    home_nav = "\n".join(nav_items).replace("{base}", "")
    home_html = TEMPLATE.format(
        title="教程导读与特性全景",
        tagline="由浅入深 · 场景驱动 · Java 示例",
        base="",
        body=home_frag,
        pager='<a class="next" href="01-overview.html"><span class="dir">下一章 →</span><span class="pt">第 1 章 认识 AgentScope 2.0</span></a>',
        active_home=" active",
        nav=home_nav,
        year="2026",
    )
    # 首页其他链接 active 类不存在，替换为空
    home_html = re.sub(r"\{active_[^}]+\}", "", home_html)
    home_html = home_html.replace("{base}", "").replace("{active_home}", " active")
    (ROOT / "index.html").write_text(home_html, encoding="utf-8")
    print("index.html")

    # ---- 各章 ----
    for fname, no, title, _short, _group in CHAPTERS:
        frag = (CH / f"{fname}.html").read_text(encoding="utf-8")
        idx = [p[0] for p in pages].index(fname)
        _f, _t, prev, nxt = pages[idx]
        pager_parts = []
        if prev:
            pager_parts.append(f'<a href="{prev[0]}.html"><span class="dir">← 上一章</span><span class="pt">{prev[1]}</span></a>')
        if nxt:
            pager_parts.append(f'<a class="next" href="{nxt[0]}.html"><span class="dir">下一章 →</span><span class="pt">{nxt[1]}</span></a>')
        html_out = TEMPLATE.format(
            title=f"{no} {title}",
            tagline=no + " · " + title,
            base="",
            body=f'<h1><span class="chapter-no">{no}</span>{title}</h1>\n' + frag,
            pager="\n".join(pager_parts),
            active_home="",
            nav=nav_html,
            year="2026",
        )
        html_out = re.sub(r"\{active_[^}]+\}", "", html_out)
        (ROOT / f"{fname}.html").write_text(html_out, encoding="utf-8")
        print(f"{fname}.html")

    # ---- 静态资源 ----
    (ROOT / "style.css").write_text((SRC / "style.css").read_text(encoding="utf-8"), encoding="utf-8")
    print("style.css")


if __name__ == "__main__":
    build()
