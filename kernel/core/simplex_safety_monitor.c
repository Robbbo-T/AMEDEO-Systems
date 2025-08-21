#include "simplex_safety_monitor.h"
#include <stdio.h>
#include <string.h>
#include <stdint.h>

/* Global Simplex Safety Monitor Context */
static simplex_context_t g_simplex_ctx;

/* Initialize Simplex Safety Monitor */
int simplex_init(void) {
    memset(&g_simplex_ctx, 0, sizeof(g_simplex_ctx));
    g_simplex_ctx.current_state = SIMPLEX_STATE_NORMAL;
    g_simplex_ctx.active_monitors = 0;
    
    printf("[SIMPLEX] Safety monitor initialized\n");
    return 0;
}

/* Register a safety monitor with check and fallback functions */
int simplex_register_monitor(uint32_t monitor_id, const char *name,
                            int (*check_fn)(uint64_t, void*),
                            int (*fallback_fn)(uint64_t, void*)) {
    if (monitor_id >= SIMPLEX_MAX_MONITORS) {
        return -1;
    }
    
    simplex_monitor_t *monitor = &g_simplex_ctx.monitors[monitor_id];
    monitor->monitor_id = monitor_id;
    monitor->enabled = true;
    monitor->name = name;
    monitor->check_function = check_fn;
    monitor->fallback_function = fallback_fn;
    monitor->violation_count = 0;
    monitor->last_violation = SIMPLEX_VIOLATION_NONE;
    
    g_simplex_ctx.active_monitors++;
    printf("[SIMPLEX] Registered monitor %u: %s\n", monitor_id, name);
    return 0;
}

/* Enable/disable specific monitors */
int simplex_enable_monitor(uint32_t monitor_id) {
    if (monitor_id >= SIMPLEX_MAX_MONITORS) {
        return -1;
    }
    g_simplex_ctx.monitors[monitor_id].enabled = true;
    return 0;
}

int simplex_disable_monitor(uint32_t monitor_id) {
    if (monitor_id >= SIMPLEX_MAX_MONITORS) {
        return -1;
    }
    g_simplex_ctx.monitors[monitor_id].enabled = false;
    return 0;
}

/* Run all enabled monitors and handle violations */
int simplex_run_monitors(uint64_t timestamp_us, void *context) {
    int violations_detected = 0;
    
    for (uint32_t i = 0; i < SIMPLEX_MAX_MONITORS; i++) {
        simplex_monitor_t *monitor = &g_simplex_ctx.monitors[i];
        
        if (!monitor->enabled || !monitor->check_function) {
            continue;
        }
        
        monitor->last_check_us = timestamp_us;
        
        /* Run monitor check function */
        int result = monitor->check_function(timestamp_us, context);
        
        if (result != 0) {
            /* Violation detected */
            monitor->violation_count++;
            g_simplex_ctx.total_violations++;
            violations_detected++;
            
            printf("[SIMPLEX] VIOLATION detected in monitor %u (%s) at t=%llu us\n",
                   monitor->monitor_id, monitor->name, 
                   (unsigned long long)timestamp_us);
            
            /* Activate fallback if available */
            if (monitor->fallback_function) {
                int fallback_result = monitor->fallback_function(timestamp_us, context);
                if (fallback_result == 0) {
                    printf("[SIMPLEX] Fallback activated for monitor %u\n", 
                           monitor->monitor_id);
                    g_simplex_ctx.fallback_activations++;
                } else {
                    printf("[SIMPLEX] CRITICAL: Fallback failed for monitor %u\n", 
                           monitor->monitor_id);
                    g_simplex_ctx.current_state = SIMPLEX_STATE_FAILED;
                    return -1;
                }
            }
            
            /* Update system state based on violation severity */
            if (g_simplex_ctx.current_state == SIMPLEX_STATE_NORMAL) {
                g_simplex_ctx.current_state = SIMPLEX_STATE_DEGRADED;
                g_simplex_ctx.last_state_change_us = timestamp_us;
            }
        }
    }
    
    return violations_detected;
}

/* Get current safety state */
simplex_state_t simplex_get_state(void) {
    return g_simplex_ctx.current_state;
}

/* Get total violation count */
uint32_t simplex_get_violation_count(void) {
    return g_simplex_ctx.total_violations;
}

/* Monitor Hook Functions */

/* Timing monitor - checks for deadline violations and jitter */
int simplex_timing_monitor(uint64_t timestamp_us, void *context) {
    (void)context;
    
    /* Simulate timing check based on current jitter */
    static uint64_t last_check = 0;
    if (last_check == 0) {
        last_check = timestamp_us;
        return 0;
    }
    
    uint64_t delta = timestamp_us - last_check;
    last_check = timestamp_us;
    
    /* Check for excessive jitter (>50us as per requirements) */
    if (delta > 1050 || delta < 950) { /* Allow 5% variance around 1000us period */
        return -1; /* Timing violation */
    }
    
    return 0;
}

/* Envelope monitor - checks operational envelope boundaries */
int simplex_envelope_monitor(uint64_t timestamp_us, void *context) {
    (void)timestamp_us;
    (void)context;
    
    /* Placeholder for envelope checking logic */
    /* In a real system, this would check flight envelope parameters */
    return 0;
}

/* Resource monitor - checks CPU and memory usage */
int simplex_resource_monitor(uint64_t timestamp_us, void *context) {
    (void)timestamp_us;
    (void)context;
    
    /* Placeholder for resource monitoring */
    /* In a real system, this would check partition resource budgets */
    return 0;
}

/* Memory monitor - checks for memory corruption and overruns */
int simplex_memory_monitor(uint64_t timestamp_us, void *context) {
    (void)timestamp_us;
    (void)context;
    
    /* Placeholder for memory monitoring */
    /* In a real system, this would check memory protection and integrity */
    return 0;
}

/* Fallback Policy Functions */

/* Timing fallback - switches to backup timing source */
int simplex_timing_fallback(uint64_t timestamp_us, void *context) {
    (void)timestamp_us;
    (void)context;
    
    printf("[SIMPLEX] Timing fallback: Switching to backup timing source\n");
    return 0;
}

/* Envelope fallback - applies safe control limits */
int simplex_envelope_fallback(uint64_t timestamp_us, void *context) {
    (void)timestamp_us;
    (void)context;
    
    printf("[SIMPLEX] Envelope fallback: Applying safe control limits\n");
    return 0;
}

/* Resource fallback - reduces non-critical processing */
int simplex_resource_fallback(uint64_t timestamp_us, void *context) {
    (void)timestamp_us;
    (void)context;
    
    printf("[SIMPLEX] Resource fallback: Reducing non-critical processing\n");
    return 0;
}

/* Memory fallback - activates memory protection mode */
int simplex_memory_fallback(uint64_t timestamp_us, void *context) {
    (void)timestamp_us;
    (void)context;
    
    printf("[SIMPLEX] Memory fallback: Activating memory protection mode\n");
    return 0;
}

/* Safety Critical Functions */

/* Force fallback for specific violation type */
int simplex_force_fallback(simplex_violation_t violation_type) {
    printf("[SIMPLEX] FORCED FALLBACK: violation type %d\n", violation_type);
    g_simplex_ctx.current_state = SIMPLEX_STATE_FALLBACK;
    g_simplex_ctx.fallback_activations++;
    return 0;
}

/* Emergency shutdown procedure */
int simplex_emergency_shutdown(void) {
    printf("[SIMPLEX] EMERGENCY SHUTDOWN initiated\n");
    g_simplex_ctx.current_state = SIMPLEX_STATE_FAILED;
    
    /* In a real system, this would:
     * 1. Stop all non-critical partitions
     * 2. Activate hardware safety interlocks
     * 3. Log safety event
     * 4. Transition to safe state
     */
    
    return 0;
}

/* Check if system is in safe state */
bool simplex_is_safe_state(void) {
    return (g_simplex_ctx.current_state == SIMPLEX_STATE_NORMAL ||
            g_simplex_ctx.current_state == SIMPLEX_STATE_DEGRADED);
}