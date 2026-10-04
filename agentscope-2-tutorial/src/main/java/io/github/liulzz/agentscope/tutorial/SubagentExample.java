package io.github.liulzz.agentscope.tutorial;

import io.agentscope.core.agent.RuntimeContext;
import io.agentscope.core.event.AgentEndEvent;
import io.agentscope.core.event.AgentEvent;
import io.agentscope.core.event.TextBlockDeltaEvent;
import io.agentscope.core.event.ToolCallStartEvent;
import io.agentscope.core.message.UserMessage;
import io.agentscope.core.state.InMemoryAgentStateStore;
import io.agentscope.harness.agent.HarnessAgent;
import io.agentscope.harness.agent.subagent.SubagentDeclaration;

/** Declares a researcher subagent and forwards parent/child events. */
public final class SubagentExample {

    private SubagentExample() {}

    static HarnessAgent buildAgent() {
        return HarnessAgent.builder()
                .name("architecture-lead")
                .sysPrompt("把独立调研交给 researcher，再由你汇总决策、风险和未知项。")
                .model(System.getenv().getOrDefault("AGENTSCOPE_MODEL", "dashscope:qwen-plus"))
                .subagent(SubagentDeclaration.builder()
                        .name("researcher")
                        .description("负责收集技术事实、约束和未知项，不做最终决策。")
                        .inlineAgentsBody("你是技术调研员。输出证据、适用边界、风险和未知项。")
                        .steps(8)
                        .persistSession(true)
                        .build())
                .stateStore(new InMemoryAgentStateStore())
                .maxIters(10)
                .build();
    }

    private static void printEvent(AgentEvent event) {
        String source = event.getSource() == null ? "parent" : event.getSource();
        if (event instanceof TextBlockDeltaEvent delta) {
            System.out.print("[" + source + "] " + delta.getDelta());
        } else if (event instanceof ToolCallStartEvent tool) {
            System.out.println("\n[" + source + "] tool=" + tool.getToolCallName());
        } else if (event instanceof AgentEndEvent) {
            System.out.println("\n[" + source + "] finished");
        }
    }

    public static void main(String[] args) {
        RuntimeContext ctx = RuntimeContext.builder()
                .userId("architect")
                .sessionId("subagent-demo")
                .build();
        try (HarnessAgent agent = buildAgent()) {
            agent.streamEvents(new UserMessage("比较 Redis 与 MySQL 作为 Agent 状态存储。"), ctx)
                    .doOnNext(SubagentExample::printEvent)
                    .blockLast();
        }
    }
}
