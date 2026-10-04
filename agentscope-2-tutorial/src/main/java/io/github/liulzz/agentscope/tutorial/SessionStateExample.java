package io.github.liulzz.agentscope.tutorial;

import io.agentscope.core.ReActAgent;
import io.agentscope.core.agent.RuntimeContext;
import io.agentscope.core.message.Msg;
import io.agentscope.core.message.UserMessage;
import io.agentscope.core.state.AgentStateStore;
import io.agentscope.core.state.JsonFileAgentStateStore;
import java.nio.file.Path;
import java.util.List;

/** Demonstrates per-call RuntimeContext and persisted multi-user session state. */
public final class SessionStateExample {

    private SessionStateExample() {}

    static ReActAgent buildAgent(AgentStateStore stateStore) {
        return ReActAgent.builder()
                .name("session-assistant")
                .sysPrompt("记住当前会话里的项目名称，并用一句话回答。")
                .model(System.getenv().getOrDefault("AGENTSCOPE_MODEL", "dashscope:qwen-plus"))
                .stateStore(stateStore)
                .maxIters(8)
                .build();
    }

    public static void main(String[] args) {
        Path stateDir = Path.of(".agentscope", "state-demo");
        AgentStateStore stateStore = new JsonFileAgentStateStore(stateDir);
        RuntimeContext alice = RuntimeContext.builder()
                .userId("alice")
                .sessionId("project-session")
                .put("request_id", "req-state-001")
                .build();

        ReActAgent first = buildAgent(stateStore);
        Msg seeded = first.call(List.of(new UserMessage("我的项目叫北极星。")), alice).block();
        System.out.println("第一轮：" + (seeded == null ? "" : seeded.getTextContent()));
        first.close();

        ReActAgent restored = buildAgent(stateStore);
        Msg answer = restored.call(List.of(new UserMessage("我的项目叫什么？")), alice).block();
        System.out.println("恢复后：" + (answer == null ? "" : answer.getTextContent()));
        restored.close();
    }
}
