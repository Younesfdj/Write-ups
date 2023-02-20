## Part one 

-Taking a look of the challenge source code we can see that it uses gets() function to get the user input than checks if there is a stack smashing by checking the old values of two varibles if they've changed after the user input or not , we may notice also the part where the program print the flag which is in the win() function.

-With this observation we see that we can execute a buffer overflow attack and ret2win to get the flag

## Part two

-Lets have some infos about this elf binary 
![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)
we can see that this is a 32bits elf so we have a simulation how this is going to be

-Now lets execute this binary and see what we got
![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

-What if we give it now more than 32 charachter !
![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)
hmm that was expected xD

-Now lets pwn this program and get the flag 

## What to do 

- Overflow the char array until we get stack smashing 
- Resetting a and b to bypass the if statement that checks if there's a stack smashing or not 
- We overflow again until we arrive to saved rip and over write it with the win function so that it will return to win rather than returning to main after executing vuln()
- Now we should handle the arguments by overflowing the stack until we arrive to where the arguments are located and we over write them with 0xdeadbeef and 0x1337

## Ressources

You will find here a video more detailed about the [challenge](https://www.youtube.com/watch?v=vO1Uj2v3r7I)

