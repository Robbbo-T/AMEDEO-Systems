#ifndef TSN_SIM_H
#define TSN_SIM_H
#include <stdint.h>
int tsn_measure(uint32_t* latency_us, uint32_t* jitter_us);
#endif
