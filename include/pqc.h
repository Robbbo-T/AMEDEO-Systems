#ifndef PQC_H
#define PQC_H
#include <stddef.h>
#include <stdint.h>
int pqc_load_mock_keys(void);
int pqc_sign(const uint8_t* msg, size_t mlen, uint8_t* sig, size_t* siglen);
#endif
