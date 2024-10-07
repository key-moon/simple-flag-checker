#include <stdio.h>
int memcmp(char* buf1, char* buf2, int len) {
  for (int i = 0; i < len; i++) {
    if (buf1[i] < buf2[i]) return -1;
    if (buf1[i] > buf2[i]) return 1;
  }
  puts("ok");
  return 0;
}
