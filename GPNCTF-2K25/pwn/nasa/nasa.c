// gcc -Og -g3 -w -fsanitize=address nasa.c -o nasa
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

void win() {
	puts("YOU WIN!!!\n");
	system("/bin/sh");
	exit(0);
}

void provide_help(void *stack_ptr) {
	printf("%p\n", stack_ptr);
	printf("%p\n", &win);
}

int main(void) {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

	long long option;
	provide_help(&option);
	while (1) {
		puts("[1] Write [2] Read [3] Exit");
		if (scanf("%llu", &option) != 1)
			break;
		if (option == 1) {
			puts("8-byte adress and 8-byte data to write please (hex)");
			uintptr_t addr;
			uint64_t val;
			scanf("%lx %lx", &addr, &val);
			*((uint64_t *)addr) = val;
		} else if (option == 2) {
			puts("8-byte adress to read please (hex)");
			uintptr_t addr;
			scanf("%lx", &addr);
			printf("%lx\n", *((uint64_t *)addr));
		} else if (option == 3) {
			puts(":wave:");
			break;
		} else {
			puts("Invalid option");
		}
	}
	return 0;
}
