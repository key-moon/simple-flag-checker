#include <stdio.h>
int main() {
  int val=0;
  scanf("%d", &val);
  if (val * 0xdeadbeef == 0xcafebabe) {
    puts("Correct!");
  }
}
