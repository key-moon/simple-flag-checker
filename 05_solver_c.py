import subprocess
from pwn import ELF
from tqdm import tqdm
from extract_data import FLAG_LEN, get_table

elf = ELF("./checker")
update = elf.read(elf.symbols["update"], 0x7a9)

subprocess.run(f"gcc -z execstack -DFUNC={','.join(map(str, update))} -o bin/05_executor 05_executor.c 2>/dev/null", shell=True)

def compute(state: bytes, c: int):
  res = subprocess.run("bin/05_executor", input=state + bytes([c]), capture_output=True).stdout
  return res

table = get_table()

flag = ""
state = b"\x00" * 36
for i in tqdm(range(FLAG_LEN)):
  for c in range(0x20, 0xff):
    next_state = compute(state,c)
    if next_state[:16] == table[i]:
      flag += chr(c)
      state = next_state
      break

print(flag)
