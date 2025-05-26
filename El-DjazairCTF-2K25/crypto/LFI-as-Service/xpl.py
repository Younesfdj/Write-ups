#!/usr/bin/env python3

from pwn import *
import base64
import hashlib
import argparse
from ecdsa import NIST256p, SigningKey
from ecdsa.util import sigdecode_der, sigencode_der

#context.binary = exe 

context.log_level = 'info'

def conn():
    if args.LOCAL:
        #r = process([exe.path])
        gdb.attach(r)
    else:
        r = remote("vm1.ctfeldjazair.dz", 12397, ssl=True)

    return r

def get_past_signature(m1, sig1, m2, sig2, target):

    # Decode Base64 signatures to DER bytes
    sig1_der = base64.b64decode(sig1)
    sig2_der = base64.b64decode(sig2)

    # Parse DER to get (r, s) for each signature
    r1, s1 = sigdecode_der(sig1_der, NIST256p.order)
    r2, s2 = sigdecode_der(sig2_der, NIST256p.order)

    if r1 != r2:
        raise ValueError("Nonce not reused: r values differ")

    # Compute message hashes as integers
    h1 = int.from_bytes(hashlib.sha256(args.m1.encode()).digest(), 'big')
    h2 = int.from_bytes(hashlib.sha256(args.m2.encode()).digest(), 'big')
    n = NIST256p.order

    # Calculate nonce k
    s_diff = (s1 - s2) % n
    if s_diff == 0:
        raise ValueError("s1 and s2 difference is 0 modulo n")
    h_diff = (h1 - h2) % n
    k = (h_diff * pow(s_diff, -1, n)) % n

    # Recover private key d
    r = r1
    numerator = (s1 * k - h1) % n
    d = (numerator * pow(r, -1, n)) % n

    # Sign target message using the recovered private key
    sk = SigningKey.from_secret_exponent(d, curve=NIST256p, hashfunc=hashlib.sha256)
    target_sig_der = sk.sign(args.target.encode(), sigencode=sigencode_der)
    target_sig_b64 = base64.b64encode(target_sig_der).decode()

    return target_sig_b64


def main():
    r = conn()
   
    r.sendline(b"sign /app/tmp/file1")
    sig1 = r.recvline()
    r.sendline(b"sign /app/tmp/file2")
    sig2 = r.recvline()

    target_sig = get_past_signature(
        "/app/tmp/file1",
        sig1,
        "/app/tmp/file2",
        sig2,
        "/flag.txt"
    )


    r.sendline(f"access {target_sig}".encode())

    r.interactive()
    r.close()


if __name__ == "__main__":
    main()
