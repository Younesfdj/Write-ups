#include <stdio.h> 
#include <stdlib.h> 
#include <string.h>

void bf(char *src, int len){

        char buf[64];
	memset(buf, 0, 64);
        int closed, opened, pos = 0;
        char *pc;

	for (pc = buf; pos < len; pos++) {
		switch (src[pos]) {
		case '>':
			pc++;
			break;
		case '<':
			pc--;
			break;
		case '+':
			(*pc)++;
			break;
		case '-':
			(*pc)--;
			break;
		case '.':
			putchar(*pc);
			break;
		case ',':
			*pc = getchar();
			break;
		case '[':
			if (!(*pc)) {
				for (opened = 0, pos++; pos < len; pos++) {
					if (src[pos] == ']' && !opened)
						break;
					else if (src[pos] == '[')
						opened++;
					else if (src[pos] == ']')
						opened--;
				}
			}
			break;
		case ']':
			if (*pc) {
				for (closed = 0, pos--; pos >= 0; pos--) {
					if (src[pos] == '[' && !closed)
						break;
					else if (src[pos] == ']')
						closed++;
					else if (src[pos] == '[')
						closed--;
				}
			}
			break;
		}
	}

        return;
}

int main(){
    setvbuf(stdin, NULL, _IONBF, 1);
    setvbuf(stdout, NULL, _IONBF, 1);
    setvbuf(stderr, NULL, _IONBF, 1);

    char *code = malloc(4096);
    int len;

    while(1){
        printf("Enter your source code (q to quit):\n>");
        fgets(code, 4095, stdin);
	len = strlen(code);
	if (code[0] == 'q'){
            break;
	}
        bf(code, len);
    }
    
    return 0; 
}
