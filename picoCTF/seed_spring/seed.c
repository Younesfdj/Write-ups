#include<stdio.h>
#include<stdlib.h>
#include<time.h>
int main(){
	srand(time(NULL));
	for(int i=0;i<30;i++){
		printf("%d ",rand() & 0xf);
	}
	return 0;
}
