#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    unsigned char point[8];
}pointer;

void ShowStack() {
    int numa = 3;
    int numb = 4;
    // long long int pushed_rbp = *(long long int *)(&numa-0x2);
    // long long int ret = *(long long int *)(&numa-0x4);
    // printf("ret addr = %x\n",*(unsigned char *)(&numa-0x20));
    printf("Function ShowStack() stack layout\n");
    printf("----------high address----------\n");
    printf("ret addr \t\t0x%x%x \t\t%p\n",*(long int *)((char *)&numa+0x10),*(long int *)((char *)&numa+0xc),&numa+0x10);
    printf("pushed rbp \t\t0x%x%x \t\t%p\n",*(long int *)((char *)&numa+0x8),*(long int *)((char *)&numa+0x4),&numa+0x8);

    // printf("pushed rbp = 0x");
    // for(numa = 0;numa < 8;numa++) {
    //     // if(*(unsigned char*)(&numa-numa) == 0) {
    //     //     printf("00");
    //     // }
    //     // else {
    //         printf("%p",*(unsigned char*)(&numa-numa));
    //     // }
    // }
    // printf("\n");

    //如果编译选项中不加-fno-stack-protector,则会出现额外的防溢出机制
    printf("numa \t\t\t%d \t\t\t%p\n",numa,&numa);
    printf("numb \t\t\t%d \t\t\t%p\n",numa,&numb);
    printf("----------low address----------\n");
}

// void * GetAddr(void * addr) {
//     char result[8];
//     int i;
//     for(i=0;i<8;i++){
//         result[8-i] = *(char *)(addr+i);
//     }
//     return (*result);
// }

void ShowHeap() {
    char * heapa;
    char * heapb;
    int i;

    heapa = (char *)malloc(1);
    heapb = (char *)malloc(0x10);

    *heapa = 0x1;
    for(i =0; i<0x10;i++) {
        *(heapb+ i) = i;
    }

    free(heapa);
    free(heapb);
}

int main(){
    printf("Function main() is at %p\n\n",&main);
    ShowStack();
    ShowHeap();
}