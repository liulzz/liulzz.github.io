package io.github.liulzz.agentscope.tutorial;

import io.agentscope.core.ReActAgent;
import io.agentscope.core.agent.RuntimeContext;
import io.agentscope.core.message.Msg;
import io.agentscope.core.message.UserMessage;
import io.agentscope.core.tool.Tool;
import io.agentscope.core.tool.ToolParam;
import io.agentscope.core.tool.Toolkit;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;

/** Registers deterministic Java business logic as AgentScope tools. */
public final class ShippingToolExample {

    private ShippingToolExample() {}

    public static final class ShippingTools {
        @Tool(
                name = "calculate_shipping",
                description = "按重量和区域计算人民币运费。",
                readOnly = true,
                concurrencySafe = true)
        public String calculateShipping(
                @ToolParam(name = "weightKg", description = "包裹重量，必须大于 0")
                        double weightKg,
                @ToolParam(name = "destination", description = "区域：local 或 remote")
                        String destination) {
            if (weightKg <= 0) {
                throw new IllegalArgumentException("weightKg 必须大于 0");
            }
            BigDecimal base;
            BigDecimal extra;
            if ("local".equals(destination)) {
                base = BigDecimal.valueOf(8);
                extra = BigDecimal.valueOf(2);
            } else if ("remote".equals(destination)) {
                base = BigDecimal.valueOf(15);
                extra = BigDecimal.valueOf(4);
            } else {
                throw new IllegalArgumentException("destination 只能是 local 或 remote");
            }
            BigDecimal price = base.add(
                    BigDecimal.valueOf(Math.max(0D, weightKg - 1D)).multiply(extra));
            return "运费为 " + price.setScale(2, RoundingMode.HALF_UP) + " 元";
        }
    }

    static Toolkit toolkit() {
        Toolkit toolkit = new Toolkit();
        toolkit.registerTool(new ShippingTools());
        return toolkit;
    }

    public static void main(String[] args) {
        ShippingTools tools = new ShippingTools();
        if (args.length > 0 && "--tool-only".equals(args[0])) {
            System.out.println(tools.calculateShipping(2.5, "remote"));
            toolkit().getToolSchemas().forEach(schema ->
                    System.out.println(schema.getName() + " -> " + schema.getParameters()));
            return;
        }

        ReActAgent agent = ReActAgent.builder()
                .name("shipping-assistant")
                .sysPrompt("涉及运费时必须调用 calculate_shipping，不得心算。")
                .model(System.getenv().getOrDefault("AGENTSCOPE_MODEL", "dashscope:qwen-plus"))
                .toolkit(toolkit())
                .maxIters(8)
                .build();
        RuntimeContext ctx = RuntimeContext.builder()
                .userId("demo-user")
                .sessionId("shipping-tool")
                .build();
        Msg result = agent.call(
                        List.of(new UserMessage("2.5kg 的包裹寄往 remote 区域要多少钱？")), ctx)
                .block();
        System.out.println(result == null ? "" : result.getTextContent());
        agent.close();
    }
}
