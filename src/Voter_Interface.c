#include "Voter_Interface.h"
#include <math.h>
static CtrlOut last;

static int eq(const CtrlOut *a, const CtrlOut *b, float e)
{
    return fabsf(a->elevon_l - b->elevon_l) <= e && fabsf(a->elevon_r - b->elevon_r) <= e;
}
int voter_compare(const CtrlOut *c, const CtrlOut *f, const CtrlOut *d, float eps)
{
    int cf = eq(c, f, eps), cd = eq(c, d, eps), fd = eq(f, d, eps);
    if ((cf && cd) || (cf && fd) || (cd && fd))
    {
        /* majority select */
        const CtrlOut *m = cf ? c : (cd ? c : f);
        last = *m;
        return VOTE_EQUAL;
    }
    return VOTE_MISMATCH;
}
const CtrlOut *voter_get_consensed_result(uint32_t ata_code)
{
    (void)ata_code;
    return &last;
}
