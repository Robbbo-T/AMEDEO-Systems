#include <stdio.h>
#include <string.h>
#include <math.h>
#include "Voter_Interface.h"
#include "HAL_Interface.h"
#include "det.h"
#include "tsn_sim.h"
#include "poae.h"

typedef struct { CtrlIn xin; CtrlOut y_cpu, y_fpga, y_dsp, y_out; } Ctx;

static CtrlOut law_cpu(const CtrlIn* x){ CtrlOut y={ x->pitch_cmd*0.8f, x->pitch_cmd*0.8f }; return y; }
static CtrlOut law_fpga(const CtrlIn* x){ CtrlOut y={ x->pitch_cmd*0.8f, x->pitch_cmd*0.8f }; return y; }
static CtrlOut law_dsp(const CtrlIn* x){ CtrlOut y={ x->pitch_cmd*0.8f, x->pitch_cmd*0.8f }; return y; }

static int perceive(uint64_t t, void* ctx){ Ctx* c=(Ctx*)ctx; (void)t; return hal_read_sensors(&c->xin,t); }
static int observe(uint64_t t, void* ctx){ (void)t; (void)ctx; return 0; }
static int actuate(uint64_t t, void* ctx){
  Ctx* c=(Ctx*)ctx;
  c->y_cpu  = law_cpu(&c->xin);
  c->y_fpga = law_fpga(&c->xin);
  c->y_dsp  = law_dsp(&c->xin);

  if (voter_compare(&c->y_cpu, &c->y_fpga, &c->y_dsp, 1e-4f) != VOTE_EQUAL){
    fprintf(stderr,"[VOTE] mismatch at t=%llu us\n",(unsigned long long)t); return -1;
  }
  c->y_out = *voter_get_consensed_result(0x27);
  hal_write_actuators(&c->y_out, sizeof(c->y_out), t);
  det_log("ATA27_STEP",&c->y_out,sizeof(c->y_out), t);
  return 0;
}
static int evolve(uint64_t t, void* ctx){ (void)t; (void)ctx; return 0; }

int main(void){
  det_init("out/det.log");
  Ctx ctx; memset(&ctx,0,sizeof(ctx));
  const int steps=1000, period_us=1000; /* 1 kHz */
  for(int i=0;i<steps;i++){
    uint64_t t = hal_now_us();
    if (poae_run_cycle(t, perceive, observe, actuate, evolve, &ctx) != 0) return 1;
    /* TSN metrics (synthetic) */
    uint32_t lat,jit; tsn_measure(&lat,&jit);
    if (jit > 1000) { fprintf(stderr,"[TSN] jitter too high\n"); return 2; }
    /* busy-wait to approximate 1kHz in host */
    while((hal_now_us() - t) < (uint64_t)period_us) {}
  }
  printf("[OK] 1000 steps @1kHz, 2oo3 consensus maintained.\n");
  return 0;
}
