import lief
import ctypes
from tqdm import tqdm
from extract_data import FLAG_LEN, get_table


bin = lief.parse("./checker")
bin.add_exported_function(bin.get_function_address("update"), "update")
bin[lief.ELF.DynamicEntry.TAG.FLAGS_1].remove(lief.ELF.DynamicEntryFlags.FLAG.PIE)
bin.write("bin/07_checker.so")

HASH_LEN = 32
lib = ctypes.CDLL('bin/07_checker.so')

def update(state: bytes, c: int):
  state_array = ctypes.create_string_buffer(state)
  lib.update(state_array, ctypes.c_char(bytes([c])))
  return bytes(state_array)

table = get_table()

flag = ""
state = b"\x00" * 36
for i in tqdm(range(FLAG_LEN)):
  for c in range(0x20, 0xff):
    next_state = update(state, c)
    if next_state[:16] == table[i]:
      flag += chr(c)
      state = next_state
      break

print(flag)
