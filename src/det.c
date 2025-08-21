#include "det.h"
#include <stdio.h>
static FILE *fp;
int          det_init(const char *path)
{
    fp = fopen(path, "wb");
    return fp ? 0 : -1;
}
int det_log(const char *tag, const void *data, size_t len, uint64_t t_us)
{
    if (!fp)
        return -1;
    fprintf(fp, "t_us=%llu tag=%s len=%zu\n", (unsigned long long)t_us, tag, len);
    fwrite(data, 1, len, fp);
    fputc('\n', fp);
    fflush(fp);
    return 0;
}
