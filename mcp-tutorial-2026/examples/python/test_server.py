"""devbox 服务器的进程内测试：无需子进程与网络。

运行方式：python test_server.py（也可以被 pytest 直接收集）
"""

import asyncio

from mcp import Client

from server import mcp


def test_hash_text_structured_output():
    async def run():
        async with Client(mcp) as client:
            tools = await client.list_tools()
            assert {t.name for t in tools.tools} == {"hash_text", "json_format", "tz_now"}

            result = await client.call_tool(
                "hash_text", {"text": "hello mcp", "algorithm": "sha256"}
            )
            assert result.is_error is False
            assert result.structured_content["algorithm"] == "sha256"
            assert len(result.structured_content["hexdigest"]) == 64

    asyncio.run(run())


def test_unknown_algorithm_is_tool_error():
    async def run():
        async with Client(mcp) as client:
            result = await client.call_tool(
                "hash_text", {"text": "x", "algorithm": "crc32"}
            )
            assert result.is_error is True
            assert "不支持的算法" in result.content[0].text

    asyncio.run(run())


def test_resource_and_prompt():
    async def run():
        async with Client(mcp) as client:
            doc = await client.read_resource("devbox://docs/style-guide")
            assert "代码风格指南" in doc.contents[0].text

            prompt = await client.get_prompt(
                "review_code", {"language": "python", "code": "x = 1"}
            )
            assert prompt.messages[0].role == "user"
            assert "python" in prompt.messages[0].content.text

    asyncio.run(run())


if __name__ == "__main__":
    test_hash_text_structured_output()
    test_unknown_algorithm_is_tool_error()
    test_resource_and_prompt()
    print("3 项测试全部通过")
