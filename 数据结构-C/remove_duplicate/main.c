#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
};

struct Node *createNode(int);
void removeDuplicates(struct Node *);
void printList(struct Node *);
void change_list(struct Node *);


int main() {

    // Create a sorted linked list:
    // 11->11->11->13->13->20
    struct Node *head = createNode(11);
    head->next = createNode(11);
    head->next->next = createNode(11);
    head->next->next->next = createNode(13);
    head->next->next->next->next = createNode(13);
    head->next->next->next->next->next = createNode(20);

    printf("Linked list before duplicate removal:\n");
    printList(head);

    removeDuplicates(head);

    printf("Linked list after duplicate removal:\n");
    printList(head);
    change_list(head);
    printList(head);

    return 0;
}

struct Node *createNode(int new_data) {
    struct Node *new_node = (struct Node *)malloc(sizeof(struct Node));
    new_node->data = new_data;
    new_node->next = NULL;
    return new_node;
}


// Function to remove duplicates
void removeDuplicates(struct Node *head) {

    // Base case: if the list is empty, return
    if (head == NULL)
        return;

    // Check if the next node exists
    if (head->next != NULL) {

        // If current node has duplicate data
        // with the next node
        if (head->data == head->next->data) {
            head->next = head->next->next;
            removeDuplicates(head);
        }
        else
            removeDuplicates(head->next);
    }
}

void printList(struct Node *node) {
    while (node != NULL) {
        printf("%d ", node->data);
        node = node->next;
    }
    printf("\n");
}

void change_list(struct Node *node)
{
    node->next = node->next->next;
}
