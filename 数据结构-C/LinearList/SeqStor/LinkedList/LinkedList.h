#ifndef LinkedList_h
#define LinkedList_h
struct nodeS{//For Singly linked list 单向链表
    int data;
    struct nodeS* next;
};

struct nodeD{//For Doubly linked list 双向链表
    int data;
    struct nodeD* next;
    struct nodeD* before;
};

struct nodeS *createList(struct nodeS *,int[],int);
void traverse(struct nodeS *);
struct nodeS *changeElement(struct nodeS *,int,int);
struct nodeS *insertAtK(struct nodeS *,int,int);
struct nodeS *deleteK(struct nodeS *,int);

struct nodeD *createListRe(struct nodeD *,int[],int);
void traverseD(struct nodeD *);
struct nodeD *changeElementRe(struct nodeD *,int,int);
struct nodeD *insertAtKRe(struct nodeD *,int,int);
struct nodeD *deleteKRe(struct nodeD *,int);

struct nodeD *swapAdjacent(struct nodeD *,int);
struct nodeD *swapNonAdj(struct nodeD *,struct nodeD *,int,int);

struct nodeS *create_circular_list(struct nodeS *,int[],int);

#endif // LinkedList_h
