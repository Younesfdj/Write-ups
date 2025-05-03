import random
from Crypto.Util.number import long_to_bytes, isPrime

def generate_prime(bits, seed):
    random.seed(seed)
    while True:
        num = random.getrandbits(bits)
        num |= (1 << (bits - 1)) | 1
        if isPrime(num):
            return num

base_timestamp = 1735926987  # timestamp of the created pgp 
flag = 74853691332836114322800517229156499048613454535610386971003097205742759876251090140905263359090728981373776584178902054210201249669100212238690032243086280755581059101008578139594809312713240761528256204631623830071930938346030753506265690147693386767699310604314708081927261896385917037161023323539415124969

for delta in range(-40, 40):
    timestamp = base_timestamp + delta
    try:
        p = generate_prime(512, timestamp)
        q = generate_prime(512, timestamp + 1)
        n = p * q
        e = 65537
        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)
        m = pow(flag, d, n)
        decrypted = long_to_bytes(m)
        if b'nexus{' in decrypted:
            print(f"Flag: {decrypted.decode()}")
            break
    except:
        continue