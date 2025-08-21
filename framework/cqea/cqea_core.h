#ifndef CQEA_CORE_H
#define CQEA_CORE_H

#include <stdint.h>

/**
 * CQEA (Coherent Quantum Error Analysis) Framework
 * Interfaces for quantum-enhanced control systems
 */

typedef struct {
    double phi_sync;      /* Trace-norm metric */
    double tau_ctl;       /* Control latency */
    double tau_max;       /* Maximum allowed latency */
    uint64_t timestamp_us;
} cqea_sync_metric_t;

/* Calculate φ_sync trace-norm metric */
double cqea_calculate_phi_sync(double coherence_factor, double decoherence_rate, double time_s);

/* Check bounded-latency constraint: τ_ctl ≤ τ_max */
int cqea_bounded_latency_check(double tau_ctl, double tau_max);

/* Run MPC demo with quantum enhancement */
int cqea_run_mpc_demo(uint64_t timestamp_us);

/* Get last computed metric */
cqea_sync_metric_t cqea_get_last_metric(void);

#endif /* CQEA_CORE_H */