from more_itertools import chunked
from pwn import ELF

FLAG_LEN = 49
DIGEST_LEN = 16

def get_table():
  elf = ELF("./checker")
  res = elf.read(elf.symbols["table"], FLAG_LEN * DIGEST_LEN)
  return list(map(bytes, chunked(res, DIGEST_LEN)))
