// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#ifndef LIST_H
#define LIST_H

#define DEFAULT_LIST_SIZE 16

#include <assert.h>
#include <stdlib.h>

#include "fatal.h"

typedef struct {
    int * ptrBuffer;
    size_t capacity;
    size_t length;
} IntList;

static void IntList_Init(IntList * const list) {
    list->ptrBuffer = malloc(sizeof(int) * DEFAULT_LIST_SIZE);
    if (list->ptrBuffer == nullptr)
        FATAL("malloc returned nullptr");
    list->capacity = DEFAULT_LIST_SIZE;
    list->length = 0;
}

static void IntList_DeInit(IntList * const list) {
    assert(list->ptrBuffer != nullptr);
    free(list->ptrBuffer);
    list->ptrBuffer = nullptr;
    list->capacity = 0;
    list->length = 0;
}

static void IntList_Expand(IntList * const list) {
    assert(list->capacity >= 1);
    const size_t new_capacity = list->capacity * 2;
    int * new_memory = realloc(list->ptrBuffer, sizeof(int) * new_capacity);
    if (new_memory == nullptr)
        FATAL("realloc returned nullptr");
    list->ptrBuffer = new_memory;
    list->capacity = new_capacity;
}

static void IntList_Append(IntList * const list, const int value) {
    if (list->capacity == list->length) {
        IntList_Expand(list);
    }
    assert(list->capacity > list->length);
    const size_t index = list->length;
    list->ptrBuffer[index] = value;
    list->length++;
}

static int compare_int(const void * a, const void * b) {
    return *(int *) a - *(int *) b;
}

static void IntList_Sort(const IntList * const list) {
    qsort(list->ptrBuffer, list->length, sizeof(int), compare_int);
}

static ssize_t IntList_Sorted_IndexOf(const IntList * const list, const int item) {
    const int * ptrItem = bsearch(&item, list->ptrBuffer, list->length, sizeof(int), compare_int);
    if (ptrItem == nullptr)
        return -1;
    return ptrItem - list->ptrBuffer;
}

static int IntList_Sorted_CountOf(const IntList * const list, const int item) {

    ssize_t index = IntList_Sorted_IndexOf(list, item);
    if (index < 0)
        return 0;

    // move backwards until a different value is found, setting lower to first index of item
    while (index > 0) {
        index--;
        if (list->ptrBuffer[index] != item) {
            index++;
            break;
        }
    }
    const size_t lower = (size_t) index;

    // move forwards until a different value is found, setting upper to one past last index of item
    size_t bound = (size_t) index;
    while (bound < list->length) {
        bound++;
        if (bound >= list->length || list->ptrBuffer[bound] != item)
            break;
    }

    return bound - lower;

}

#endif //LIST_H
