#ifndef LRUcache_h
#define LRUcache_h
struct nodeC{
    int key;
    int value;
    struct nodeC *next;
    struct nodeC *prev;
};

struct LRUcache{
    int capacity;
    struct nodeC *head;
    struct nodeC *tail;
    int cache[];
};

struct nodeC *ini_node(int);
struct LRUcache *ini_cache(int);
#endif // LRUcache_h
