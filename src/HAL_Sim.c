#include "HAL_Interface.h"
#include <math.h>
#include <stdio.h>
#include <time.h>

static uint64_t t0;
static uint64_t mono_us()
{
#if defined(_WIN32)
    /* Fallback monotonic approx for Windows */
    return 0;
#else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000ull + ts.tv_nsec / 1000ull;
#endif
}

int hal_read_sensors(CtrlIn *x, uint64_t tick_us)
{
    double t = tick_us / 1e6;
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
    x->aoa_deg = 5.0f + 2.0f * (float)sin(2 * M_PI * 0.2 * t);
    x->tas_mps = 220.0f + 5.0f * (float)sin(2 * M_PI * 0.1 * t);
    x->roll_cmd = 0.5f * (float)sin(2 * M_PI * 0.5 * t);
    x->pitch_cmd = 0.3f * (float)sin(2 * M_PI * 0.4 * t);
    x->yaw_cmd = 0.2f * (float)sin(2 * M_PI * 0.3 * t);
    return 0;
}
int hal_write_actuators(const void *y, uint64_t len, uint64_t tick_us)
{
    (void)y;
    (void)len;
    (void)tick_us;
    return 0;
}
uint64_t hal_now_us(void)
{
    if (!t0)
        t0 = mono_us();
    return mono_us() - t0;
}
