#ifndef ARINC653_PARTITION_H
#define ARINC653_PARTITION_H

#include <stdint.h>

/**
 * ARINC 653-like partition scheduler interface
 * Supports time/space partitioning for AQUA-OS/ADT
 */

/* Initialize the partition scheduler */
void arinc653_init(void);

/* Execute scheduling for current time */
int arinc653_schedule(uint64_t current_time_us);

/* Get worst-case jitter bound */
int arinc653_get_worst_case_jitter_us(void);

#endif /* ARINC653_PARTITION_H */