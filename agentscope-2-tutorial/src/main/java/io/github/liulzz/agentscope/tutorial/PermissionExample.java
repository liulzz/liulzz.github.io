package io.github.liulzz.agentscope.tutorial;

import io.agentscope.core.ReActAgent;
import io.agentscope.core.message.Msg;
import io.agentscope.core.message.UserMessage;
import io.agentscope.core.permission.PermissionBehavior;
import io.agentscope.core.permission.PermissionContextState;
import io.agentscope.core.permission.PermissionMode;
import io.agentscope.core.permission.PermissionRule;
import io.agentscope.core.tool.Tool;
import io.agentscope.core.tool.ToolParam;
import io.agentscope.core.tool.Toolkit;

/** Shows ALLOW / ASK / DENY guardrails for business tools. */
public final class PermissionExample {

    private PermissionExample() {}

    public static final class OrderTools {
        @Tool(name = "query_order", description = "查询订单状态", readOnly = true)
        public String queryOrder(@ToolParam(name = "orderId", description = "订单号") String orderId) {
            return "订单 " + orderId + " 状态为 PAID";
        }

        @Tool(name = "refund_order", description = "发起退款")
        public String refundOrder(@ToolParam(name = "orderId", description = "订单号") String orderId) {
            return "退款已提交：" + orderId;
        }
    }

    static PermissionContextState permissionPolicy(boolean headless) {
        return PermissionContextState.builder()
                .mode(headless ? PermissionMode.DONT_ASK : PermissionMode.DEFAULT)
                .addAllowRule(
                        "query_order",
                        new PermissionRule(
                                "query_order", null, PermissionBehavior.ALLOW, "tutorial-policy"))
                .addAskRule(
                        "refund_order",
                        new PermissionRule(
                                "refund_order", null, PermissionBehavior.ASK, "tutorial-policy"))
                .build();
    }

    public static void main(String[] args) {
        boolean headless = args.length > 0 && "--headless".equals(args[0]);
        Toolkit toolkit = new Toolkit();
        toolkit.registerTool(new OrderTools());
        ReActAgent agent = ReActAgent.builder()
                .name("order-assistant")
                .sysPrompt("查询可直接执行；退款必须经过权限系统，不得绕过确认。")
                .model(System.getenv().getOrDefault("AGENTSCOPE_MODEL", "dashscope:qwen-plus"))
                .toolkit(toolkit)
                .permissionContext(permissionPolicy(headless))
                .maxIters(8)
                .build();
        Msg result = agent.call(new UserMessage("请退款订单 O-1001")).block();
        System.out.println("generateReason=" + (result == null ? null : result.getGenerateReason()));
        System.out.println(result == null ? "" : result.getTextContent());
        agent.close();
    }
}
