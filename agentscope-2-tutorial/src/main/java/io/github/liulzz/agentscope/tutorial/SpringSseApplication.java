package io.github.liulzz.agentscope.tutorial;

import io.agentscope.core.agent.RuntimeContext;
import io.agentscope.core.event.AgentEvent;
import io.agentscope.core.event.TextBlockDeltaEvent;
import io.agentscope.core.message.UserMessage;
import io.agentscope.harness.agent.HarnessAgent;
import java.nio.file.Paths;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

/** Spring WebFlux adapter that exposes AgentScope events as SSE. */
@SpringBootApplication
public class SpringSseApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringSseApplication.class, args);
    }

    @Configuration(proxyBeanMethods = false)
    static class AgentConfiguration {
        @Bean(destroyMethod = "close")
        HarnessAgent supportAgent() {
            return HarnessAgent.builder()
                    .name("support-agent")
                    .sysPrompt("你是 Java 系统中的客服 Agent。回答简洁，不得编造订单状态。")
                    .model(System.getenv().getOrDefault("AGENTSCOPE_MODEL", "dashscope:qwen-plus"))
                    .workspace(Paths.get(".agentscope", "spring-workspace"))
                    .maxIters(8)
                    .build();
        }
    }

    @RestController
    static class ChatController {
        private final HarnessAgent agent;

        ChatController(HarnessAgent agent) {
            this.agent = agent;
        }

        @GetMapping(path = "/api/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
        Flux<String> stream(
                @RequestParam String message,
                @RequestParam String sessionId,
                @RequestHeader(name = "X-User-ID") String userId,
                @RequestHeader(name = "X-Request-ID", required = false) String requestId) {
            RuntimeContext ctx = RuntimeContext.builder()
                    .userId(userId)
                    .sessionId(sessionId)
                    .put("request_id", requestId == null ? "generated-by-server" : requestId)
                    .build();
            return agent.streamEvents(new UserMessage(message), ctx)
                    .ofType(TextBlockDeltaEvent.class)
                    .map(TextBlockDeltaEvent::getDelta)
                    .timeout(java.time.Duration.ofSeconds(60))
                    .onErrorResume(error -> Flux.just("[ERROR] " + error.getMessage()));
        }

        @GetMapping("/actuator/tutorial-health")
        String health() {
            return "UP";
        }
    }
}
