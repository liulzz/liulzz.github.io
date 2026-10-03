/**
 * devbox 客户端示例：以 stdio 子进程方式启动服务器并完成一轮完整交互。
 */
import { Client } from '@modelcontextprotocol/client';
import { StdioClientTransport } from '@modelcontextprotocol/client/stdio';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));

async function main(): Promise<void> {
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [path.join(here, 'server.js')],
  });

  const client = new Client({ name: 'devbox-client', version: '1.0.0' });
  await client.connect(transport);

  // 1. 列出工具
  const tools = await client.listTools();
  console.log('== 工具列表 ==');
  for (const tool of tools.tools) {
    console.log(`- ${tool.name}: ${tool.description}`);
  }

  // 2. 调用工具
  const result = await client.callTool({
    name: 'hash_text',
    arguments: { text: 'hello mcp', algorithm: 'sha256' },
  });
  console.log('\n== hash_text 结果 ==');
  console.log(JSON.stringify(result.structuredContent, null, 2));

  // 3. 列出并读取资源
  const resources = await client.listResources();
  const templates = await client.listResourceTemplates();
  console.log('\n== 资源列表 ==');
  for (const item of resources.resources) {
    console.log(`- ${item.uri} (${item.title})`);
  }
  for (const item of templates.resourceTemplates) {
    console.log(`- ${item.uriTemplate} (模板)`);
  }

  const doc = await client.readResource({ uri: 'devbox://docs/style-guide' });
  console.log('\n== 读取资源 devbox://docs/style-guide ==');
  for (const content of doc.contents) {
    console.log('text' in content ? content.text : JSON.stringify(content));
  }

  // 4. 获取提示模板
  const prompt = await client.getPrompt({
    name: 'review_code',
    arguments: { language: 'python', code: 'x = 1' },
  });
  console.log('\n== 提示模板 review_code ==');
  for (const message of prompt.messages) {
    console.log(message.role, ':', message.content.type === 'text' ? message.content.text : '');
  }

  await client.close();
}

main().catch((error: unknown) => {
  console.error('fatal:', error);
  process.exit(1);
});
