## Part one 

-Taking a look of the challenge source code we can see that it uses the gets() function to get the user input then it checks if there is a stack smashing by checking the old values of two varibles if they've changed after the user input or not, we may notice also the part where the program prints the flag which is in the win() function.

-With this we can see that if we execute a buffer overflow attack and ret2win we can get the flag

## Part two

-Lets have some infos about this elf binary 
``` 
└─$ file chall
chall: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=b3563ca5a27565370cc241ea9e18b31339da248d, for GNU/Linux 3.2.0, not stripped
```
we can see that this is a 32bits elf, so we can expect how we can proceed

-Now lets execute this binary and see what we get
```
└─$ ./chall
Enter data: hellllo world!
You entered: hellllo world!
``` 
-What if we input more than 32 byte !
```
└─$ ./chall  
Enter data: aaaabaaacaaadaaaeaaafaaagaaahaaaia
Stack Smashing detected
The program will automatically exit
```
hmm that was expected xD

-Now lets pwn this program and get the flag 

## What to do 

- Overflow the char array until we get stack smashing 
- Resetting a and b to bypass the if condition that checks if there's a stack smashing or not 
- We overflow again until we find the offset of the saved eip and overwrite it with the win() function's address so that it will return to win rather than returning to main() after executing vuln()
- Now we should handle the arguments by overflowing the stack until we find their offset and we overwrite them with 0xdeadbeef and 0x1337

## Ressources

More detailed video about the challenge [here](https://www.youtube.com/watch?v=vO1Uj2v3r7I)

The solution for the challenge [here](https://github.com/Younesfdj/Write-ups/blob/main/Hack.INI-2K23/Pwn/32bits_call_convo/exploit.py)

