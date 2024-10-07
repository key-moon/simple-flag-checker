#include<stdio.h>
#include<string.h>

#include "hash.h"

#ifndef FLAG_DATA
#define FLAG_DATA 1
#endif
#ifndef FLAG_LEN
#define FLAG_LEN 1
#endif

char table[FLAG_LEN][16] = { FLAG_DATA };

int __attribute__((optimize("O1"))) main() {
  char buf[FLAG_LEN + 1];
  printf("flag? ");
  fgets(buf, FLAG_LEN + 1, stdin);

  char hash[HASH_LEN] = {0};

  int correct = 1;
  for (int i = 0; i < FLAG_LEN; i++) {
    update(hash, buf[i]);
    correct &= memcmp(hash, table[i], 16) == 0;
  }

  if (correct) {
    printf("Correct! Your flag is: %s\n", buf);
    return 0;
  }
  else {
    puts("Wrong...");
    return 1;
  }
}
