#! /usr/bin/env python3

target_string = "ucaqbvl,n*d\\\'R#!!l"

def find_input():
    input_chars = []
    
    for i in range(len(target_string)):
        correct_char = chr(ord(target_string[i]) + i)
        input_chars.append(correct_char)
    
    return ''.join(input_chars)

correct_input = find_input()
print(f"input is: {correct_input}")
