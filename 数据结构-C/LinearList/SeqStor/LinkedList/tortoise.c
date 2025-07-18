#include <stdio.h>
#include <stdlib.h>
#include "tortoise.h"
#include "LinkedList.h"

//int main()
//{
//    struct nodeS *test;
//    int array[] = {1,6,4,3,8,2,5,1,5,4,6,13,50};
//    int size;
//    size = sizeof(array)/sizeof(array[0]);
//    test = NULL;
//    test = create_circular_list(test,array,size);
//
//    printf("The length of loop is %d\n",detect_cycle(test));
//    system("pause");
//
//    return 0;
//}

/*
Apply Tortoise and Hare Algorithm, tort moves one node per iteration, while hare moves two.
As hare reach the end, tort will be in the middle
*/
struct nodeS *find_middle(struct nodeS *root)
{
    struct nodeS *tort,*hare;
    tort = hare = root;

    while(hare!=NULL && hare->next!=NULL){
        tort = tort->next;
        hare = hare->next->next;
    }

    return tort;
}

int count_cycle(struct nodeS *node)
{
    struct nodeS *tmp = node;
    int count = 1;
    while(tmp->next != node){
        count++;
        tmp = tmp->next;
    }
    return count;
}

int detect_cycle(struct nodeS *root)
{
    int flag = 0;
    struct nodeS *slow,*fast;
    slow = fast = root;

    while(fast != NULL&&fast->next != NULL&&flag == 0){
        slow = slow->next;
        fast = fast->next->next;
        if(slow == fast){
            return count_cycle(slow);
        }
    }

    return flag;
}




