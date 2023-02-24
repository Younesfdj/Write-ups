## Part one 

-Taking a look of the challenge elf file
```
└─$ file chall
chall: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=9287e3a80b10eb0d8c384f5a2e352833abf64b49, for GNU/Linux 3.2.0, not stripped
```
so we're working with 32 bits elf , hmm noicee
-Lets open it with ghidra now

## Part two

-As the pic shows there is nothing in the main() function
![App Screenshot](https://github.com/Younesfdj/Write-ups/tree/main/Hack.INI-2K23/Pwn/Ret2libc/screens/main.png)
lets check the vuln() function

-The vuln() function is get a string of 36 chars from the user using the gets() function
![App Screenshot](https://github.com/Younesfdj/Write-ups/tree/main/Hack.INI-2K23/Pwn/Ret2libc/screens/vuln.png)
Since the program is using gets we could control the instruction pointer to point wherever we want but!,
there's no a win function to print our flag also we cant inject arbitary code to get access to the machine since the stack is non-executable as the checksec shows
```
└─$ checksec chall  
[*] '/home/sams/Desktop/hack.ini2k23/pwn/ret2libc/chall'
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
-As the name of the challenge we could think of using the technique of ret2libc to get the full access to the machine, the idea is to overwrite the eip to return to a libc function which is gonna be system() function in our case after, that we set its parameter which gonna be '/bin/sh' to get a shell 

## What to do 

- Get the offset of system() function using the giving libc
```
└─$ gdb libc.so.6
```
then
```
(gdb) x system
```
- Get the offset of "/bin/sh" string
```
strings -a -t x libc.so.6 | grep "/bin/sh"
```
- After that we use the address of printf to get the address of system() and "/bin/sh" in libc
```
└─$ ./chall             
Some help: 0xf7c57a70    <-- printf() address
Enter data:
```
then we do some math

@system() = @printf - OFFSET printf + OFFSET system 

@/bin/sh = @printf - OFFSET printf + OFFSET "/bin/sh"

- We need alse to find the perfect padding to overwrite the saved eip which gonna be 44 bytes in our case 

## Ressources
More detailed video about the challenge [here](https://www.youtube.com/watch?v=m17mV24TgwY)

The solution for the challenge [here](https://github.com/Younesfdj/Write-ups/blob/main/Hack.INI-2K23/Pwn/Ret2libc/exploit.py) 
