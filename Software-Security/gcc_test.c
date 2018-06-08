#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int i;
int i = 0x1000;

void PrintHex(unsigned char * start, int len) {
    int i;
    printf("\n%p || ",start);
    for(i=0;i<len;i++){
        if((int)*(start+i) < 16) {
            printf("0%x",(unsigned int)*(start+i));
        }
        else {
            printf("%x",(unsigned int)*(start+i));
        }
        if(!((i+1)%4)) {
            printf(" ");
        }
    }
}

void PrintMap(char * start, char * end) {
    //返回一段内存dump
    int i;
    printf("\ncurrent dump from %p to %p :\n",start,end);
    for(i=0;i<(end-start); ) {
        if (end-start-i>=16) {
            PrintHex(start+i,16);
        }
        else {
            PrintHex(start+i,end-i-start);
        }
        i += 16;
    }
}

void stack_protect() {
    int i;
    unsigned char buff[16];

    printf("int i at %p\n",&i);
    printf("char * buff at %p\n",buff);
    PrintMap(buff-0x10,buff+0x30);
    for(i=0;i<16;i++) {
        buff[i] = (char)(16-i);
    }
    buff[16] = 'A';
    PrintMap(buff-0x10,buff+0x30);
}

void aslr_pie(){

}

int main(){
    stack_protect();
}