#include <stdio.h>
#include <stdlib.h>
#include "LinkedList.h"
/*
进度：
    2024/9/7    line 237
    2024/9/9    line 79
    2024/9/10   line 546
    2024/9/26   line 550 swapNonAdj 出现无限循环的问题
    2024/9/27   Over
*/

/*Beginner programmer 初学者进度：
  --1.Create a linked list(single/double) of N nodes;如果已知链表长度，应当只调用一次函数，并一次同时分配所有结点的内存
  --2.Traverse a linked list forward/backward;
  --3.Find/Change an element;
  --4.Insert an element start/end/Kth;
  --5.Delete an element start/end/Kth.
*/

/*Advanced:
  --1.All of that using recursion;
  --2.Swap adjacent elements;
    3.Swap non-adjacent elements;
*/

/*Gains so far 收获:
    1.(*example).pointer is equal to example->pointer.
    2.Do not set structure's pointer to NULL then malloc; Instead, use existed parent node's next pointer to malloc.
*/




/*
Accept a root pointer, an integer array containing a list of elements and integer telling how many elements does array have.
While array element exist, allocate a memory to new pointer. If root structure is empty, initialize it; Else, connect new structure after root.
Return root pointer.
*/
struct nodeS *createList(struct nodeS* root,int dataList[],int listSize)
{
    struct nodeS *newP,*tmp;
    int j = 0;

    while(j < listSize){
        newP = (struct nodeS *)malloc(sizeof(struct nodeS));
        if(newP != NULL){
            (*newP).data = dataList[j];
            (*newP).next = NULL;
            j++;
            if(root == NULL){
                root = newP;
                tmp = root;
            }else{
                (*tmp).next = newP;
                tmp = newP;
            }
        }else{
            j = listSize;
            printf("Memory is full");
        }
    }
    return root;
}

struct nodeS *create_circular_list(struct nodeS *root,int data_list[],int list_size)
{
    struct nodeS *newP,*tmp;
    int j = 0;

    while(j < list_size){
        newP = (struct nodeS *)malloc(sizeof(struct nodeS));
        if(newP != NULL){
            (*newP).data = data_list[j];
            (*newP).next = NULL;
            j++;
            if(root == NULL){
                root = newP;
                tmp = root;
            }else{
                (*tmp).next = newP;
                tmp = newP;
            }
        }else{
            j = list_size;
            printf("Memory is full");
        }
    }

    if(j == list_size&&newP != NULL)
        (*tmp).next = root;

    return root;
}

void traverse(struct nodeS* tList)
{
    int j;

    for(j = 0;tList != NULL;j++){
        printf("Node %d: %d\n",j,tList->data);
        tList = tList->next;
    }
}

/*
Accepts a linked list and 2 integers. Find the first target node containing data that will be replaced, and change its data with new data.
If the first node of list contains target data, change its data with new data, otherwise, use a new pointer to find
*/
struct nodeS *changeElement(struct nodeS* cList,int target,int element)
{
    struct nodeS *tmp = cList;

    while(tmp != NULL){
        if((*tmp).data != target){
            tmp = (*tmp).next;
        }else{
            (*tmp).data = element;
            return cList;
        }
    }

    printf("Did not find the target");
    return cList;
}

/*
Accept a root pointer, two integers one represents where to insert and another one represents insert element.
First declare two structure pointer.Using loop to find where to insert new node. After find it, allocate memory to new pointer and connect with list.
Return root pointer.
1-index based.
*/
struct nodeS *insertAtK(struct nodeS * kList, int position, int element)
{
    struct nodeS *kNode = kList, *newP;

    if(position > 1){
        while(position > 2){
            if((*kNode).next != NULL){
                kNode = (*kNode).next;
                position-=1;
            }else{
                printf("Kth is too long for this list");
                return kList;
            }
        }

        newP = (struct nodeS *)malloc(sizeof(struct nodeS));
        if(newP != NULL){
            (*newP).data = element;
            (*newP).next = (*kNode).next;
            (*kNode).next = newP;
        }else
            printf("Memory is full");
    }else if(position == 1){
        newP = (struct nodeS *)malloc(sizeof(struct nodeS));
        (*newP).data = element;
        (*newP).next = kNode;
        kList = newP;
    }else
        printf("K is not a positive integer.\n");

    return kList;
}

/*
Accepts a root pointer and an integer that represents where to delete the node.
Find Kth position inside the list according to the integer, change the pointer and free Kth node.
Return root pointer.
*/
struct nodeS *deleteK(struct nodeS *dList,int dPosition)
{
    struct nodeS *delNode = dList, *tmp;

    if(dPosition < 1){
        printf("K is not a positive integer\n");
        return dList;
    }

    if(dPosition != 1){//For deleting non-root node
        while(dPosition > 1){
            tmp = delNode;
            delNode = (*tmp).next;
            if(delNode != NULL){
                dPosition -= 1;
            }else{
                printf("Kth node is too long for this list to delete");
                return dList;
            }
        }
        (*tmp).next = (*delNode).next;
        free(delNode);
    }else{//For deleting root node
        tmp = (*delNode).next;
        free(delNode);
        dList = tmp;
    }
    return dList;
}

/*
Accept a node structure, an array and an integer that represents size of the list.
Declare a new node pointer. If array still remains element to be inserted, initialize new node, connect with node structure and call this function again.
If not, return the node structure.
*/
struct nodeD *createListRe(struct nodeD *parentRe,int arrayRe[],int sizeRe)
{
    struct nodeD *newP;
    sizeRe-=1;

    if(sizeRe >= 0){
        newP = (struct nodeD *)malloc(sizeof(struct nodeD));
        (*newP).data = arrayRe[sizeRe];
        (*newP).next = NULL;
        if(parentRe == NULL){//For root node
            (*newP).before = NULL;
            parentRe = newP;
            parentRe = createListRe(parentRe,arrayRe,sizeRe);
        }else{//For non-root node
            (*newP).before = parentRe;
            (*parentRe).next = newP;
            newP = createListRe(newP,arrayRe,sizeRe);
        }
    }

    return parentRe;
}

void traverseD(struct nodeD* tListD)
{
    int j;

    for(j = 0;tListD != NULL;j++){
        printf("Node %d: %d\n",j,tListD->data);
        tListD = tListD->next;
    }
    printf("dsakflajfldsajflk");
}

/*
 * Function Name: changeElementRe
 * Purpose: Recursively change a target node's value to a given value in the Doubly Linked list

 * Parameters:
     - cListRe: Pointer to the root of the doubly linked list.
     - positionRe: Integer representing the position of target node.(1-based index).
     - elementRe: Integer representing the value to be replaced in the target node.

 * Returns:
     - Pointer to the root of the updated doubly linked list.

 * Logic:
     1. Check if the current node is at the positionRe position in the list.
        - If not, and the next node exists, recursively call the function to traverse the list.
        - If the next node does not exist, print an error message indicating that positionRe exceeds the list size.
     2. If the current node is at positionRe, update its value to valueRe.
     3. Ensure positionRe is positive, otherwise print an error message.
     4. Return the root pointer of the updated list after modification.
*/
struct nodeD *changeElementRe(struct nodeD* cListRe,int positionRe,int valueRe)
{
    // Early exit for invalid position
    if (positionRe <= 0) {
        printf("The given parameter positionRe is not a positive integer.\n");
        return cListRe;
    }

    if(positionRe > 1){//Node not found yet
        if((*cListRe).next != NULL){
            (*cListRe).next = changeElementRe((*cListRe).next,positionRe-1,valueRe);
        }else{
            printf("The given parameter positionRe is too long for this list.\n");
        }
    }else{//Node found
        (*cListRe).data = valueRe;
    }

    return cListRe;
}

/*
 * Function Name: insertAfKRe
 * Purpose: Recursively insert a new node with a given value  at the specified position in a doubly linked list.

 * Parameters:
    - present: Pointer to the root of the doubly linked list.
    - positionRe: Integer representing the position where the new node is to be inserted.(1-based index)
    - valueRe: Integer representing the value of the node to be inserted.

 * Returns:
    - Pointer to the root of the updated doubly linked list.

 * Logic:
    1. If positionRe is 1, insert the new node at the beginning.
    2. If positionRe is 2, insert the new node after the current node.
    3. Otherwise, if the next node exists, recursively call the function with positionRe decremented by 1.
    4. If the next node does not exist and positionRe is greater than the list length, print an error message.
    5. Return the updated root pointer.
*/
struct nodeD *insertAtKRe(struct nodeD * present,int positionRe,int valueRe)
{
    struct nodeD *tmp;

    if (positionRe <= 0) {
        printf("The given parameter positionRe is not a positive integer.\n");
        return present;
    }

    if(positionRe == 1){
        tmp = (struct nodeD *)malloc(sizeof(struct nodeD));
        if(!tmp){
            printf("Memory allocation failed.\n");
            return present;
        }else{
            (*tmp).data = valueRe;
            (*tmp).before = NULL;
            (*tmp).next = present;
            if (present != NULL) {
                (*present).before = tmp;
            }
            return present;
        }
    }

    if(positionRe == 2){
        tmp = (struct nodeD*)malloc(sizeof(struct nodeD));
        if(!tmp){
            printf("Memory allocation failed.\n");
            return present;
        }
        (*tmp).data = valueRe;
        (*tmp).before = present;
        (*tmp).next = (*present).next;
        if((*present).next != NULL){
            (*(*present).next).before = tmp;
        }
        (*present).next = tmp;
        return present;
    }

    if((*present).next != NULL){
        (*present).next = insertAtKRe((*present).next, --positionRe, valueRe);
    }else{
        printf("The given parameter positionRe is too long for this list.\n");
    }

    return present;
}

/*
 * Function Name: deleteKRe
 * Purpose: Delete a node at a specified position in the doubly linked list.

 * Parameters:
    - present: Pointer to the root of the doubly linked list.
    - positionRe: Integer representing the position of deleted node.(1-based index)
 * Returns:
    - Pointer to the root of the updated linked list.
 * Logic:
    1. If positionRe is 1, delete the current node.
    2. Check if the next node of current node exists
        -If so, recursively call the function to traverse this list.
        -If not, print error message.
    3. Return the updated root pointer
*/
struct nodeD *deleteKRe(struct nodeD *present,int positionRe)
{
    struct nodeD *tmp;

    if(positionRe <= 0){
        printf("The given parameter positionRe is not a positive integer.\n");
        return present;
    }

    if(positionRe == 1){
        tmp = present;
        if(present->next){//Special case for last node
            present->next->before = tmp->before;
            present = present->before;
        }
        if(present->before){//Special case for root node
            present->before->next = tmp->next;
            present = present->next;
        }
        free(tmp);
        return present;
    }

    if(present->next != NULL){
        present->next = deleteKRe(present->next,--positionRe);
    }else{
        printf("The parameter positionRe is too long for this list.\n");
    }

    return present;
}

struct nodeD *swapAdjacent(struct nodeD *present,int positionRe)
{
    struct nodeD *tmp;
    int backup;

    if(positionRe <= 0){
        printf("The parameter positionRe is not a positive integer.\n");
        return present;
    }

    if(present->next != NULL){
        if(positionRe == 1){
            tmp = present->next;
            backup = tmp->data;
            tmp->data = present->data;
            present->data = backup;
        }else{
            present->next = swapAdjacent(present->next,--positionRe);
        }
    }else{
        printf("The parameter positionRe is too long for this list.\n");
    }

    return present;
}

/*
 * Function Name: swapNonAdj
 * Purpose: Swap 2 non-adjacent nodes'elements using recursion.

 * Parameters:
    -nodeA: Pointer to the root of the doubly linked list.
    -nodeB: Same as nodeA.
    -posA: Integer representing the position where first node at.(1-based index)
    -posB: Integer representing the position where second node at.(1-based index)

 * Returns: Pointer to the root of the updated list.

 * Logic:
    1.If positionA is greater than positionB, swap them.
    2.Move nodeA and nodeB recursively and simultaneously, until find the first node's position.
    3.Move only nodeB recursively, until find the second node's position.
    4.Swap two nodes' elements.
    5.Return the updated nodeA's pointer.
*/
struct nodeD *swapNonAdj(struct nodeD *nodeA,struct nodeD *nodeB,int posA,int posB)
{
    int backup;

    if(posA > posB){
        backup = posA;
        posA = posB;
        posB = backup;
    }

    if(posA != 1){//Have not found nodeA
        if(nodeA->next != NULL){
            nodeA->next = swapNonAdj(nodeA->next,nodeB->next,posA-1,posB-1);
            return nodeA;
        }else{
            printf("PositionA is too long for this list.\n");
            return nodeA;
        }
    }else{
        if(posB != 1){//Have found nodeA, but not nodeB
            if(nodeB->next != NULL){
                nodeB->next = swapNonAdj(nodeA,nodeB->next,posA,posB-1);
                return nodeB;
            }else{
                printf("PositionB is too long for this list.\n");
                return nodeB;
            }
        }else{//Have found nodeA and nodeB
            backup = nodeA->data;
            nodeA->data = nodeB->data;
            nodeB->data = backup;
            return nodeB;
        }
    }

    return nodeA;//For return back to callee.
}








