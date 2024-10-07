import subprocess
from tqdm import tqdm
from extract_data import FLAG_LEN, get_table

res = open("checker", "rb").read()
open("bin/03_checker_puts", "wb").write(res.replace(b'memcmp', b'puts\x00\x00'))
subprocess.run("chmod +x bin/03_checker_puts", shell=True)

table = get_table()

def check(flag: bytes):
  output = subprocess.run("bin/03_checker_puts", input=flag+b'\n', capture_output=True).stdout
  expected_hash = table[len(flag) - 1].split(b'\x00')[0]
  return expected_hash in output

t = tqdm(total=FLAG_LEN)
def solve(flag):
  print(flag)
  if len(flag) == FLAG_LEN:
    return flag
  for c in range(0x20, 0xff):
    next_flag = flag+bytes([c])
    if check(next_flag):
      res = solve(next_flag)
      if res is not None: return res
  return None

print(solve(b''))
