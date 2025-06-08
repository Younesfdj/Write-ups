#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()

    r.sendline(b"test")
    r.sendline(b"5") # random value
    r.sendline(b"5") 
    r.sendline(b"5")

    r.sendline(b"10") # read from constant seed
    r.sendline(b"0")

    r.interactive()


if __name__ == "__main__":
    main()
