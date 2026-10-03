"""devbox 客户端示例：以 stdio 子进程方式启动服务器并完成一轮完整交互。

依次演示：列出工具、调用工具、列出资源、读取资源、获取提示模板。
"""

import asyncio
import json
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters

SERVER_PATH = Path(__file__).with_name("server.py")


async def main() -> None:
    # 使用当前解释器启动服务器，保证服务器与客户端处于同一环境。
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
    )
    async with Client(params) as client:
        # 1. 列出工具
        tools = await client.list_tools()
        print("== 工具列表 ==")
        for tool in tools.tools:
            print(f"- {tool.name}: {tool.description}")

        # 2. 调用工具
        result = await client.call_tool(
            "hash_text", {"text": "hello mcp", "algorithm": "sha256"}
        )
        print("\n== hash_text 结果 ==")
        print(json.dumps(result.structured_content, ensure_ascii=False, indent=2))

        result = await client.call_tool("json_format", {"text": '{"a":1,"b":[2,3]}'})
        print("\n== json_format 结果 ==")
        for block in result.content:
            print(block.text)

        # 3. 列出资源（直接资源与资源模板）
        resources = await client.list_resources()
        templates = await client.list_resource_templates()
        print("\n== 资源列表 ==")
        for item in resources.resources:
            print(f"- {item.uri} ({item.title})")
        for item in templates.resource_templates:
            print(f"- {item.uri_template} (模板)")

        # 4. 读取资源
        doc = await client.read_resource("devbox://docs/style-guide")
        print("\n== 读取资源 devbox://docs/style-guide ==")
        for content in doc.contents:
            print(content.text)

        snippet = await client.read_resource("devbox://snippets/python")
        print("== 读取资源 devbox://snippets/python ==")
        for content in snippet.contents:
            print(content.text)

        # 5. 获取提示模板
        prompt = await client.get_prompt(
            "review_code",
            {"language": "python", "code": "def add(a,b):\n    return a+b"},
        )
        print("\n== 提示模板 review_code ==")
        for message in prompt.messages:
            print(message.role, ":", message.content.text)


if __name__ == "__main__":
    asyncio.run(main())
