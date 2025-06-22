#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>

#define RAW_FLAG "GPNCTF{fake_flag}"

char *FLAG = RAW_FLAG;

int no(char c)
{
    if (c == '.')
        return 1;
    if (c == '/')
        return 1;
    if (c == 'n')
        return 1;
    if (c == 'c')
        return 1;
    return 0;
}

char filebuf[4096] = {};
int main(int argc, char **argv)
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    char buf[200] = {};
    puts("Give me a file to read");
    read(STDIN_FILENO, buf, (sizeof buf) - 1);
    buf[sizeof buf - 1] = '\0';
    size_t str_len = strlen(buf);
    for (size_t i = 0; i < str_len; i++)
    {
        if (no(buf[i]))
        {
            puts("I don't like your character!");
            exit(1);
        }
    }
    char *filename = calloc(200, 1);
    snprintf(filename, (sizeof filename) - 1, buf);
    puts("Will open:");
    puts(filename);
    int fd = open(filename, 0);
    if (fd < 0)
    {
        perror("open");
        exit(1);
    }
    while (1)
    {
        int count = read(fd, filebuf, (sizeof filebuf) - 1);
        if (count > 0)
        {
            write(STDOUT_FILENO, filebuf, count);
        }
        else
        {
            break;
        }
    }
}