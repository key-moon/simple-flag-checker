#include<stdio.h>
#include<string.h>
#include<stdint.h>

#include "hash.h"

#define FLAG_LEN 0x60

int main() {
  uint8_t hash[HASH_LEN] = {0};

  char input[0x100];
  scanf("%s", input);

  int correct = 1;
  for (int i = 0; i < strlen(input); i++) {
    update((char*)hash, input[i]);
    for (int j = 0; j < 16; j++) {
      printf("%d,", hash[j]);
    }
  }
  printf("\n");
}
