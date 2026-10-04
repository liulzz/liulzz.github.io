package io.github.liulzz.agentscope.tutorial;

import io.agentscope.core.agent.RuntimeContext;
import io.agentscope.core.message.Msg;
import io.agentscope.core.message.UserMessage;
import io.agentscope.harness.agent.HarnessAgent;
import io.agentscope.harness.agent.memory.MemoryConfig;
import io.agentscope.harness.agent.memory.compaction.CompactionConfig;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;

/** Uses HarnessAgent's daily memory log, MEMORY.md and context compaction. */
public final class LongTermMemoryExample {

    private static final Path WORKSPACE = Path.of(".agentscope", "memory-workspace");

    private LongTermMemoryExample() {}

    static HarnessAgent buildAgent() {
        return HarnessAgent.builder()
                .name("long-term-assistant")
                .sysPrompt("只保存稳定且未来有价值的用户偏好，不保存密码、令牌或身份证号。")
                .model(System.getenv().getOrDefault("AGENTSCOPE_MODEL", "dashscope:qwen-plus"))
                .workspace(WORKSPACE)
                .memory(MemoryConfig.builder()
                        .flushTrigger(MemoryConfig.FlushTrigger.throttled(Duration.ofMinutes(10)))
                        .dailyFileRetentionDays(30)
                        .sessionRetentionDays(60)
                        .build())
                .compaction(CompactionConfig.builder()
                        .triggerMessages(30)
                        .keepMessages(10)
                        .build())
                .maxIters(8)
                .build();
    }

    private static void inspect() throws Exception {
        if (!Files.exists(WORKSPACE)) {
            System.out.println("尚无记忆文件，请先运行 remember。运行模型需要相应 API Key。");
            return;
        }
        try (var paths = Files.walk(WORKSPACE)) {
            paths.filter(Files::isRegularFile)
                    .map(WORKSPACE::relativize)
                    .sorted()
                    .forEach(System.out::println);
        }
    }

    public static void main(String[] args) throws Exception {
        String mode = args.length == 0 ? "inspect" : args[0];
        if ("inspect".equals(mode)) {
            inspect();
            return;
        }
        RuntimeContext ctx = RuntimeContext.builder()
                .userId("alice")
                .sessionId("memory-demo")
                .build();
        try (HarnessAgent agent = buildAgent()) {
            String prompt = "remember".equals(mode)
                    ? "请记住：我偏好先给结论，代码示例使用 Java。"
                    : "请按我的偏好解释什么是 Reactor Mono。";
            Msg result = agent.call(new UserMessage(prompt), ctx).block();
            System.out.println(result == null ? "" : result.getTextContent());
        }
    }
}
