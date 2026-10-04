package io.github.liulzz.agentscope.tutorial;

import io.agentscope.core.agent.RuntimeContext;
import io.agentscope.core.event.AgentEventType;
import io.agentscope.core.event.TextBlockDeltaEvent;
import io.agentscope.core.message.Msg;
import io.agentscope.core.message.UserMessage;
import io.agentscope.harness.agent.HarnessAgent;
import java.nio.file.Paths;

/** Builds the first long-running HarnessAgent and demonstrates call / streamEvents. */
public final class FirstAgent {

    private FirstAgent() {}

    static HarnessAgent buildAgent() {
        return HarnessAgent.builder()
                .name("requirement-assistant")
                .sysPrompt("你是需求澄清助手。先总结目标和约束，再提出下一步问题。")
                .model(System.getenv().getOrDefault("AGENTSCOPE_MODEL", "dashscope:qwen-plus"))
                .workspace(Paths.get(".agentscope/workspace"))
                .maxIters(8)
                .build();
    }

    public static void main(String[] args) {
        RuntimeContext ctx = RuntimeContext.builder()
                .userId("demo-user")
                .sessionId("first-agent")
                .put("request_id", "req-first-agent")
                .build();

        try (HarnessAgent agent = buildAgent()) {
            if (args.length > 0 && "--stream".equals(args[0])) {
                agent.streamEvents(new UserMessage("我想做一个智能客服，但需求还不清楚。"), ctx)
                        .filter(event -> event.getType() == AgentEventType.TEXT_BLOCK_DELTA)
                        .cast(TextBlockDeltaEvent.class)
                        .doOnNext(event -> System.out.print(event.getDelta()))
                        .blockLast();
                System.out.println();
            } else {
                Msg result = agent.call(
                                new UserMessage("我想做一个智能客服，但需求还不清楚。"), ctx)
                        .block();
                System.out.println(result == null ? "" : result.getTextContent());
            }
        }
    }
}
