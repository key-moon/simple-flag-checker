import subprocess
from tqdm import tqdm
from extract_data import FLAG_LEN

subprocess.run("gcc -shared -o bin/02_hook.so 02_hook.c 2> /dev/null", shell=True)

def check(flag):
  res = subprocess.run("./checker", env={"LD_PRELOAD": "bin/02_hook.so"}, input=flag + "\n", capture_output=True, text=True).stdout
  return res.count("ok")

flag = ""
for i in tqdm(range(FLAG_LEN)):
  for c in range(0x20, 0xff):
    if check(flag + chr(c)) == i + 1:
      flag += chr(c)
      break

print(flag)
