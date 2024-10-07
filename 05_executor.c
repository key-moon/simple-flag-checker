#include<stdio.h>
int main(){
  char update[] = { FUNC };
  char buf[36];
  read(0, buf, 36);
  char c;
  read(0, &c, 1);
  ((void(*)(char*, char))update)(buf, c);
  write(1, buf, 36);
}
