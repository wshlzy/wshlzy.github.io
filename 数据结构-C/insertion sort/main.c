#include <stdio.h>
#include <stdlib.h>

void insertSort(int[],int);
void shellSort(int[],int,int);
void percDown(int[],int,int);
void swapA(int[],int,int);
void heapSort(int[],int);
void mergeSort();

void quickSort();

int sum = 0;//Global counter

int main()
{
    int z;
    int array[] = {0,3,1,4,1,5,9,2,6};//position 0 as tmp
    int size = sizeof(array)/sizeof(array[0]);
    //int shell[] = {1,3,7};


    for(z = 1;z < size;z++)
        printf("%d ",array[z]);

    return 0;
}

void insertSort(int oriArray[],int load)
{
    int i,j;

    for(i = 2;i < load;i++)
    {
        oriArray[0] = oriArray[i];
        for(j = i;j > 1&&oriArray[j - 1] > oriArray[0];j--)
            oriArray[j] = oriArray[j - 1];
        oriArray[j] = oriArray[0];
    }
}

void shellSort(int shellArray[],int sLoad,int shell)
{
    int i,j;

    for(i = 1+shell;i < sLoad;i++)
    {
        shellArray[0] = shellArray[i];
        for(j = i;j > 1&&shellArray[j - shell] > shellArray[0];j-=shell)
            shellArray[j] = shellArray[j - shell];
            sum++;
        shellArray[j] = shellArray[0];
    }
    printf("\nFor %d shell:",shell);
}

void percDown(int percArray[],int target,int pLoad)
{
    int child = 2*target;
    int flag = 0;

    for(percArray[0] = percArray[target];flag != 1&&(2*target) < pLoad;)
    {
        if(child+1 < pLoad)
        {
            if(percArray[child] >= percArray[child+1])
                child++;
        }
        if(percArray[0] > percArray[child])
        {
            percArray[target] = percArray[child];
            target = child;
            child = 2*target;
        }
        else
            flag = 1;
    }
    percArray[target] = percArray[0];
}

void swapA(int swapArray[],int numA,int numB)
{
    swapArray[0] = swapArray[numA];
    swapArray[numA] = swapArray[numB];
    swapArray[numB] = swapArray[0];
}

void heapSort(int heapArray[],int hLoad)
{
    int i,j;
    int center = hLoad/2;

    for(i = center;i >= 1;i--)
        percDown(heapArray,i,hLoad);

    for(j = hLoad-1;j > 1;j--)
    {
        swapA(heapArray,1,j);
        percDown(heapArray,1,j);
        printf("delete %d:",heapArray[j]);
        for(i = 1;i < hLoad;i++)
            printf("%d ",heapArray[i]);
        printf("\n");
    }
}

