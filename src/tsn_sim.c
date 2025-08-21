#include "tsn_sim.h"
#include <stdint.h>

/* Deterministic LCG for repeatable results */
static uint32_t lcg_state = 123456789u;
static uint32_t lcg_next(void)
{
    lcg_state = 1103515245u * lcg_state + 12345u;
    return (lcg_state >> 16) & 0x7FFFu; /* 15-bit */
}

int tsn_measure(uint32_t *lat, uint32_t *jit)
{
    uint32_t r1 = lcg_next();
    uint32_t r2 = lcg_next();
    *lat = 150u + (r1 % 40u); /* ~150-189 us */
    *jit = 1u + (r2 % 3u);    /* 1-3 us */
    return 0;
}
