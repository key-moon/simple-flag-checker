import gdb
from tqdm import tqdm

FLAG_LEN = 49

gdb.execute("file ./checker")

gdb.execute("start")
gdb.execute("b *main+175")
gdb.execute("det")

def check(flag):
  open("input.txt", "w").write(flag)
  gdb.execute("r < input.txt")

  res = 0
  for i in range(FLAG_LEN):
    rax = gdb.parse_and_eval("$rax")
    if rax == 0: res += 1
    gdb.execute("continue")

  return res

flag = ""
for i in tqdm(range(FLAG_LEN)):
  for c in range(0x20, 0xff):
    if check(flag + chr(c)) == i + 1:
      flag += chr(c)
      break

print(flag)
