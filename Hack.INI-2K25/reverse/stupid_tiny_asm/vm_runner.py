import base64

#  the instructions
_X = 'ZmVrbgprChMdVmZla24KaQobHlZ5f2gKawppVnl+ZXhvCmsKGlZmZWtuCmsKHRhWeX5leG8KawobVmZla24KawocE1Z5fmV4bwprChhWZmVrbgprCh5WZmVrbgpoChsTVmd/ZgpoCmtWeX5leG8KaAoZVnl+ZXhvCmgKHlZmZWtuCmsKGRxWeX5leG8KawofVmZla24KawoZHVZrbm4KawppVnl+ZXhvCmsKHFZmZWtuCmsKExNWeX5leG8KawodVmBkcAppCh8ZVmZla24KawoSH1Z5fmV4bwprChJWZmVrbgprChsbHlZ5fmV4bwprChNWeX5leG8KawobGlZmZWtuCmsKHBNWZmVrbgpoChgaVmZla24KaQobVmZla24KbgobG1ZmZWtuCm8KGxpWZmVrbmdvZwprCmhWa25uCmsKb1Z5fmV4bwprCmhWa25uCmgKaVZ5f2gKbgppVmBkcApuChkbVmZla24KawoaVmZla24KaAocG1ZmZWtuCmkKG1ZmZWtuCm4KGlZmZWtuCm8KG1ZmZWtuCmwKGlZmZWtuZ29nCmwKa1Z5f2gKbApuVmBwCmwKHhNWeX5leG8KbgprVmBnegoeE1ZmZWtuCmwKGlZrbm4KawppVnl/aApoCmlWYGRwCmgKHhlWYGd6Ch0SVmZla24KawocHVZ5fmV4bwprChJWZmVrbgpuChgdVmZla24KaQobVmZla24KaAoYGlZmZWtuZ29nCmsKaFZmZWtuCm8KH1Zrbm4KawpvVmZla24KbwpoVmZla24KbAoYGlZ5f2gKbwpsVmZla24KbQoTVm5jfApvCm1WZ39mCm8KbVZmZWtuCmwKaFZmZWtuCmIKGBpWeX9oCmwKYlZ5f2gKbApvVmZla25nb2cKbQpsVnJleAprCm1WeX5leG8KawpoVmtubgpoCmlWeX9oCm4KaVZgZHAKbgofElZgZ3oKGR1WYmtmfg=='

def decode_ins(encoded, key=42):
    raw = base64.b64decode(encoded)
    txt = ''.join(chr(b ^ key) for b in raw)
    return txt.split('|')

# VM states + write-log
regs   = {r:0 for r in 'ABCDEFGH'}
mem    = {}
stack  = []
writes = []    # log of (address, value) for every STORE

# init mem[0..19] = ord('A')
for addr in range(20):
    mem[addr] = ord('A')

# load the hex blob into mem[20..]
hex_blob = '1b1b1b1b1b444d121f1b2e11771c12670b3221336f030e60120939'
data     = bytes.fromhex(hex_blob)
for i,b in enumerate(data):
    mem[20+i] = b

insns = decode_ins(_X)

# interpreter with STORE
pc, jumped = 0, False

def is_reg(x): return x in regs

while pc < len(insns):
    parts = insns[pc].split()
    op = parts[0]

    if op == 'HALT':
        break

    if op == 'JMP':
        tgt = int(parts[1])
        if 0 <= tgt < len(insns):
            pc, jumped = tgt, True

    elif op == 'PUSH':
        r = parts[1]
        if is_reg(r):
            stack.append(regs[r])

    elif op == 'POP':
        r = parts[1]
        if stack and is_reg(r):
            regs[r] = stack.pop()

    elif op == 'PRINT':
        # no-ops in this program
        pass

    elif op == 'LOAD':
        dst, src = parts[1], parts[2]
        if is_reg(dst):
            regs[dst] = regs[src] if is_reg(src) else int(src)

    elif op == 'STORE':
        src, addr = parts[1], parts[2]
        if is_reg(src):
            loc = regs[addr] if is_reg(addr) else int(addr)
            val = regs[src]
            mem[loc] = val
            writes.append((loc, val))

    elif op == 'LOADMEM':
        dst, addr = parts[1], parts[2]
        if is_reg(dst):
            loc = regs[addr] if is_reg(addr) else int(addr)
            regs[dst] = mem.get(loc, 0)

    elif op in ('ADD','SUB','MUL','DIV','XOR'):
        dst, src = parts[1], parts[2]
        if is_reg(dst) and is_reg(src):
            a,b = regs[dst], regs[src]
            try:
                if   op=='ADD': regs[dst]=a+b
                elif op=='SUB': regs[dst]=a-b
                elif op=='MUL': regs[dst]=a*b
                elif op=='DIV': regs[dst]=a//max(b,1)
                elif op=='XOR': regs[dst]=a^b
            except: pass

    elif op == 'JZ':
        r, tgt = parts[1], int(parts[2])
        if is_reg(r) and regs[r]==0 and 0<=tgt<len(insns):
            pc, jumped = tgt, True

    elif op == 'JNZ':
        r, tgt = parts[1], int(parts[2])
        if is_reg(r) and regs[r]!=0 and 0<=tgt<len(insns):
            pc, jumped = tgt, True

    if not jumped:
        pc += 1
    else:
        jumped = False

flag = ''

for addr, val in writes:
    if 32 <= val < 127:
        flag += ''.join(chr(val))

print(flag)
