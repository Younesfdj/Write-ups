#!/usr/bin/env python3

from pwn import *

exe = ELF("./gradeViewer")

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

    r.sendline(b"-62482")
    r.sendline(b"f1shc0de"
            

    r.interactive()


if __name__ == "__main__":
    main()
