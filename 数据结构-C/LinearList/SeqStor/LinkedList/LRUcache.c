#include <stdio.h>

int main()
{

    system("pause");
    return 0;
}

struct nodeC *ini_node(int key,int value)
{
    struct nodeC *node = (struct nodeC*)malloc(sizeof(struct nodeC));

    if(node != NULL){
        node->key = key;
        node->value = value;
        node->next = NULL;
        node->prev = NULL;
    }
    return node;
}

struct LRUcache *ini_cache(int capacity)
{
    struct LRUcache *lru = (struct LRUcache*)malloc(sizeof(struct LRUcache)+capacity*sizeof(int));

    if(lru != NULL){
        lru->head = (struct nodeC*)malloc(sizeof(struct nodeC));
        lru->tail = (struct nodeC*)malloc(sizeof(struct nodeC));
        lru->head->key = lru->tail->key = lru->head->value = lru->tail->value = -1;
    }
};
