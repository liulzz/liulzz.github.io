package io.github.liulzz.agentscope.tutorial;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.agentscope.core.permission.PermissionMode;
import java.util.List;
import org.junit.jupiter.api.Test;

class TutorialExamplesTest {

    @Test
    void shippingToolRunsOfflineAndPublishesSchema() {
        ShippingToolExample.ShippingTools tools = new ShippingToolExample.ShippingTools();
        assertEquals("运费为 21.00 元", tools.calculateShipping(2.5, "remote"));
        assertThrows(IllegalArgumentException.class, () -> tools.calculateShipping(0, "local"));
        assertEquals("calculate_shipping", ShippingToolExample.toolkit().getToolSchemas().get(0).getName());
    }

    @Test
    void environmentAndPermissionsAreSane() {
        assertTrue(Runtime.version().feature() >= 17);
        assertEquals(PermissionMode.DONT_ASK, PermissionExample.permissionPolicy(true).getMode());
        assertEquals(PermissionMode.DEFAULT, PermissionExample.permissionPolicy(false).getMode());
    }

    @Test
    void productionChecklistHasNoOfflineFailures() {
        List<ProductionChecklist.Check> checks = ProductionChecklist.runChecks();
        assertTrue(checks.stream().noneMatch(check -> "FAIL".equals(check.status())));
        assertTrue(checks.stream().anyMatch(check -> "MANUAL".equals(check.status())));
    }
}
