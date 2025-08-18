#include "pqc.h"
#include <string.h>
int pqc_load_mock_keys(void){ return 0; }
int pqc_sign(const uint8_t* msg, size_t mlen, uint8_t* sig, size_t* siglen){
  const char* mock="MOCKSIG_KYBER_DILITHIUM";
  (void)msg; (void)mlen;
  memcpy(sig,mock,strlen(mock));
  *siglen = strlen(mock);
  return 0;
}
