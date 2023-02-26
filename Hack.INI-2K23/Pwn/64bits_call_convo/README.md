## Part one 

-Taking a look of the challenge source code we can see that it uses the gets() function to get the user input then it checks if there is a stack smashing by checking the old values of two varibles if they've changed after the user input or not, we may notice also the part where the program prints the flag which is in the win() function.

-With this we can see that if we execute a buffer overflow attack and ret2win we can get the flag

## Part two

-Lets have some infos about this elf binary 
``` 
└─$ file chall
chall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=db9abcaff5baddee93c28d193df776e58d66ba70, not stripped
```
we can see that this is a 64bits elf , things are not going to be like the 32bits arch

-Now lets execute this binary and see what we get
```
└─$ ./chall
Enter data: hellllo world!
You entered: hellllo world!
``` 
-What if we input more than 32 byte  !
```
└─$ ./chall  
Enter data: aaaabaaacaaadaaaeaaafaaagaaahaaaia
Stack Smashing detected
The program will automatically exit
```
hmm that was expected xD

-Before proceeding to pwn this program there's something important to be discussed, the steps of pwning this program gonna be the same as the 32bits arch except that the registers we are going to overwrite are 64bits sized so we use struct.pack("Q",....) instead of "I" to represent the data as 64bits long

One other thing that is interesting is the arguments in 64bits arch are passed in the RDI and RSI registers, so we need an instruction to set the RDI to 0xdeadbeef and RSI to 0x1337, this can be done using a gadget 

-Lets find the good gadgets using the commands below 
```
└─$ ropper --file chall --search "pop rsi"
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: pop rsi

[INFO] File: chall
0x0000000000400931: pop rsi; pop r15; ret;
```
And 
```
└─$ ropper --file chall --search "pop rdi"
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: pop rdi

[INFO] File: chall
0x0000000000400933: pop rdi; ret; 
```
## What to do

- Overflow the char array until we get a stack smashing 
- Resetting a and b to bypass the if condition that checks if there's a stack smashing or not 
- We overflow again until we find the offset of the saved rip and overwrite it with the rdi gadget then the value we want to set the rdi to, then the rsi gadget and its value, then with the win function's address so that it will return to win() rather than returning to main() after executing vuln()
- One important thing to focus on is the pop rsi gadget, we need to set a value to r15 register as well as the rsi, so we pass the wanted value to rsi and a junk for r15

## Ressources

More detailed video about the challenge [here](https://www.youtube.com/watch?v=vO1Uj2v3r7I)

The solution for the challenge [here](https://github.com/Younesfdj/Write-ups/blob/main/Hack.INI-2K23/Pwn/64bits_call_convo/exploit.py)
