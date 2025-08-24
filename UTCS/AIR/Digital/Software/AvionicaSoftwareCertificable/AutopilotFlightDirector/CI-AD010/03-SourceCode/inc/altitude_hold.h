/**
 * @file altitude_hold.h
 * @brief Altitude hold mode logic header for CI-AD010 AutopilotComputer
 * @version 1.0
 * @date 2024
 * @classification DAL-C Compliance
 */

#ifndef ALTITUDE_HOLD_H
#define ALTITUDE_HOLD_H

#include "apc_common.h"

/**
 * @brief Initialize altitude hold module
 * @return int Status code (0 = success)
 */
int altitude_hold_init(void);

/**
 * @brief Engage altitude hold mode
 * @param current_altitude Current aircraft altitude
 * @return int Status code (0 = success)
 */
int altitude_hold_engage(float current_altitude);

/**
 * @brief Execute altitude hold control
 * @param input Sensor input data
 * @param output Control output data
 * @return int Status code (0 = success)
 */
int altitude_hold_execute(const sensor_data_t* input, control_output_t* output);

#endif /* ALTITUDE_HOLD_H */