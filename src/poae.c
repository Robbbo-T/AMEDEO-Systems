#include "poae.h"
int poae_run_cycle(uint64_t t, poae_fn p, poae_fn o, poae_fn a, poae_fn e, void *c)
{
    if (p)
    {
        p(t, c);
    }
    if (o)
    {
        o(t, c);
    }
    if (a)
    {
        a(t, c);
    }
    if (e)
    {
        e(t, c);
    }
    return 0;
}
