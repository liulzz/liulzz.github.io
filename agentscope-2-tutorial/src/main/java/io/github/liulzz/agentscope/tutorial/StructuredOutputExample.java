package io.github.liulzz.agentscope.tutorial;

import io.agentscope.core.ReActAgent;
import io.agentscope.core.agent.RuntimeContext;
import io.agentscope.core.message.Msg;
import io.agentscope.core.message.UserMessage;
import java.util.List;

/** Binds an agent response to a Java POJO. */
public final class StructuredOutputExample {

    private StructuredOutputExample() {}

    public static final class Ticket {
        public String category;
        public String priority;
        public String summary;
        public String nextAction;

        public Ticket() {}

        @Override
        public String toString() {
            return "Ticket{" + "category='" + category + '\'' + ", priority='" + priority + '\''
                    + ", summary='" + summary + '\'' + ", nextAction='" + nextAction + '\'' + '}';
        }
    }

    public static void main(String[] args) {
        ReActAgent agent = ReActAgent.builder()
                .name("ticket-classifier")
                .sysPrompt("把客户邮件分类为 billing、technical、account 或 other。")
                .model(System.getenv().getOrDefault("AGENTSCOPE_MODEL", "dashscope:qwen-plus"))
                .maxIters(8)
                .build();
        RuntimeContext ctx = RuntimeContext.builder()
                .userId("demo-user")
                .sessionId("structured-output")
                .build();
        Msg msg = agent.call(
                        List.of(new UserMessage(
                                "重置密码后仍无法登录，报表马上要提交，请生成工单。")),
                        Ticket.class,
                        ctx)
                .block();
        Ticket ticket = msg == null ? null : msg.getStructuredData(Ticket.class);
        System.out.println(ticket);
        agent.close();
    }
}
