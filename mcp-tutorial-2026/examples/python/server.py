"""devbox：一个面向开发场景的 MCP 服务器示例。

包含三种核心能力：工具（tool）、资源（resource）、提示模板（prompt）。
以 stdio 传输方式运行：JSON-RPC 消息经标准输入输出流动，日志写入标准错误。
"""

import hashlib
import json
import logging
from datetime import datetime
from typing import TypedDict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ResourceNotFoundError, ToolError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = MCPServer("devbox", version="1.0.0")

SNIPPETS = {
    "python": "if __name__ == \"__main__\":\n    main()\n",
    "typescript": "export function main(): void {\n    // ...\n}\n",
    "sql": "SELECT 1;\n",
}


class HashResult(TypedDict):
    """hash_text 的结构化输出。"""

    algorithm: str
    hexdigest: str
    length: int


@mcp.tool()
def hash_text(text: str, algorithm: str = "sha256") -> HashResult:
    """计算一段文本的密码学摘要值。

    Args:
        text: 待计算的原始文本。
        algorithm: 摘要算法名称，可选 sha256、sha1、md5，默认 sha256。

    Returns:
        包含 algorithm、hexdigest、length 三个字段的字典。
    """
    if algorithm not in {"sha256", "sha1", "md5"}:
        raise ToolError(f"不支持的算法：{algorithm}")
    digest = hashlib.new(algorithm, text.encode("utf-8")).hexdigest()
    logger.info("hash_text: algorithm=%s length=%d", algorithm, len(text))
    return {"algorithm": algorithm, "hexdigest": digest, "length": len(text)}


@mcp.tool()
def json_format(text: str, indent: int = 2) -> str:
    """把一段 JSON 文本格式化为缩进清晰的形式。

    Args:
        text: 待格式化的 JSON 文本。
        indent: 缩进空格数，默认 2。

    Returns:
        格式化之后的 JSON 文本。
    """
    data = json.loads(text)
    return json.dumps(data, ensure_ascii=False, indent=indent)


@mcp.tool()
def tz_now(timezone: str = "UTC", fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """查询某个时区的当前时间。

    Args:
        timezone: IANA 时区名称，例如 Asia/Shanghai、UTC。
        fmt: 输出格式，采用 strftime 格式串。

    Returns:
        按指定格式渲染的当前时间文本。
    """
    try:
        zone = ZoneInfo(timezone)
    except ZoneInfoNotFoundError as exc:
        raise ToolError(f"未知时区：{timezone}") from exc
    return datetime.now(zone).strftime(fmt)


@mcp.resource(
    "devbox://docs/style-guide",
    title="代码风格指南",
    mime_type="text/markdown",
)
def style_guide() -> str:
    """返回团队代码风格指南的正文。"""
    return "# 代码风格指南\n\n1. 命名使用完整英文单词。\n2. 公共函数必须书写类型标注。\n"


@mcp.resource(
    "devbox://snippets/{lang}",
    title="语言模板片段",
    mime_type="text/plain",
)
def snippet(lang: str) -> str:
    """按语言名称返回一段模板代码。

    Args:
        lang: 语言名称，可选 python、typescript、sql。
    """
    if lang not in SNIPPETS:
        raise ResourceNotFoundError(f"暂无该语言的模板：{lang}")
    return SNIPPETS[lang]


@mcp.prompt(title="代码评审")
def review_code(language: str, code: str) -> list[dict]:
    """生成一份代码评审提示模板。

    Args:
        language: 被评审代码使用的编程语言。
        code: 被评审代码的正文。
    """
    return [
        {
            "role": "user",
            "content": (
                f"请对下面这段 {language} 代码做评审，"
                "依次检查正确性、可读性与潜在风险，并给出修改建议：\n\n"
                f"```{language}\n{code}\n```"
            ),
        }
    ]


if __name__ == "__main__":
    # stdio 传输：stdin 读取请求，stdout 输出响应，日志写入 stderr。
    mcp.run(transport="stdio")
