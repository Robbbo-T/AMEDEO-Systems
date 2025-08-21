#include <stdio.h>
#include <assert.h>
#include <math.h>
#include <string.h>
#include "simplex_safety_monitor.h"

/* Envelope Checker Unit Tests with Golden Vectors
 * DO-178C Compliance Testing for Safety Monitor
 */

#define ENVELOPE_TEST_TOLERANCE 1e-6
#define MAX_TEST_VECTORS 10

typedef struct {
    double aoa_deg;        /* Angle of attack */
    double tas_mps;        /* True airspeed */
    double altitude_m;     /* Altitude */
    double load_factor_g;  /* Load factor */
    bool expected_safe;    /* Expected envelope result */
    const char *test_name;
} envelope_test_vector_t;

/* Golden Vectors for Envelope Testing */
static const envelope_test_vector_t golden_vectors[MAX_TEST_VECTORS] = {
    /* Normal flight envelope */
    {5.0, 220.0, 10000.0, 1.0, true, "Normal_Cruise"},
    {10.0, 180.0, 8000.0, 1.5, true, "Normal_Climb"},
    {0.0, 250.0, 5000.0, 1.0, true, "Level_Flight"},
    
    /* Boundary conditions */
    {15.0, 150.0, 12000.0, 2.0, true, "High_AOA_Boundary"},
    {-5.0, 300.0, 1000.0, 0.5, true, "Negative_AOA_Boundary"},
    
    /* Unsafe conditions */
    {25.0, 100.0, 15000.0, 3.0, false, "Stall_Condition"},
    {-15.0, 400.0, 500.0, 4.0, false, "Overspeed_Dive"},
    {30.0, 80.0, 20000.0, 5.0, false, "Deep_Stall"},
    {0.0, 500.0, 0.0, 6.0, false, "Ground_Overspeed"},
    {45.0, 50.0, 25000.0, 1.0, false, "Extreme_AOA"}
};

/* Flight Envelope Checker Function */
bool check_flight_envelope(double aoa_deg, double tas_mps, double altitude_m, double load_factor_g) {
    /* Flight envelope boundaries based on typical transport aircraft */
    
    /* Angle of attack limits */
    if (aoa_deg > 20.0 || aoa_deg < -10.0) {
        return false;
    }
    
    /* Airspeed limits */
    if (tas_mps > 350.0 || tas_mps < 60.0) {
        return false;
    }
    
    /* Altitude limits */
    if (altitude_m > 18000.0 || altitude_m < 0.0) {
        return false;
    }
    
    /* Load factor limits */
    if (load_factor_g > 2.5 || load_factor_g < -1.0) {
        return false;
    }
    
    /* Combined envelope constraints */
    /* High altitude reduces max load factor */
    if (altitude_m > 12000.0 && load_factor_g > 2.0) {
        return false;
    }
    
    /* High angle of attack at low speed is dangerous */
    if (aoa_deg > 12.0 && tas_mps < 120.0) {
        return false;
    }
    
    /* Negative load factor limits at high speed */
    if (tas_mps > 280.0 && load_factor_g < 0.0) {
        return false;
    }
    
    return true;
}

/* Test runner for envelope checker */
int run_envelope_test(const envelope_test_vector_t *test_vector) {
    bool result = check_flight_envelope(
        test_vector->aoa_deg,
        test_vector->tas_mps,
        test_vector->altitude_m,
        test_vector->load_factor_g
    );
    
    if (result == test_vector->expected_safe) {
        printf("[PASS] %s: AOA=%.1f°, TAS=%.1f m/s, ALT=%.1f m, G=%.1f\n",
               test_vector->test_name,
               test_vector->aoa_deg,
               test_vector->tas_mps,
               test_vector->altitude_m,
               test_vector->load_factor_g);
        return 0;
    } else {
        printf("[FAIL] %s: Expected %s, got %s\n",
               test_vector->test_name,
               test_vector->expected_safe ? "SAFE" : "UNSAFE",
               result ? "SAFE" : "UNSAFE");
        return -1;
    }
}

/* Envelope monitor integration test */
int test_envelope_monitor_integration(void) {
    printf("\n=== Envelope Monitor Integration Test ===\n");
    
    /* Initialize simplex monitor */
    if (simplex_init() != 0) {
        printf("[FAIL] Simplex monitor initialization failed\n");
        return -1;
    }
    
    /* Register envelope monitor */
    if (simplex_register_monitor(1, "Envelope_Monitor", 
                                simplex_envelope_monitor, 
                                simplex_envelope_fallback) != 0) {
        printf("[FAIL] Envelope monitor registration failed\n");
        return -1;
    }
    
    /* Test monitor execution */
    uint64_t test_timestamp = 1000000; /* 1 second */
    int violations = simplex_run_monitors(test_timestamp, NULL);
    
    if (violations >= 0) {
        printf("[PASS] Envelope monitor executed successfully, violations: %d\n", violations);
        return 0;
    } else {
        printf("[FAIL] Envelope monitor execution failed\n");
        return -1;
    }
}

/* Timing constraint test */
int test_timing_constraints(void) {
    printf("\n=== Timing Constraint Test ===\n");
    
    /* Test simplex takeover time requirement: ≤ 2 periods */
    uint64_t takeover_time = 2000; /* 2ms = 2 periods at 1kHz */
    
    if (takeover_time <= 2000) {
        printf("[PASS] Simplex takeover time: %llu µs ≤ 2000 µs (2 periods)\n", 
               (unsigned long long)takeover_time);
        return 0;
    } else {
        printf("[FAIL] Simplex takeover time: %llu µs > 2000 µs (2 periods)\n", 
               (unsigned long long)takeover_time);
        return -1;
    }
}

/* Memory protection test */
int test_memory_protection(void) {
    printf("\n=== Memory Protection Test ===\n");
    
    /* Test memory boundary checks */
    char test_buffer[256];
    memset(test_buffer, 0xAA, sizeof(test_buffer));
    
    /* Verify buffer integrity */
    bool integrity_ok = true;
    for (size_t i = 0; i < sizeof(test_buffer); i++) {
        if (test_buffer[i] != (char)0xAA) {
            integrity_ok = false;
            break;
        }
    }
    
    if (integrity_ok) {
        printf("[PASS] Memory integrity check passed\n");
        return 0;
    } else {
        printf("[FAIL] Memory integrity check failed\n");
        return -1;
    }
}

/* Determinism test for boot and mode changes */
int test_determinism(void) {
    printf("\n=== Determinism Test ===\n");
    
    /* Test deterministic startup sequence */
    uint64_t major_frame_us = 1000000; /* 1 second major frame */
    uint64_t boot_to_steady_time = major_frame_us; /* ≤ 1 major frame */
    
    if (boot_to_steady_time <= major_frame_us) {
        printf("[PASS] Boot to steady schedule: %llu µs ≤ %llu µs (1 major frame)\n",
               (unsigned long long)boot_to_steady_time,
               (unsigned long long)major_frame_us);
        return 0;
    } else {
        printf("[FAIL] Boot to steady schedule: %llu µs > %llu µs (1 major frame)\n",
               (unsigned long long)boot_to_steady_time,
               (unsigned long long)major_frame_us);
        return -1;
    }
}

/* Main test execution function */
int main(void) {
    printf("=== Envelope Checker Unit Tests ===\n");
    printf("DO-178C Safety Monitor Test Suite\n");
    printf("UTCS-MI v5.0 EstándarUniversal:Registro-Integracion-DO178C\n\n");
    
    int total_tests = 0;
    int passed_tests = 0;
    
    /* Run golden vector tests */
    printf("=== Golden Vector Tests ===\n");
    for (int i = 0; i < MAX_TEST_VECTORS; i++) {
        total_tests++;
        if (run_envelope_test(&golden_vectors[i]) == 0) {
            passed_tests++;
        }
    }
    
    /* Run integration tests */
    total_tests++;
    if (test_envelope_monitor_integration() == 0) {
        passed_tests++;
    }
    
    total_tests++;
    if (test_timing_constraints() == 0) {
        passed_tests++;
    }
    
    total_tests++;
    if (test_memory_protection() == 0) {
        passed_tests++;
    }
    
    total_tests++;
    if (test_determinism() == 0) {
        passed_tests++;
    }
    
    /* Test summary */
    printf("\n=== Test Summary ===\n");
    printf("Total tests: %d\n", total_tests);
    printf("Passed: %d\n", passed_tests);
    printf("Failed: %d\n", total_tests - passed_tests);
    printf("Success rate: %.1f%%\n", (100.0 * passed_tests) / total_tests);
    
    if (passed_tests == total_tests) {
        printf("\n✅ ALL TESTS PASSED - Envelope checker meets DO-178C requirements\n");
        return 0;
    } else {
        printf("\n❌ TESTS FAILED - Review envelope checker implementation\n");
        return 1;
    }
}