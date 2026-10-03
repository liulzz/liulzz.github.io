# MCP 由浅入深：大模型上下文协议完全教程

本仓库是 GitHub Pages 教程站点的源码，主题是 LLM 语境下的 MCP（Model Context Protocol）。

## 内容结构

- `index.html`：教程正文，共 14 个章节，从动机、架构、协议报文讲到 Python 与 TypeScript 实战、调试测试、进阶模式、安全实践与版本演进。
- `assets/`：样式表与交互脚本（主题切换、阅读进度、目录高亮、代码复制）。
- `examples/python/`：Python 示例（`mcp` 2.x），包含服务器 `server.py`、客户端 `client.py`、测试 `test_server.py`。
- `examples/typescript/`：TypeScript 示例（`@modelcontextprotocol/server` / `client` 2.x），源码在 `src/`。
- `examples/raw/session-2026-07-28.json`：对示例服务器真实调用的 JSON-RPC 报文记录。

## 运行示例

Python（需要 Python 3.10+）：

```bash
cd examples/python
uv venv && source .venv/bin/activate
uv add "mcp[cli]"
python client.py      # 启动服务器并完成一轮端到端交互
python test_server.py # 进程内测试
```

TypeScript（需要 Node.js 18+）：

```bash
cd examples/typescript
npm install
npm run build
node dist/client.js
```

## 版本基准

- MCP 规范：`2026-07-28`
- Python SDK：`mcp` 2.2.0
- TypeScript 包：`@modelcontextprotocol/server` / `@modelcontextprotocol/client` 2.0.0

示例代码均已实际编译并运行验证。协议与 SDK 持续演进，阅读时请以官方文档为准。
