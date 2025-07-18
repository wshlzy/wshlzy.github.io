#include <stdio.h>
#include <stdlib.h>
#include <time.h>
//Add & is when you want to get variable's address.
//Add * is when you want to get the value stored in the address; Or used in data type area, store the memory address of a specific data type.
struct node{
    int data;
    int quantity;
    struct node* LC;
    struct node* RC;
};

// contract, what this does, valid inputs, valid range of outputs
struct node* insertion(struct node**,int);
struct node* createNode(struct node**,int);
struct node* findP(struct node**,int);
void fatalError(char[]);
void printTree(struct node*,int);
struct node* findMin(struct node**);
struct node* findMax(struct node**);
void deletion(struct node**,int);

int main()
{
    int i;
    int array[] = {1,5,4,7,4,6,2,9,11,13,2,8,10,5,3,100,14,21,0,1};
    int total = sizeof(array)/sizeof(array[0]);
    struct node* tree = NULL;

    for(i = 0;i < total;i++)
    {
        tree = insertion(&tree,array[i]);
    }

    printTree(tree,-1);
    for(i = total - 1;i >= 0;i--){
        deletion(&tree,array[i]);
        printf("\ndeleted node = %d\n\n",array[i]);
        printTree(tree,-1);
    }
    printTree(tree,-1);

    return 0;
}
/*
*Insert a new node to the passed tree.*

Contract to createNode, findP functions.

This function first determine whether tree is empty or not:
    If empty, use root to create a new node;
    If not empty, go to find newVal's parent node:
        if newVal smaller than found node's data:
            if newVal exist in tree, add up quantity;
            if does not exist, use found node's LC to create a new node.
        if newVal greater than found node's data:
            if newVal exist in tree, add up quantity;
            if does not exist, use found node's RC to create a new node.
        if newVal equals to found node's data(which is root, because root have no parent, hence return itself), add up quantity.
Return the root pointer.

Input includes root's pointer and inserted data.

Output is the root's pointer.
*/
struct node* insertion(struct node** tree,int newVal)
{
    if(*tree == NULL)
        *tree = createNode(&(*tree),newVal);
    else{
        struct node* newP = NULL;
        newP = findP(&(*tree),newVal);

        if(newVal < newP->data){
            if(newP->LC != NULL && newVal == newP->LC->data)
                newP->LC->quantity++;
            else{
                newP = createNode(&(newP->LC),newVal);
            }
        }else if(newVal > newP->data){
            if(newP->RC != NULL && newVal == newP->RC->data)
                newP->RC->quantity++;
            else{
                newP = createNode(&(newP->RC),newVal);
            }
        }else
            newP->quantity++;//When root's data is duplicated
    }

    return *tree;
}

/*
*Create a node and assign data to it using the passed empty node's pointer.*

Contract to nothing.

This function first create an empty node using the passed pointer, then determine whether this node be created or not(its pointer point to NULL or not):
    if it already been created, set data, quantity(lazy deletion), left and right child's pointer;
    if it not been created, print error of memory out of space.
Return this node.

Input includes node's pointer which is where the inserted data wants to be inserted, and the inserted data.

Output is the new created node's pointer.
*/
struct node* createNode(struct node** emptyP,int createData)
{
    *emptyP = (struct node*)malloc(sizeof(struct node));

    if(*emptyP != NULL)
    {
        (*emptyP)->data = createData;
        (*emptyP)->quantity = 1;
        (*emptyP)->LC = (*emptyP)->RC = NULL;
    }
    else
        fatalError("Sorry, memory out of space");

    return *emptyP;
}


/*
*Find parent node of child node that contains the target data using passed tree.*

Contract to nothing.

This function first create a new pointer points to the passed root, and a flag to determine whether target node exists or not.
Then it start a loop which will keep iterate until find the target node or the place to insert the target node inside the tree.
Return the found node or parent node of the ready to inserted node.

Input includes the root's pointer and target data.

Output is the parent node of the target node.
*/

/*When set preNode to NULL, it ends the traversal in the tree and lose all the place information recording where this node is placed.
So whether return its parent node or send back the NULL pointer's address(might help).*/
struct node* findP(struct node** root,int target)
{
    struct node* preNode = *root;
    struct node* parent = *root;

    while(preNode != NULL&&preNode->data != target)
    {
        parent = preNode;

        if(target < preNode->data)
            preNode = preNode->LC;
        else if(target > preNode->data)
            preNode = preNode->RC;
    }

    return parent;
}

//for error printing
void fatalError(char errorMes[])
{
    printf("\n");
    puts(errorMes);
    printf("\n");
}

/*
*Print all the information inside one node.*

Contract to nothing.

Input is the root's pointer.

Output is nothing.
*/
void printTree(struct node* rootP,int depth)
{
    struct node* copy = rootP;
    int i;
    depth++;

    if(copy != NULL){
        if(depth != 0){
            for(i = 1;i < depth;i++)
                printf("   ");
            printf("|__");
        }
        printf("%d quantity:%d \n",copy->data,copy->quantity);
        printTree(copy->LC,depth);
        printTree(copy->RC,depth);
    }
}


struct node* findMin(struct node** lBranch)
{
    struct node* lBrcPrt = *lBranch;
    struct node* copy = *lBranch;

    while(copy->LC){
        lBrcPrt = copy;
        copy = copy->LC;
    }

    return lBrcPrt;
}

/*
*Return the Rightest node and its parent.*

Iterate the passed tree's pointer to right child when it is not NULL.
*/
struct node* findMax(struct node** rBranch)
{
    struct node* rBrcPrt = *rBranch;
    struct node* copy = *rBranch;

    while(copy->LC){
        rBrcPrt = copy;
        copy = copy->RC;
    }

    return rBrcPrt;
}

/*
Accepts a binary tree and a aim value, find node that have the aim value, which called delete node.
Replace its value with the minimum value of node from the right subtree of the delete node, which called replace node.
After change replace node's pointer, delete the replace node.
If no delete node inside the tree, print error.
If delete node has less than 1 child, change its pointer and delete the delete node.

Anticipated error:
    When find delete node and replace node, function return their parent node whether they exist or not.
    When delete node is root, its returning parent node will be the root as well.
        In this case, add a special if statement change root to replace node might help.
    When find the parent node of delete node, how to find delete node? This is also the problem for find replace node after find its parent node.
        In this case, first determine if delete node's parent node's left and right child is exist or not, then determine which child's value equal to aim value, and set delete node if equal.
*/

void deletion(struct node** subtree, int aim)
{
    struct node* del = NULL;
    struct node* delPrt = NULL;
    struct node* replace = NULL;
    struct node* replacePrt = NULL;
    int flag = 0;//flag record delete node in which side of its parent. 1 for left, 0 for right.

    delPrt = findP(&(*subtree),aim);//assign delPrt with the returned parent node's pointer of delete node.

    if(delPrt->LC != NULL&&delPrt->LC->data == aim){//for delete node in left side, assign del and record the side status using flag.
        flag = 1;
        del = delPrt->LC;
    }
    if(delPrt->RC != NULL&&delPrt->RC->data == aim)//for delete node in right side, assign del and record the status using flag.
        del = delPrt->RC;

    if((*subtree)->data == aim){//special case for delete root: if passed tree's root equals aim value, set delete node as root.
        del = *subtree;
        delPrt = NULL;//delPrt can be a flag separating root case and non-root case.
    }

    if(del != NULL){//since del will not be assigned if each side of delPrt's value is not equal to aim value.
        if(del->quantity == 1){//for case that no need to use lazy deletion
            if(del->LC&&del->RC){//case that delete node have 2 children can be transformed into case that has less than 1 child.
                replacePrt = del;
                replacePrt = findMin(&replacePrt->RC);//can also be changed as findMax in left branch of delete node.
                if(del == replacePrt)//indicate delete node's right child do not have left branch.
                    replace = replacePrt->RC;
                else{//indicate delete node's right child have left branch.
                    flag = 1;//since later on, delete node will be used to represent right now replace node's place, so the side status need to update.
                    replace = replacePrt->LC;
                }
                del->data = replace->data;
                del = replace;//delete node will be free later.
                delPrt = replacePrt;
            }

            if(flag){//del in left side of delPrt
                if(flag && delPrt != NULL)
                    delPrt->LC = del->RC;
                else if(!flag && delPrt != NULL)
                    delPrt->RC = del->RC;
                else//dealing with root has only left single branch.
                    *subtree = del->LC;
            }else{//del in right side of delPrt
                if(flag && delPrt != NULL)
                    delPrt->LC = del->LC;
                else if(!flag && delPrt != NULL)
                    delPrt->RC = del->LC;
                else//dealing with root has only right single branch.
                    *subtree = del->RC;
            }

            free(del);
        }else//Lazy deletion
            del->quantity--;
    }else
        fatalError("Data not found");
}
