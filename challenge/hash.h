#include<string.h>
#include<stdint.h>

#define HASH_LEN (9*4)

#define ROTL32(x, y) (((x) << (y)) | ((x) >> ((sizeof(uint32_t)*8) - (y))))

#define F(X, Y, Z) (((X) & (Y)) | ((~(X)) & (Z)))
#define G(X, Y, Z) (((X) & (Z)) | (Y & (~(Z))))
#define H(X, Y, Z) ((X) ^ (Y) ^ (Z))
#define I(X, Y, Z) ((Y) ^ ((X) | (~(Z))))

void update(char* buf, uint8_t c) { 
  int val[9];
  int vval[4];
  memcpy(val, buf, sizeof(int) * 9);
  for (int i = 4; i < 9; i++) {
    val[i] = ROTL32(val[i - 4], 5) + F(ROTL32(val[i - 3], 23), ROTL32(val[i - 2], 29), ROTL32(val[i - 1], 3));
  }

  for (int i = 0; i < 9; i++) {
    val[i] ^= G(ROTL32(0xdeadbeefU, c & 15), ROTL32(0xcafebabeU, c >> 4), ROTL32(0xfee1f2eeU, 8 - (c >> 4))) + c*998244353;
  }

  __asm__ __volatile__ (
      "movdqu (%0), %%xmm0        \n\t"
      "movdqu (%1), %%xmm1        \n\t"
      "pmaddwd %%xmm1, %%xmm0     \n\t"
      "movdqu %%xmm0, (%2)        \n\t"
      :
      : "r"(&val[0]), "r"(&val[4]), "r"(&vval[0])
      : "xmm0", "xmm1", "memory"
  );

  for(int i = 0; i < 9; i++) {
    int t = val[(i + 4) % 9] ^ ROTL32(val[(i + 1) % 9], 1);
    for(int j = 0; j < 9; j += 3) {
      switch (val[(j + i) % 9] & 3) {
        case 0:
          val[(j + i) % 9] += F(t, ROTL32(val[(j + i + 1) % 9], val[(j + i) % 9] >> 2 & 7), ROTL32(val[(j + i + 1) % 9]^vval[0], val[(j + i) % 9] >> 5));
          break;
        case 1:
          val[(j + i) % 9] += G(t, ROTL32(val[(j + i + 1) % 9], val[(j + i) % 9] >> 2 & 7), ROTL32(val[(j + i + 1) % 9]^vval[1], val[(j + i) % 9] >> 5));
          break;
        case 2:
          val[(j + i) % 9] += H(t, ROTL32(val[(j + i + 1) % 9], val[(j + i) % 9] >> 2 & 7), ROTL32(val[(j + i + 1) % 9]^vval[2], val[(j + i) % 9] >> 5));
          break;
        case 3:
          val[(j + i) % 9] += I(t, ROTL32(val[(j + i + 1) % 9], val[(j + i) % 9] >> 2 & 7), ROTL32(val[(j + i + 1) % 9]^vval[3], val[(j + i) % 9] >> 5));
          break;
      }
    }
  }

  int* newval = (int*)(void*)buf;
  for (int i = 0; i < 9; i++) {
    newval[(i+0)%4] += F(val[i % 9], val[(i + 2) % 9], val[(i + 5) % 9]);
    newval[(i+1)%4] ^= ROTL32(G(val[i % 9], val[(i + 8) % 9], val[(i + 3) % 9]), 7);
    newval[(i+2)%4] += ROTL32(H(val[i % 9], val[(i + 1) % 9], val[(i + 6) % 9]), 13);
    newval[(i+3)%4] ^= ROTL32(I(val[i % 9], val[(i + 4) % 9], val[(i + 7) % 9]), 23);
  }
}
