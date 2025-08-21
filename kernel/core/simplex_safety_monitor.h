#ifndef SIMPLEX_SAFETY_MONITOR_H
#define SIMPLEX_SAFETY_MONITOR_H

#include <stdint.h>
#include <stdbool.h>

/* Simplex Safety Monitor for DO-178C Compliance
 * Implements monitor hooks and fallback policy for deterministic kernel
 */

#define SIMPLEX_MAX_MONITORS 8
#define SIMPLEX_TIMEOUT_US 2000  /* 2 periods max for takeover */

typedef enum {
    SIMPLEX_STATE_NORMAL = 0,
    SIMPLEX_STATE_DEGRADED,
    SIMPLEX_STATE_FALLBACK,
    SIMPLEX_STATE_FAILED
} simplex_state_t;

typedef enum {
    SIMPLEX_VIOLATION_NONE = 0,
    SIMPLEX_VIOLATION_TIMING,
    SIMPLEX_VIOLATION_ENVELOPE,
    SIMPLEX_VIOLATION_RESOURCE,
    SIMPLEX_VIOLATION_MEMORY,
    SIMPLEX_VIOLATION_COMMUNICATION
} simplex_violation_t;

typedef struct {
    uint32_t monitor_id;
    bool enabled;
    uint64_t last_check_us;
    uint32_t violation_count;
    simplex_violation_t last_violation;
    const char *name;
    int (*check_function)(uint64_t timestamp_us, void *context);
    int (*fallback_function)(uint64_t timestamp_us, void *context);
} simplex_monitor_t;

typedef struct {
    simplex_state_t current_state;
    uint32_t active_monitors;
    uint64_t last_state_change_us;
    uint32_t total_violations;
    uint32_t fallback_activations;
    simplex_monitor_t monitors[SIMPLEX_MAX_MONITORS];
} simplex_context_t;

/* Core Functions */
int simplex_init(void);
int simplex_register_monitor(uint32_t monitor_id, const char *name,
                            int (*check_fn)(uint64_t, void*),
                            int (*fallback_fn)(uint64_t, void*));
int simplex_enable_monitor(uint32_t monitor_id);
int simplex_disable_monitor(uint32_t monitor_id);
int simplex_run_monitors(uint64_t timestamp_us, void *context);
simplex_state_t simplex_get_state(void);
uint32_t simplex_get_violation_count(void);

/* Monitor Hook Functions */
int simplex_timing_monitor(uint64_t timestamp_us, void *context);
int simplex_envelope_monitor(uint64_t timestamp_us, void *context);
int simplex_resource_monitor(uint64_t timestamp_us, void *context);
int simplex_memory_monitor(uint64_t timestamp_us, void *context);

/* Fallback Policy Functions */
int simplex_timing_fallback(uint64_t timestamp_us, void *context);
int simplex_envelope_fallback(uint64_t timestamp_us, void *context);
int simplex_resource_fallback(uint64_t timestamp_us, void *context);
int simplex_memory_fallback(uint64_t timestamp_us, void *context);

/* Safety Critical Functions */
int simplex_force_fallback(simplex_violation_t violation_type);
int simplex_emergency_shutdown(void);
bool simplex_is_safe_state(void);

#endif /* SIMPLEX_SAFETY_MONITOR_H */