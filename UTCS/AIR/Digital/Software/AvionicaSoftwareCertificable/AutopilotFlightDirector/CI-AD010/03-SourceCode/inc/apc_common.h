/**
 * @file apc_common.h
 * @brief Common definitions and types for CI-AD010 AutopilotComputer
 * @version 1.0
 * @date 2024
 * @classification DAL-C Compliance
 */

#ifndef APC_COMMON_H
#define APC_COMMON_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

/**
 * @brief Sensor data structure
 */
typedef struct {
    float altitude;         /**< Current altitude in feet */
    float airspeed;         /**< Current airspeed in knots */
    float pitch_angle;      /**< Current pitch angle in degrees */
    float roll_angle;       /**< Current roll angle in degrees */
    float pitch_rate;       /**< Current pitch rate in deg/sec */
    float roll_rate;        /**< Current roll rate in deg/sec */
    float yaw_rate;         /**< Current yaw rate in deg/sec */
} sensor_data_t;

/**
 * @brief Control output structure
 */
typedef struct {
    float pitch_cmd;        /**< Pitch command in degrees */
    float roll_cmd;         /**< Roll command in degrees */
    float rudder_cmd;       /**< Rudder command in degrees */
    float throttle_cmd;     /**< Throttle command (0.0 to 1.0) */
} control_output_t;

/**
 * @brief System status enumeration
 */
typedef enum {
    APC_STATUS_INIT = 0,    /**< System initializing */
    APC_STATUS_READY,       /**< System ready */
    APC_STATUS_ACTIVE,      /**< System active */
    APC_STATUS_FAULT        /**< System fault */
} apc_status_t;

#endif /* APC_COMMON_H */