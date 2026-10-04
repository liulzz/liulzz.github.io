package io.github.liulzz.agentscope.tutorial;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.Test;

class SiteStructureTest {

    private static final Path ROOT = Path.of(System.getProperty("user.dir"));

    @Test
    void siteContainsEightCompleteJavaScenarios() throws IOException {
        String html = Files.readString(ROOT.resolve("index.html"));
        for (int chapter = 1; chapter <= 8; chapter++) {
            assertTrue(html.contains("id: " + chapter + ","));
        }
        for (String heading : List.of("场景", "理论", "实践", "运行与验证", "常见坑", "挑战任务", "本章小测")) {
            assertTrue(html.contains(heading), heading);
        }
        assertTrue(html.contains("AgentScope Java 2.0.3"));
        assertTrue(html.contains("Spring WebFlux"));
    }

    @Test
    void allPublishedExamplesAreJavaAndPresent() {
        Path source = ROOT.resolve("src/main/java/io/github/liulzz/agentscope/tutorial");
        List<String> expected = List.of(
                "EnvironmentCheck.java",
                "FirstAgent.java",
                "ShippingToolExample.java",
                "StructuredOutputExample.java",
                "SessionStateExample.java",
                "LongTermMemoryExample.java",
                "SubagentExample.java",
                "SpringSseApplication.java");
        expected.forEach(file -> assertTrue(Files.isRegularFile(source.resolve(file)), file));
        assertFalse(Files.exists(ROOT.resolve("requirements.txt")));
        assertFalse(Files.exists(ROOT.resolve("examples")));
        assertFalse(Files.exists(ROOT.resolve("tests")));
    }

    @Test
    void buildAndPagesWorkflowUseJava() throws IOException {
        String pom = Files.readString(ROOT.resolve("pom.xml"));
        String workflow = Files.readString(ROOT.resolve(".github/workflows/pages.yml"));
        assertTrue(pom.contains("<agentscope.version>2.0.3</agentscope.version>"));
        assertTrue(pom.contains("<maven.compiler.release>17</maven.compiler.release>"));
        assertTrue(workflow.contains("actions/setup-java@"));
        assertTrue(workflow.contains("mvn --batch-mode --no-transfer-progress test"));
        assertTrue(workflow.contains("cp src/main/java"));
        assertFalse(workflow.contains("setup-python"));
        assertEquals(1, count(workflow, "pages: write"));
    }

    private static int count(String text, String token) {
        int count = 0;
        for (int index = 0; (index = text.indexOf(token, index)) >= 0; index += token.length()) {
            count++;
        }
        return count;
    }
}