#ifndef DET_H
#define DET_H
#include <stddef.h>
#include <stdint.h>
int det_init(const char* path);
int det_log(const char* tag, const void* data, size_t len, uint64_t t_us);
#endif
