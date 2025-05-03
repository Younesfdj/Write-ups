import random
import time
from Crypto.Util.number import isPrime
from Crypto.Util.number import bytes_to_long, long_to_bytes

def generate_prime(bits, seed):
    random.seed(seed)
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1  
        if isPrime(num):
            return num

def generate_rsa_params(seed):
    p = generate_prime(512, seed)
    q = generate_prime(512, seed + 1)
    n = p * q
    e = 65537
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return (n, e), (d, p, q),phi,d




# Create RSA key
def rsa_encrypt(message, public_key):
    n,e= public_key
    m = bytes_to_long(message)
    return pow(m, e, n)



def main():
    
    timestamp = int(time.time())
    print(timestamp)
    pub, priv,phi,d = generate_rsa_params(timestamp)
    with open("flag.txt", "rb") as f:
        flag = f.read()
    print(f"Flag: {flag}")
    encrypted = rsa_encrypt(flag,pub)
    print(f"Encrypted: {encrypted}")
    with open("flag.enc", "w") as f:
        f.write(str(encrypted))

main()