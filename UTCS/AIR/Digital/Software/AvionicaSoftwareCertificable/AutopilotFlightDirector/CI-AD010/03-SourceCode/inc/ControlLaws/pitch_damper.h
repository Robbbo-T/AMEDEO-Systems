/**
 * @file pitch_damper.h
 * @brief Pitch damper control law header for CI-AD010 AutopilotComputer
 * @version 1.0
 * @date 2024
 * @classification DAL-C Compliance
 */

#ifndef PITCH_DAMPER_H
#define PITCH_DAMPER_H

#include "apc_common.h"

/**
 * @brief Initialize pitch damper module
 * @return int Status code (0 = success)
 */
int pitch_damper_init(void);

/**
 * @brief Execute pitch damper control law
 * @param input Sensor input data
 * @param output Control output data
 * @return int Status code (0 = success)
 */
int pitch_damper_execute(const sensor_data_t* input, control_output_t* output);

#endif /* PITCH_DAMPER_H */