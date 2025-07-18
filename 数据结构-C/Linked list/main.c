#include <stdio.h>
#include <stdlib.h>

struct node{
    int data;
    struct node* next;
    struct node* back;
};

struct header{
    int amount;
    struct node* top;
};

void test(int*,struct node*);
void insertion(struct header*,int,int);
void findP(struct node*,int);
struct node* createNode(struct node*,struct header*,int);
struct node* traverse(struct node*,int);
struct node* findE(struct node**,int);
struct node* changeE(struct node**,int);
struct node* insertAtK(struct node**,int);
struct node* deleteE(struct node**,int);
void printList(struct header*);
//(*test).pointer is equal to test->pointer.


int main()
{
    struct header* head = (struct header*)malloc(sizeof(struct header));
    (*head).top = NULL;//equal to head->top
    (*head).amount = 0;
    int array[] = {2,5,3,4,7,11,12,0,5,7,6,9,10};
    int total = sizeof(array)/sizeof(array[0]);
    int i;

    for(i = 0;i < total;i++)
    {
        insertion(head,array[i],i);
    }
    printf("%d\n",head->top->data);
    printf("%d\n",head->top->next->data);
    printf("%d\n",head->top->next->next->data);

    printList(head);

//    int x = 1;
//    struct node* ptr = (struct node*)malloc(sizeof(struct node));
//    (*ptr).data = 1;
//    (*ptr).next = NULL;
//    (*ptr).back = NULL;
//    test(&x,ptr);
//    printf("ptr.data:%d\n",(*ptr).data);
//    printf("x's memory address: %d\n",&x);

    return 0;
}

void test(int* xn,struct node* nd)
{
    (*nd).data = 2;
    struct node* copy = (struct node*)malloc(sizeof(struct node));
    (*copy).data = 3;
    (*copy).back = NULL;
    (*copy).next = NULL;
    *nd = *copy;
    printf("%d %d\n",nd,copy);
    //*xn+=1;
//    int* copy = xn;
//    *xn+=1;
//    *copy+=1;
//    printf("x's memory address: %d\n",xn);
//    printf("copy's memory address: %d\n",&(*copy));
}
/*
Accepts a list node and a value. Find where is the last of the list, and create a new node connect to last node.
If list node is empty, create a new node using this node.
*/
void insertion(struct header* list,int value,int position)
{
    struct node* newP = (*list).top;

    if(newP != NULL){
        findP(newP,position);
        printf("newP->data: %d\n",(*newP).data);

        if((*newP).next != NULL){
            printf("N:%d\n",1);
            struct node* tmp = (struct node*)malloc(sizeof(struct node));
            (*tmp).data = value;
            (*tmp).back = NULL;
            (*tmp).next = (*newP).next;
            (*newP).next = tmp;
        }else{
            printf("Y:%d\n",2);
            (*newP).next = (struct node*)malloc(sizeof(struct node));
            (*(*newP).next).data = value;
            (*(*newP).next).next = NULL;
            (*(*newP).next).back = NULL;
        }
    }else{
        printf("H:%d\n",3);
        (*list).top = (struct node*)malloc(sizeof(struct node));
            (*(*list).top).data = value;
            (*(*list).top).next = NULL;
            (*(*list).top).back = NULL;
    }
    (*list).amount+=1;
}

void findP(struct node* pList,int fPos)
{
    while((*pList).next != NULL && fPos > 1){
        printf("%d\n",97);
        *pList = *((*pList).next);
        fPos-=1;
    }
}

struct node* findE(struct node** fList,int target)
{
    while(*fList != NULL && (*fList)->data != target){
        *fList = (*fList)->next;
    }

    return *fList;
}

struct node* traverse(struct node* start,int stopP)
{
    while((*start).next != NULL && stopP > 0){
        printf("%d\n",12);
        start = (*start).next;
        stopP--;
    }
    printf("traverse: %d\n",(*start).data);

    return start;
}

void printList(struct header* pList)
{
    struct node* copy = (pList->top);
    printf("List has %d node\n",pList->amount);
    while(copy != NULL)
    {
        printf("Node: %d\n",copy->data);
        copy = copy->next;
    }
}



struct node* deleteE(struct node** dList,int aim)
{

}
