# AgentScope Java 2.0.3 中文实战教程

面向 **Java / Spring Boot 开发者**的场景化教程，基于官方 `agentscope-ai/agentscope-java` 的 **v2.0.3**，按“场景 → 理论 → Java 实践 → 验证 → 常见坑 → 挑战 → 小测”组织。

在线站点：https://liulzz.github.io/agentscope-2-tutorial/

## 学习路线

1. JDK 17、Maven 与 AgentScope 模块化依赖
2. `HarnessAgent`、`RuntimeContext`、`Mono` / `Flux`
3. `@Tool`、`@ToolParam` 与 `Toolkit`
4. Java POJO 结构化输出
5. `AgentStateStore` 与多用户会话隔离
6. `MemoryConfig`、`MEMORY.md` 与上下文压缩
7. `SubagentDeclaration` 与多智能体事件转发
8. Permission、Spring WebFlux SSE 与生产门禁

## 版本要求

- JDK 17+
- Maven 3.9+
- AgentScope Java 2.0.3
- Spring Boot 4.0.4（仅 SSE 示例）

## 构建和离线验证

```bash
mvn test
mvn -q exec:java \
  -Dexec.mainClass=io.github.liulzz.agentscope.tutorial.EnvironmentCheck
mvn -q exec:java \
  -Dexec.mainClass=io.github.liulzz.agentscope.tutorial.ShippingToolExample \
  -Dexec.args="--tool-only"
mvn -q exec:java \
  -Dexec.mainClass=io.github.liulzz.agentscope.tutorial.ProductionChecklist
```

这些命令不需要模型 API Key。需要真实模型的示例读取环境变量：

```bash
export DASHSCOPE_API_KEY="..."
export AGENTSCOPE_MODEL="dashscope:qwen-plus"
```

也可以添加对应模型扩展后使用 `openai:*`、`anthropic:*`、`gemini:*` 或 `ollama:*`。

## 启动 Spring WebFlux SSE 示例

```bash
mvn spring-boot:run \
  -Dspring-boot.run.main-class=io.github.liulzz.agentscope.tutorial.SpringSseApplication

curl -N \
  -H 'X-User-ID: alice' \
  -H 'X-Request-ID: req-001' \
  'http://localhost:8080/api/chat/stream?sessionId=s1&message=你好'
```

## 本地浏览教程

```bash
python3 -m http.server 8000
```

打开 `http://localhost:8000`。Python 只用于启动静态文件服务器，教程代码和测试全部是 Java。

## 目录

```text
.
├── index.html
├── styles.css
├── pom.xml
├── src/main/java/io/github/liulzz/agentscope/tutorial/
├── src/test/java/io/github/liulzz/agentscope/tutorial/
└── .github/workflows/pages.yml
```

## 生产边界

- 核心业务规则、金额、权限和状态机继续由 Java 领域服务负责。
- 多副本生产不要使用本地 JSON 状态，切换到 Redis、MySQL 或 PostgreSQL。
- Local filesystem 可执行宿主命令，不是安全沙箱；不可信代码使用 Docker、Kubernetes、AgentRun 或 E2B。
- 高风险工具使用 ASK / DENY；无人值守任务使用 `DONT_ASK`，不要直接 `BYPASS`。

## 许可证

MIT，见 [LICENSE](LICENSE)。AgentScope Java 本身采用 Apache-2.0。
