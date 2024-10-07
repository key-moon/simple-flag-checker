import subprocess
from tqdm import tqdm
from extract_data import FLAG_LEN

def check(flag):
  res = subprocess.run("ltrace -e memcmp ./checker", shell=True, input=flag + "\n", capture_output=True, text=True).stderr
  iter = 0
  for line in res.splitlines():
    if "memcmp" not in line: continue
    _, retval = line.split("=")
    if retval.strip() == "0": iter += 1
  return iter

flag = ""
for i in tqdm(range(FLAG_LEN)):
  for c in range(0x20, 0xff):
    if check(flag + chr(c)) == i + 1:
      flag += chr(c)
      break

print(flag)
