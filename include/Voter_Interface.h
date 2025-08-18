#ifndef VOTER_INTERFACE_H
#define VOTER_INTERFACE_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

typedef struct { float elevon_l, elevon_r; } CtrlOut;
typedef enum { VOTE_EQUAL = 0, VOTE_MISMATCH = 1 } vote_result_t;

int voter_compare(const CtrlOut* cpu, const CtrlOut* fpga, const CtrlOut* dsp, float eps);
/* Returns pointer to last consensus result; ata_code used for logging/routing */
const CtrlOut* voter_get_consensed_result(uint32_t ata_code);

#ifdef __cplusplus
}
#endif
#endif
