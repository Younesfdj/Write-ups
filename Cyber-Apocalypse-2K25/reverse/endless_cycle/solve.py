#! /usr/bin/env python3

def reverse_xor(encrypted_data):
    key = 0xbeefcafe  # XOR key from gdb
    decrypted = bytearray()
    
    for i in range(0, len(encrypted_data), 4):
        chunk = encrypted_data[i:i+4]
        if len(chunk) < 4:
            decrypted.extend(chunk)
            break
        
        # process 4-byte chunk
        chunk_int = int.from_bytes(chunk, byteorder='little')
        decrypted_int = chunk_int ^ key
        decrypted_chunk = decrypted_int.to_bytes(4, byteorder='little')
        decrypted.extend(decrypted_chunk)
    
    return bytes(decrypted)
    
def construct_flag(*parts):
    flag = ""
    for part in parts :
        flag += part.decode()
        
    return flag
    
# flag parts xored read from memory using gdb
part1 = reverse_xor(b'\xb6\x9e\xad\xc5\x92\xfa\xdf\xd5')
part2 = reverse_xor(b'\xa1\xa8\xdc\xc7\xce\xa4\x8b\xe1')
part3 = reverse_xor(b'\x8a\xa2\xdc\xe1\x89\xfa\x9d\xd2')
part4 = reverse_xor(b'\x9a\xb7\xca\xfe')

flag = construct_flag(part1, part2, part3, part4)
print(flag) 
