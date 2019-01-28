#include <stdio.h>
#include <stdlib.h>

#define BLACK 1
#define WHITE 0

unsigned char ** chess_map;
int N,M;

int gen_map() {
    int i,j;
    char * buff;

    if (feof(stdin))
        return 0;
    scanf("%d%d",&N,&M);
    chess_map = (unsigned char **) malloc (N * sizeof(void *));
    for (i = 0; i<N; i++) 
        chess_map[i] = (unsigned char *)malloc(M);
    buff = (unsigned char *)malloc(N + 1);

    for(i = 0;i < N; i++) {
        scanf("%s",buff);
        for(j = 0; j < M; j++) {
            if (buff[j] == 'b') 
                chess_map[i][j] = BLACK;
            else 
                chess_map[i][j] = WHITE;
        }
    }
    free(buff);
    return 1;
}

int inner_count(int i, int j) {
    int limit = M;
    int count = 0;

    for (; i<N; i++) {
        for (; j<limit; j++){
            if (chess_map[i][j] == WHITE)
                count++;
            else
                break;
        }
        limit = j;
    }

    return count;
}

int travers() {
    int i,j;
    int count = 0;

    for(i = 0; i<N; i++) {
        for(j = 0; j<M; j++) {
            count += inner_count(i,j);
        }
    }

    return count;
}

int main() {
    int i;
    
    while (gen_map()){
        printf("%d\n",travers());
        for(i = 0;i<M;i++){
            free(chess_map[i]);
        }
        free(chess_map);
    }
    return 0;
}