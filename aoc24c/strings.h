// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#ifndef STRINGS_H
#define STRINGS_H

#define DEFAULT_STRING_SIZE 16

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "fatal.h"

typedef struct StringBuffer {
    char * data;
    size_t length;
    size_t capacity;
} StringBuffer;

static void StringBuffer_Init(StringBuffer * const buffer) {
    buffer->capacity = DEFAULT_STRING_SIZE;
    buffer->length = 0;
    buffer->data = malloc(sizeof(char) * (buffer->capacity + 1));
    buffer->data[0] = '\0';
}

static void StringBuffer_DeInit(StringBuffer * const buffer) {
    buffer->capacity = 0;
    buffer->length = 0;
    free(buffer->data);
}

static void StringBuffer_Expand(StringBuffer * const buffer) {
    assert(buffer->capacity >= 1);
    const size_t new_capacity = buffer->capacity * 2;
    char * new_memory = realloc(buffer->data, sizeof(int) * (new_capacity + 1));
    if (new_memory == nullptr)
        FATAL_ERROR_EXIT("realloc returned nullptr");
    buffer->data = new_memory;
    buffer->capacity = new_capacity;
}

static void StringBuffer_Append(StringBuffer * const buffer, const char value) {
    if (buffer->capacity == buffer->length)
        StringBuffer_Expand(buffer);
    assert(buffer->capacity >= buffer->length);
    buffer->data[buffer->length] = value;
    buffer->length++;
    buffer->data[buffer->length] = '\0';
}

static void StringBuffer_Clear(StringBuffer * const buffer) {
    buffer->length = 0;
    buffer->data[buffer->length] = '\0';
}

static void StringBuffer_Print(const char * const name, const StringBuffer * const buffer) {
    printf("%s = \"%s\" (length = %lu, capacity = %lu)\n", name, buffer->data, buffer->length, buffer->capacity);
}

static void StringBuffer_Append_String(StringBuffer * const buffer, const char * const value) {
    const size_t length = strlen(value);
    for (size_t i = 0; i < length; i++) {
        StringBuffer_Append(buffer, value[i]);
    }
}

#endif //STRINGS_H
