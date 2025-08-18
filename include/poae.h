#ifndef POAE_H
#define POAE_H
#include <stdint.h>
typedef int (*poae_fn)(uint64_t t_us, void* ctx);
int poae_run_cycle(uint64_t t_us, poae_fn perceive, poae_fn observe, poae_fn actuate, poae_fn evolve, void* ctx);
#endif
