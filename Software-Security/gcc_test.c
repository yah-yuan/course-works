#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int g_uninit[30000];
int g_init = 0x1000;

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
    for(i=0;i<8;i++){
        buff[0x18+i] = 'A';
    }
    PrintMap(buff-0x10,buff+0x30);
}

void aslr_pie(){
    int pid = getpid();
    char stack = 'a';
    void * heap_small = malloc(1);
    void * heap_large = malloc(0x100000);
    printf("program pid = %d\n",pid);
    printf("===============================================\n");
    printf("globle var uninitial is at %p, bss segment\n",&g_uninit);
    printf("globle var initialed is at %p, data segment\n",&g_init);
    printf("this function is at %p, program segment\n",&aslr_pie);
    printf("stack var is at %p, stack segment\n",&stack);
    printf("small heap is at %p, heap segment\n",heap_small);
    printf("large heap is at %p, heap segment\n",heap_large);
    getchar();
}

void test_memcpy() {
    char buff[0x10];
    char str[0x10] = "hey there";
    strcpy(buff,str); //20个A,溢出
}

void NX() {
    int pid = getpid();
    printf("program pid = %d\n",pid);
    getchar();
}
void relro(){
    int pid = getpid();
    printf("program pid = %d\n",pid);
    getchar();
}

int main(){
    // stack_protect();
    // aslr_pie();
    // NX();
    // test_memcpy();
    relro();
}