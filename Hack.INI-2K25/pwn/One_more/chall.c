#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#define BUF_SIZE 120
int i ;

void win() {
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        perror("flag.txt");
        exit(1);
    }
    char flag[256];
    if (fgets(flag, sizeof(flag), f) == NULL) {
        printf("Failed to read flag\n");
        fclose(f);
        exit(1);
    }
    fclose(f);
    printf("%s\n", flag);
    exit(0);
}

void vuln(char * str) { 
    char buffer[BUF_SIZE];
    for (i=0;i<=BUF_SIZE;i++){
        buffer[i] = str[i];
    }
}

int main(int argc, char**argv) {
    vuln(argv[1]);
    return 0;
}
