#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MALLOC_SIZE 0x100

typedef struct {
    unsigned char point[8];
}pointer;

void ShowStack() {
    int numa = 3;
    int numb = 4;
    
    printf("FunctinthowStack() stack layout\n");
    printf("----------high address----------\n");
    printf("ret addr\t\t0x%x%x \t%p\n",*(long int *)((char *)&numa+0x10),*(long int *)((char *)&numa+0xc),&numa+0x10);
    printf("push addr \t\t0x%x%x \t\t%p\n",*(long int *)((char *)&numa+0x8),*(long int *)((char *)&numa+0x4),&numa+0x8);

    //如果编译选项中不加-fno-stack-protector,则会出现额外的防溢出机制
    printf("numa \t\t\t%d \t\t\t%p\n",numa,&numa);
    printf("numb \t\t\t%d \t\t\t%p\n",numa,&numb);
    printf("----------low address----------\n");
}

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

void ShowHeap() {
    char * heapa;
    char * heapb;
    char * heapc;
    int i;
    printf("\n====================================\naccess to heap test\n");
    printf("Top of heap is %p",sbrk(0));
    while(1) {

        printf("\n====================================\ntap to malloc all\n");
        getchar();

        heapa = (char *)malloc(MALLOC_SIZE);
        heapb = (char *)malloc(MALLOC_SIZE);
        heapc = (char *)malloc(MALLOC_SIZE);
        
        printf("heap a is at :%p\n",heapa);
        printf("heap b is at :%p\n",heapb);
        printf("heap c is at :%p\n",heapc);
        PrintMap(heapb-0xd0,heapb+0xd0);

        printf("\n====================================\ntap to free\n");
        getchar();

        printf("\nfree heap a\n");
        free(heapa);
        PrintMap(heapb-0xd0,heapb+0xd0);
        printf("\nfree heap b\n");
        free(heapb);
        PrintMap(heapb-0xd0,heapb+0xd0);
        printf("\nfree heap c\n");
        free(heapc);
        PrintMap(heapb-0xd0,heapb+0xd0);

        printf("\n====================================\ntap to malloc heap b\n");
        getchar();

        heapb = (char *)malloc(MALLOC_SIZE);
        printf("heap b is at :%p\n",heapb);
        PrintMap(heapb-0xd0,heapb+0xd0);

    }
}

void ShowLargeHeap(){
    void * heapa;
    void * heapb;
    void * heapc;
    heapa = malloc(MALLOC_SIZE);
    heapb = malloc(MALLOC_SIZE);
    heapc = malloc(MALLOC_SIZE);
    printf("heap a is at :%p\n",heapa);
    printf("heap b is at :%p\n",heapb);
    printf("heap c is at :%p\n",heapc);
    PrintMap(heapa-0x20,heapa+0x20);
    PrintMap(heapb-0x20,heapb+0x20);
    PrintMap(heapc-0x20,heapc+0x20);
    PrintMap(heapc+MALLOC_SIZE,heapc+MALLOC_SIZE+0x20);
    printf("\n====================================\nfree heap a\n");
    free(heapa);
    PrintMap(heapa-0x20,heapa+0x20);
    PrintMap(heapa+MALLOC_SIZE-0x20,heapa+MALLOC_SIZE+0x20);
    printf("\n====================================\nfree heap b\n");
    free(heapb);
    PrintMap(heapb-0x20,heapb+0x20);
    PrintMap(heapb+MALLOC_SIZE-0x20,heapb+MALLOC_SIZE+0x20);
    printf("\n====================================\nfree heap c\n");
    free(heapc);
    PrintMap(heapc-0x20,heapc+0x20);
    PrintMap(heapc+MALLOC_SIZE-0x20,heapc+MALLOC_SIZE+0x20);
    printf("\n====================================\nall\n");
    PrintMap(heapa-0x20,heapa+0x20);
    PrintMap(heapc+MALLOC_SIZE-0x20,heapc+MALLOC_SIZE+0x20);
}

void ShowArena() {
    void * topchunk = sbrk(0);
    void * heaphead = topchunk - 0x21000;
    void * chunk = heaphead;
    int length;
    PrintMap(heaphead,heaphead+0x100);
    for(;;) {
        length = *((int *)chunk+2) - 1;
        printf("\nchunk length = %d");
        if (length<0x500) {
            PrintMap(chunk,chunk+length);
        }
        else {
            printf("too long,skip");
        }
        chunk = chunk + length;
        printf("\n");
        getchar();
    }
}

void ShowBrk() {
    void * topchunk = sbrk(0);
    //可以通过sbrk()函数分配当前堆的边界
    printf("%p",topchunk);
    // PrintMap(topchunk,topchunk+0x10)
    // 以上代码报错,说明超过topchhunk的内存没有映射到物理内存
    PrintMap(topchunk-0x100,topchunk);
    printf("\n");
}

int main(){
    int pid;
    pid = getpid();
    printf("Process pid = %d\n",pid);
    // getchar();
    // getchar();
    // printf("Function main() is at %p\n",&main);
    // ShowStack();
    // ShowBrk();
    // ShowArena();
    // ShowHeap();
    ShowLargeHeap();
}