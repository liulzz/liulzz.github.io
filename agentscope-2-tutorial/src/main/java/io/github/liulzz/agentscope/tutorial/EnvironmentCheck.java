package io.github.liulzz.agentscope.tutorial;

import io.agentscope.harness.agent.HarnessAgent;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Verifies the JDK, AgentScope Java version and model credentials. */
public final class EnvironmentCheck {

    private EnvironmentCheck() {}

    public static Map<String, String> inspect() {
        Map<String, String> result = new LinkedHashMap<>();
        int feature = Runtime.version().feature();
        result.put("java", System.getProperty("java.version"));
        result.put("javaStatus", feature >= 17 ? "PASS" : "FAIL");
        String version = detectAgentScopeVersion();
        result.put("agentscope", version == null ? "unknown" : version);
        result.put("agentscopeStatus", "2.0.3".equals(version) ? "PASS" : "WARN");
        result.put(
                "credential",
                hasText(System.getenv("DASHSCOPE_API_KEY"))
                        || hasText(System.getenv("OPENAI_API_KEY"))
                        ? "PASS"
                        : "WARN");
        return result;
    }

    private static boolean hasText(String value) {
        return value != null && !value.isBlank();
    }

    private static String detectAgentScopeVersion() {
        String implementationVersion = HarnessAgent.class.getPackage().getImplementationVersion();
        if (hasText(implementationVersion)) {
            return implementationVersion;
        }
        try {
            String location = HarnessAgent.class
                    .getProtectionDomain()
                    .getCodeSource()
                    .getLocation()
                    .toString();
            Matcher matcher = Pattern.compile("agentscope-harness-([0-9][0-9A-Za-z.-]*)\\.jar")
                    .matcher(location);
            return matcher.find() ? matcher.group(1) : "unknown";
        } catch (RuntimeException ignored) {
            return "unknown";
        }
    }

    public static void main(String[] args) {
        inspect().forEach((key, value) -> System.out.printf("%-18s %s%n", key + ":", value));
    }
}
