# 示例代码

与教程正文完全一致的可运行示例。

- `python/`：`server.py`（devbox 服务器）、`client.py`（stdio 客户端）、`test_server.py`（进程内测试）。依赖 `mcp[cli]` 2.x，Python 3.10+。
- `typescript/`：`src/server.ts` 与 `src/client.ts`。依赖 `@modelcontextprotocol/server` / `@modelcontextprotocol/client` 2.x，`npm run build` 编译到 `dist/`。
- `raw/session-2026-07-28.json`：向 Python 示例服务器真实发送的 JSON-RPC 请求与响应记录（协议修订版 2026-07-28）。

运行方式见仓库根目录的 README。
