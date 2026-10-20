from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX_PATH = ROOT / "index.html"

CATEGORY_ORDER = [
    "📖 速查手册",
    "🤖 AgentScope 智能体框架",
    "🔌 MCP 模型上下文协议",
    "🌐 建站 / 部署",
    "🛒 消费分析",
]

DEFAULT_META = {
    "wsl-cheatsheet": {"ico": "🐧", "name": "WSL 命令大全", "desc": "WSL — The Complete Command Atlas"},
    "log-cheatsheet": {"ico": "📜", "name": "Linux 查日志工具箱", "desc": "Linux 查日志 — The Complete Log Toolkit"},
    "kubectl-cheatsheet": {"ico": "☸️", "name": "kubectl 命令大全", "desc": "kubectl — The Complete Command Atlas"},
    "java-vscode-cheatsheet": {"ico": "☕", "name": "Java × VS Code 速查", "desc": "Java 开发高频操作与 Language Server 技巧"},
    "auth-token-storage": {"ico": "🔐", "name": "前端 Token 存储安全", "desc": "认证 Token 存储安全 · 速查"},
    "agentscope-tutorial": {"ico": "🧩", "name": "AgentScope Java 2.0 入门", "desc": "从消息模型到生产部署 · 15 章体系教程"},
    "agentscope-tutorial-ds": {"ico": "🎓", "name": "智能体场景课", "desc": "AgentScope 2.0 学习手册 · 理论 + 实践 + 自测"},
    "agentscope-tutorial-glm": {"ico": "📚", "name": "AgentScope Java 2.0 新手入门完整版", "desc": "21 章场景式学习"},
    "agentscope-harness": {"ico": "🧪", "name": "AgentScope Harness 设计拆解", "desc": "拆解 HarnessAgent 设计思想与实现原理"},
    "agentscope-2-tutorial": {"ico": "⚙️", "name": "AgentScope Java 2.0.3 实战", "desc": "用 Java 构建生产级智能体系统"},
    "mcp-tutorial": {"ico": "🔗", "name": "MCP 由浅入深教程", "desc": "Model Context Protocol 完全指南"},
    "mcp-tutorial-2026": {"ico": "🧭", "name": "MCP 完全教程 2026", "desc": "从协议动机到服务端 / 客户端实现"},
    "mcp-learning-guide": {"ico": "📘", "name": "MCP 学习指南", "desc": "从协议基础到生产实现 · 含示例与源码"},
    "github-pages-tutorial": {"ico": "🚀", "name": "GitHub Pages 教程", "desc": "由浅入深 · 10 分钟拥有免费网站"},
    "mojimac-price": {"ico": "💻", "name": "摩集电商 MacBook 价格分析", "desc": "MacBook Pro 价格全景分析 · V2EX"},
}

CATEGORY_MAP = {
    "📖 速查手册": {"wsl-cheatsheet", "log-cheatsheet", "kubectl-cheatsheet", "java-vscode-cheatsheet", "auth-token-storage"},
    "🤖 AgentScope 智能体框架": {"agentscope-tutorial", "agentscope-tutorial-ds", "agentscope-tutorial-glm", "agentscope-harness", "agentscope-2-tutorial"},
    "🔌 MCP 模型上下文协议": {"mcp-tutorial", "mcp-tutorial-2026", "mcp-learning-guide"},
    "🌐 建站 / 部署": {"github-pages-tutorial"},
    "🛒 消费分析": {"mojimac-price"},
}


def detect_category(repo: str) -> str:
    if repo in CATEGORY_MAP["📖 速查手册"]:
        return "📖 速查手册"
    if repo in CATEGORY_MAP["🤖 AgentScope 智能体框架"]:
        return "🤖 AgentScope 智能体框架"
    if repo in CATEGORY_MAP["🔌 MCP 模型上下文协议"]:
        return "🔌 MCP 模型上下文协议"
    if repo in CATEGORY_MAP["🌐 建站 / 部署"]:
        return "🌐 建站 / 部署"
    if repo in CATEGORY_MAP["🛒 消费分析"]:
        return "🛒 消费分析"
    if repo.startswith("agentscope"):
        return "🤖 AgentScope 智能体框架"
    if repo.startswith("mcp"):
        return "🔌 MCP 模型上下文协议"
    if "cheatsheet" in repo or "guide" in repo:
        return "📖 速查手册"
    return "🌐 建站 / 部署"


def build_data() -> list[dict]:
    scanned = [
        p.name for p in sorted(ROOT.iterdir(), key=lambda p: p.name)
        if p.is_dir() and not p.name.startswith(".")
    ]
    grouped: dict[str, list[dict]] = {cat: [] for cat in CATEGORY_ORDER}

    for repo in scanned:
        category = detect_category(repo)
        meta = DEFAULT_META.get(repo, {
            "ico": "📦",
            "name": repo.replace("-", " ").replace("_", " ").title(),
            "desc": "自动发现的项目页面",
        })
        grouped.setdefault(category, []).append({
            "ico": meta["ico"],
            "name": meta["name"],
            "desc": meta["desc"],
            "repo": repo,
        })

    ordered = []
    for cat in CATEGORY_ORDER:
        items = grouped.get(cat, [])
        if items:
            ordered.append({"cat": cat, "items": items})

    # Append any additional categories not in the base order.
    for cat, items in grouped.items():
        if cat not in CATEGORY_ORDER and items:
            ordered.append({"cat": cat, "items": items})

    return ordered


def render_page(data: list[dict]) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>liulzz · 项目导航</title>
<style>
  :root{{
    --bg:#f7f8fa; --card:#ffffff; --ink:#1f2329; --sub:#646a73;
    --line:#e5e6eb; --accent:#3370ff; --accent-soft:#eaf0ff;
    --shadow:0 1px 3px rgba(0,0,0,.04),0 4px 16px rgba(0,0,0,.04);
    --shadow-h:0 4px 12px rgba(51,112,255,.12),0 12px 32px rgba(0,0,0,.08);
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
    background:var(--bg); color:var(--ink); line-height:1.6;
    -webkit-font-smoothing:antialiased;
  }}
  .wrap{{max-width:1080px; margin:0 auto; padding:56px 24px 80px}}
  header{{margin-bottom:44px}}
  .title{{font-size:34px; font-weight:700; letter-spacing:-.5px; display:flex; align-items:center; gap:12px}}
  .title .dot{{width:12px;height:12px;border-radius:50%;background:var(--accent);display:inline-block}}
  .subtitle{{color:var(--sub); font-size:15px; margin-top:10px}}
  .subtitle b{{color:var(--ink)}}
  .search{{
    margin-top:24px; width:100%; max-width:420px; padding:11px 16px;
    border:1px solid var(--line); border-radius:10px; font-size:15px;
    background:var(--card); color:var(--ink); outline:none; transition:.2s;
  }}
  .search:focus{{border-color:var(--accent); box-shadow:0 0 0 3px var(--accent-soft)}}
  .cat{{margin-top:40px}}
  .cat-head{{display:flex; align-items:center; gap:10px; margin-bottom:16px}}
  .cat-head h2{{font-size:16px; font-weight:600}}
  .cat-head .count{{font-size:12px; color:var(--sub); background:var(--line); padding:2px 9px; border-radius:20px}}
  .grid{{display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:16px; align-items:stretch}}
  .card{{
    display:flex; flex-direction:column; background:var(--card); border:1px solid var(--line);
    border-radius:14px; padding:20px; text-decoration:none; color:inherit;
    box-shadow:var(--shadow); transition:.22s cubic-bezier(.4,0,.2,1); position:relative; overflow:hidden;
  }}
  .card::before{{content:""; position:absolute; left:0; top:0; bottom:0; width:3px; background:var(--accent); transform:scaleY(0); transform-origin:top; transition:.22s}}
  .card:hover{{transform:translateY(-3px); box-shadow:var(--shadow-h); border-color:#c9d5f0}}
  .card:hover::before{{transform:scaleY(1)}}
  .card .ico{{font-size:22px; margin-bottom:10px}}
  .card .name{{font-size:16px; font-weight:600; margin-bottom:6px}}
  .card .desc{{font-size:13px; color:var(--sub); min-height:20px}}
  .card .repo{{font-size:11px; color:#a6abb3; margin-top:auto; padding-top:12px; font-family:ui-monospace,"SF Mono",Menlo,monospace}}
  footer{{margin-top:64px; text-align:center; color:#a6abb3; font-size:13px}}
  footer a{{color:var(--accent); text-decoration:none}}
  .no-result{{display:none; color:var(--sub); padding:40px 0; text-align:center}}
  @media (max-width:600px){{.wrap{{padding:36px 16px 60px}}.title{{font-size:26px}}}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="title"><span class="dot"></span>项目导航</div>
    <div class="subtitle">liulzz 的 GitHub Pages 作品集 · 共 <b id="total">—</b> 个在线项目</div>
    <input class="search" id="q" placeholder="🔍 搜索项目…" autocomplete="off">
  </header>

  <div id="cats"></div>
  <div class="no-result" id="nr">没有匹配的项目 🤔</div>

  <footer>
    Built with ❤ · <a href="https://github.com/liulzz" target="_blank">github.com/liulzz</a>
  </footer>
</div>

<script>
const DATA={payload};
const BASE="./";
const catsEl=document.getElementById("cats");
function render(){{
  catsEl.innerHTML="";
  DATA.forEach(c=>{{
    const sec=document.createElement("div"); sec.className="cat"; sec.dataset.cat="1";
    sec.innerHTML=`<div class="cat-head"><h2>${{c.cat}}</h2><span class="count">${{c.items.length}}</span></div>`;
    const grid=document.createElement("div"); grid.className="grid";
    c.items.forEach(it=>{{
      const a=document.createElement("a"); a.className="card"; a.href=BASE+it.repo+"/"; a.target="_blank";
      a.dataset.key=(it.name+" "+it.desc+" "+it.repo).toLowerCase();
      a.innerHTML=`<div class="ico">${{it.ico}}</div><div class="name">${{it.name}}</div><div class="desc">${{it.desc}}</div><div class="repo">${{it.repo}}</div>`;
      grid.appendChild(a);
    }});
    sec.appendChild(grid); catsEl.appendChild(sec);
  }});
}}
render();
document.getElementById("total").textContent=DATA.reduce((n,c)=>n+c.items.length,0);
document.getElementById("q").addEventListener("input",e=>{{
  const q=e.target.value.trim().toLowerCase();
  let any=false;
  document.querySelectorAll(".cat").forEach(sec=>{{
    let vis=0;
    sec.querySelectorAll(".card").forEach(card=>{{
      const m=!q||card.dataset.key.includes(q);
      card.style.display=m?"":"none"; if(m)vis++;
    }});
    sec.style.display=vis?"":"none"; if(vis)any=true;
  }});
  document.getElementById("nr").style.display=any?"none":"block";
}});
</script>
</body>
</html>
'''


def main() -> None:
    data = build_data()
    INDEX_PATH.write_text(render_page(data), encoding="utf-8")
    total = sum(len(cat["items"]) for cat in data)
    print(f"Homepage generated: {total} projects across {len(data)} sections")


if __name__ == "__main__":
    main()
