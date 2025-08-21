#ifndef HAL_INTERFACE_H
#define HAL_INTERFACE_H
#include <stdint.h>
typedef struct
{
    float aoa_deg, tas_mps;
    float roll_cmd, pitch_cmd, yaw_cmd;
} CtrlIn;

int      hal_read_sensors(CtrlIn *x, uint64_t tick_us);
int      hal_write_actuators(const void *y, uint64_t len, uint64_t tick_us);
uint64_t hal_now_us(void);
#endif
