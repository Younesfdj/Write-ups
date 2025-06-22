#include <stdio.h>
#include <unistd.h>


char *fgets(char* s, int size, FILE *restrict stream) {
    char* cursor = s;
    for (int i = 0; i < size -1; i++) {
        int c = getc(stream);
        if (c == EOF) break;
        *(cursor++) = c;
        if (c == '\n') break;
    }
    // *cursor = '\0'; // our note is always null terminated
    return s;
}

void win() {
    execve("/bin/sh", NULL, NULL);
}
