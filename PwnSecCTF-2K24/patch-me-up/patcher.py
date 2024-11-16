#!/usr/bin/env python3

from pwn import *

#Arch:       amd64-64-little
#RELRO:      Partial RELRO
#Stack:      Canary found
#NX:         NX enabled
#PIE:        No PIE (0x400000)


exe = ELF("./patchMeUp")

context.binary = exe


def main():

    #0x000000000040182a <+34>:    cmp    DWORD PTR [rbp-0xc],0x1337
    #0x0000000000401831 <+41>:    jne    0x40183d <main+53>

    # replace the JNE with a NOP Sled
    exe.asm(0x0000000000401831, 'nop')
    exe.asm(0x0000000000401832, 'nop')
    
    #0x00000000004017ec <+39>:    call   0x412600 <gets>
    #0x00000000004017f1 <+44>:    nop
   
    # return just after the gets function call
    exe.asm(0x00000000004017f1, 'ret') # replace with RET instruction
    exe.save("./patched")


if __name__ == "__main__":
    main()
