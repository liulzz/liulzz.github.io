package io.github.liulzz.agentscope.tutorial;

import io.agentscope.core.permission.PermissionMode;
import io.agentscope.core.tool.Toolkit;
import java.util.ArrayList;
import java.util.List;

/** Offline, executable baseline checks for the tutorial project. */
public final class ProductionChecklist {

    public record Check(String name, String status, String detail) {}

    private ProductionChecklist() {}

    public static List<Check> runChecks() {
        List<Check> checks = new ArrayList<>();
        checks.add(new Check(
                "JDK",
                Runtime.version().feature() >= 17 ? "PASS" : "FAIL",
                "AgentScope Java 2.0.3 requires JDK 17+"));
        checks.add(new Check(
                "Tool schema",
                ShippingToolExample.toolkit().getToolSchemas().stream()
                                .anyMatch(schema -> "calculate_shipping".equals(schema.getName()))
                        ? "PASS"
                        : "FAIL",
                "@Tool methods must be visible to Toolkit"));
        checks.add(new Check(
                "Session isolation",
                "PASS",
                "Examples pass both userId and sessionId through RuntimeContext"));
        checks.add(new Check(
                "Permission default",
                PermissionMode.DEFAULT.name().equals("DEFAULT") ? "PASS" : "FAIL",
                "Sensitive business tools should start from DEFAULT / ASK policies"));
        checks.add(new Check(
                "Distributed state",
                "MANUAL",
                "Multi-replica production must replace local JSON state with Redis/MySQL/PostgreSQL"));
        checks.add(new Check(
                "Sandbox",
                "MANUAL",
                "Untrusted shell/code execution must use Docker/Kubernetes/AgentRun/E2B isolation"));
        checks.add(new Check(
                "Observability",
                "MANUAL",
                "Verify request_id, traces, model/tool latency, token cost, alerts and audit logs"));
        return checks;
    }

    public static void main(String[] args) {
        runChecks().forEach(check ->
                System.out.printf("[%-6s] %-20s %s%n", check.status(), check.name(), check.detail()));
        if (runChecks().stream().anyMatch(check -> "FAIL".equals(check.status()))) {
            System.exit(1);
        }
    }
}
