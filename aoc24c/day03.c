// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <stdio.h>
#include <assert.h>
#include <ctype.h>

#include "days.h"
#include "timing.h"

typedef enum MulState {

    /* state where nothing useful is being read */

    START = 0,  // no instruction

    /* states where we are parsing a mul instruction */

    M,                               // "m"
    MU,                              // "mu"
    MUL,                             // "mul"
    MULO,                            // "mul("
    MULOX, MULOXX, MULOXXX,          // "mul(###"
    MULOXC,                          // "mul(###,"
    MULOXCY, MULOXCYY, MULOXCYYY,    // "mul(###,###"
    MULOXCYE,                        // "mul(###,####)"

    /* states where we are parsing a do or don't instruction */
    D,  // d
    DO, // do

    /* states where we are parsing a do instruction */
    DOO,   // do(
    DOOE,  // do()

    /* states where we are parsing a don't instruction */
    DON,     // don
    DONA,    // don'
    DONAT,   // don't
    DONATO,  // don't(
    DONATOE  // don't()

} MulState;

typedef struct MulStateData {
    MulState state;
    int first;
    int second;
} MulStateData;

static void MulStateData_Init(MulStateData * const data) {
    data->state = START;
    data->first = 0;
    data->second = 0;
}

static void MulStateData_Update(MulStateData * const data, const char character) {

    /* resetting state to start of an active parse on 'm' or 'd' */

    if (character == 'm') {
        MulStateData_Init(data);
        data->state = M;
    } else if (character == 'd') {
        MulStateData_Init(data);
        data->state = D;

    /* progressing mul states */

    } else if (data->state == M && character == 'u') {
        data->state = MU;
    } else if (data->state == MU && character == 'l') {
        data->state = MUL;
    } else if (data->state == MUL && character == '(') {
        data->state = MULO;
    } else if (data->state == MULO && isdigit(character)) {
        data->state = MULOX;
        data->first = character - '0';
    } else if (data->state == MULOX && isdigit(character)) {
        data->state = MULOXX;
        data->first = data->first * 10 + character - '0';
    } else if (data->state == MULOXX && isdigit(character)) {
        data->state = MULOXXX;
        data->first = data->first * 10 + character - '0';
    } else if ((data->state == MULOX || data->state == MULOXX || data->state == MULOXXX) && character == ',') {
        data->state = MULOXC;
    } else if (data->state == MULOXC && isdigit(character)) {
        data->state = MULOXCY;
        data->second = character - '0';
    } else if (data->state == MULOXCY && isdigit(character)) {
        data->state = MULOXCYY;
        data->second = data->second * 10 + character - '0';
    } else if (data->state == MULOXCYY && isdigit(character)) {
        data->state = MULOXCYYY;
        data->second = data->second * 10 + character - '0';
    } else if ((data->state == MULOXCY || data->state == MULOXCYY || data->state == MULOXCYYY) && character == ')') {
        data->state = MULOXCYE;

    /* progressing the do or don't parse */

    } else if (data->state == D && character == 'o') {
        data->state = DO;

    /* progressing the do parse */

    } else if (data->state == DO && character == '(') {
        data->state = DOO;
    } else if (data->state == DOO && character == ')') {
        data->state = DOOE;

    /* progressing the don't parse */

    } else if (data->state == DO && character == 'n') {
        data->state = DON;
    } else if (data->state == DON && character == '\'') {
        data->state = DONA;
    } else if (data->state == DONA && character == 't') {
        data->state = DONAT;
    } else if (data->state == DONAT && character == '(') {
        data->state = DONATO;
    } else if (data->state == DONATO && character == ')') {
        data->state = DONATOE;

    /* resetting to the neutral start state on anything unexpected, no progression, no 'm' or 'd' */

    } else {
        MulStateData_Init(data);
    }

}

int day03() {

    start_timer();

    FILE * file = fopen("input03.txt", "r");
    if (file == NULL) {
        printf("unable to open input file");
        return 1;
    }

    int part1 = 0;
    int part2 = 0;

    MulStateData data;
    MulStateData_Init(&data);
    int c;
    bool is_enabled = true;
    while ((c = getc(file)) != EOF) {
        assert(c >= 0 && c <= 127);
        MulStateData_Update(&data, (char) c);
        if (data.state == MULOXCYE) {
            const int value = data.first * data.second;
            part1 += value;
            if (is_enabled)
                part2 += value;
        } else if (data.state == DOOE)
            is_enabled = true;
        else if (data.state == DONATOE)
            is_enabled = false;
    }

    fclose(file);

    const double time = stop_timer();
    printf("Advent of Code 2024\n");
    printf("Day 3 - Mull It Over\n");
    printf("Part 1: %d\n", part1);
    printf("Part 2: %d\n", part2);
    printf("Time Taken: %.6f s\n", time);
    return 0;

}
