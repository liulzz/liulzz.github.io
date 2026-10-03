/**
 * devbox：与 Python 示例同一业务的 MCP 服务器（TypeScript 实现）。
 *
 * 传输方式为 stdio：JSON-RPC 消息经标准输入输出流动，
 * 因此日志一律写入标准错误，避免破坏协议消息流。
 */
import { McpServer, ResourceTemplate } from '@modelcontextprotocol/server';
import { StdioServerTransport } from '@modelcontextprotocol/server/stdio';
import { createHash } from 'node:crypto';
import * as z from 'zod/v4';

const server = new McpServer({ name: 'devbox', version: '1.0.0' });

const SNIPPETS: Record<string, string> = {
  python: 'if __name__ == "__main__":\n    main()\n',
  typescript: 'export function main(): void {\n    // ...\n}\n',
  sql: 'SELECT 1;\n',
};

// ---------- 工具 ----------

server.registerTool(
  'hash_text',
  {
    title: '文本摘要',
    description: '计算一段文本的密码学摘要值。',
    inputSchema: z.object({
      text: z.string().describe('待计算的原始文本'),
      algorithm: z
        .enum(['sha256', 'sha1', 'md5'])
        .default('sha256')
        .describe('摘要算法名称'),
    }),
    outputSchema: z.object({
      algorithm: z.string(),
      hexdigest: z.string(),
      length: z.number().int(),
    }),
  },
  async ({ text, algorithm }) => {
    const hexdigest = createHash(algorithm).update(text, 'utf8').digest('hex');
    console.error(`hash_text: algorithm=${algorithm} length=${text.length}`);
    return {
      content: [{ type: 'text', text: hexdigest }],
      structuredContent: { algorithm, hexdigest, length: text.length },
    };
  },
);

server.registerTool(
  'json_format',
  {
    title: 'JSON 格式化',
    description: '把一段 JSON 文本格式化为缩进清晰的形式。',
    inputSchema: z.object({
      text: z.string().describe('待格式化的 JSON 文本'),
      indent: z.number().int().min(0).max(8).default(2).describe('缩进空格数'),
    }),
  },
  async ({ text, indent }) => {
    const formatted = JSON.stringify(JSON.parse(text), null, indent);
    return { content: [{ type: 'text', text: formatted }] };
  },
);

// ---------- 资源 ----------

server.registerResource(
  'style-guide',
  'devbox://docs/style-guide',
  { title: '代码风格指南', mimeType: 'text/markdown' },
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        mimeType: 'text/markdown',
        text: '# 代码风格指南\n\n1. 命名使用完整英文单词。\n2. 公共函数必须书写类型标注。\n',
      },
    ],
  }),
);

server.registerResource(
  'snippet',
  new ResourceTemplate('devbox://snippets/{lang}', {
    // 列表回调必须显式声明；传 undefined 表示不支持枚举全部实例。
    list: undefined,
  }),
  { title: '语言模板片段', mimeType: 'text/plain' },
  async (uri, variables) => {
    const lang = String(variables.lang);
    const text = SNIPPETS[lang];
    if (text === undefined) {
      throw new Error(`暂无该语言的模板：${lang}`);
    }
    return { contents: [{ uri: uri.href, mimeType: 'text/plain', text }] };
  },
);

// ---------- 提示模板 ----------

server.registerPrompt(
  'review_code',
  {
    title: '代码评审',
    description: '生成一份代码评审提示模板。',
    argsSchema: z.object({
      language: z.string().describe('被评审代码使用的编程语言'),
      code: z.string().describe('被评审代码的正文'),
    }),
  },
  ({ language, code }) => ({
    messages: [
      {
        role: 'user' as const,
        content: {
          type: 'text' as const,
          text:
            `请对下面这段 ${language} 代码做评审，` +
            '依次检查正确性、可读性与潜在风险，并给出修改建议：\n\n' +
            '```' + language + '\n' + code + '\n```',
        },
      },
    ],
  }),
);

// ---------- 启动 ----------

async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('devbox server running on stdio');
}

main().catch((error: unknown) => {
  console.error('fatal:', error);
  process.exit(1);
});
