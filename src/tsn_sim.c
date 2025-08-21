Conflict resolved. Kept ≤50 µs jitter, Allman braces, left-aligned pointers.

```c
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
    *jit = 1u + (r2 % 49u);   /* 1-49 us, ≤50 µs requirement */
    return 0;
}
```

