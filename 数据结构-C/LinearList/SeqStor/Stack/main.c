#include <stdio.h>
#include <stdlib.h>

struct stack{
    int data;
    struct stack *next_to_top;
};

void push(struct stack *,int);
int pop(struct stack *);
struct stack *create_stack_list(struct stack *,int[],int);

int main()
{
    struct stack *top = NULL;
    int array[] = {1,6,4,3,8,2,5,7};
    int size = sizeof(array)/sizeof(array[0]);

//    top = create_stack_list(top,array,size);
//    printf("%d\n",top->data);
//    push(top)

    return 0;
}

void push(struct stack *top,int element)
{
    struct stack *newP = (struct stack *)malloc(sizeof(struct stack));

    if(newP == NULL){
        printf("Memory is full");
    }else{
        newP->data = element;
        newP->next_to_top = top;
        top = newP;
    }
}

/*
 *Function Name: create_stack_list
 *Purpose: Use the given array to create a stack along with the top pointer

 *Parameters:
    -top: Top of the stack pointer, can be whether empty or stored with data.
    -data_list: An integer array containing data that will be inserted into stack.
    -list_size: An integer number representing size of the array.

 *Returns:
    -Top of the updated stack pointer.

 *Logic:
    1.The function first verifies if top pointer is empty or not
    2.It then iterates through all elements in the array, put it into the stack
    3.At last, return top pointer
*/
struct stack *create_stack_list(struct stack *top,int data_list[],int list_size)
{
    struct stack *newP = NULL;
    int flag = 0; //Start from 0 to represent where to start in the data_list when iterating

    if(top == NULL){//Handle the situation when the passing stack is empty
        top = (struct stack *)malloc(sizeof(struct stack));
        top->data = data_list[flag];
        top->next_to_top = NULL;
        flag+=1;
    }

    while(flag < list_size){
        newP = (struct stack *)malloc(sizeof(struct stack));
        newP->data = data_list[flag];
        newP->next_to_top = top;
        top = newP;
        flag+=1;
    }

    return top;
}
