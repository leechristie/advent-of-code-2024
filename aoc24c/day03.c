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

#define MAX_LENGTH (12)

typedef struct MulStateData {
    char string[MAX_LENGTH + 1];
    size_t length;
    MulState state;
} MulStateData;

static void MulStateData_Init(MulStateData * const data) {
    data->string[0] = '\0';
    data->length = 0;
    data->state = START;
}

static void MulStateData_AppendAndSwitchState(MulStateData * const data, const char character, const MulState state) {
    assert(data->length < MAX_LENGTH);
    data->string[data->length] = character;
    data->length++;
    data->string[data->length] = '\0';
    data->state = state;
}

static int parse_int_1_to_3_digits(const char * const string, int i) {

    // first digit
    assert(isdigit(string[i]));
    int rv = string[i] - '0';

    // second digit
    i++;
    if (!isdigit(string[i]))
        return rv;
    rv = 10 * rv + (string[i] - '0');

    // third digit
    i++;
    if (!isdigit(string[i]))
        return rv;
    rv = 10 * rv + (string[i] - '0');

    // next character after 3rd digit
    i++;
    assert(!isdigit(string[i]));
    return rv;

}

static int MulStateData_Evaluate(const MulStateData * const data) {
    assert(data->state == MULOXCYE);
    int i = 0;
    while (!isdigit(data->string[i]))
        i++;
    const int left = parse_int_1_to_3_digits(data->string, i);
    while (data->string[i] != ',')
        i++;
    while (!isdigit(data->string[i]))
        i++;
    const int right = parse_int_1_to_3_digits(data->string, i);
    return left * right;
}

static void MulStateData_Print(const MulStateData * const data) {
    printf("data = \"%s\" (length = %lu, state = %d)", data->string, data->length, data->state);
}

static void MulStateData_Update(MulStateData * const data, const char character) {

    /* resetting state to start of an active parse on 'm' or 'd' */

    if (character == 'm') {
        MulStateData_Init(data);
        MulStateData_AppendAndSwitchState(data, character, M);
        data->state = M;
    } else if (character == 'd') {
        MulStateData_Init(data);
        MulStateData_AppendAndSwitchState(data, character, D);
        data->state = D;

    /* progressing mul states */

    } else if (data->state == M && character == 'u') {
        MulStateData_AppendAndSwitchState(data, character, MU);
    } else if (data->state == MU && character == 'l') {
        MulStateData_AppendAndSwitchState(data, character, MUL);
    } else if (data->state == MUL && character == '(') {
        MulStateData_AppendAndSwitchState(data, character, MULO);
    } else if (data->state == MULO && isdigit(character)) {
        MulStateData_AppendAndSwitchState(data, character, MULOX);
    } else if (data->state == MULOX && isdigit(character)) {
        MulStateData_AppendAndSwitchState(data, character, MULOXX);
    } else if (data->state == MULOXX && isdigit(character)) {
        MulStateData_AppendAndSwitchState(data, character, MULOXXX);
    } else if ((data->state == MULOX || data->state == MULOXX || data->state == MULOXXX) && character == ',') {
        MulStateData_AppendAndSwitchState(data, character, MULOXC);
    } else if (data->state == MULOXC && isdigit(character)) {
        MulStateData_AppendAndSwitchState(data, character, MULOXCY);
    } else if (data->state == MULOXCY && isdigit(character)) {
        MulStateData_AppendAndSwitchState(data, character, MULOXCYY);
    } else if (data->state == MULOXCYY && isdigit(character)) {
        MulStateData_AppendAndSwitchState(data, character, MULOXCYYY);
    } else if ((data->state == MULOXCY || data->state == MULOXCYY || data->state == MULOXCYYY) && character == ')') {
        MulStateData_AppendAndSwitchState(data, character, MULOXCYE);

    /* progressing the do or don't parse */

    } else if (data->state == D && character == 'o') {
        MulStateData_AppendAndSwitchState(data, character, DO);

    /* progressing the do parse */

    } else if (data->state == DO && character == '(') {
        MulStateData_AppendAndSwitchState(data, character, DOO);
    } else if (data->state == DOO && character == ')') {
        MulStateData_AppendAndSwitchState(data, character, DOOE);

    /* progressing the don't parse */

    } else if (data->state == DO && character == 'n') {
        MulStateData_AppendAndSwitchState(data, character, DON);
    } else if (data->state == DON && character == '\'') {
        MulStateData_AppendAndSwitchState(data, character, DONA);
    } else if (data->state == DONA && character == 't') {
        MulStateData_AppendAndSwitchState(data, character, DONAT);
    } else if (data->state == DONAT && character == '(') {
        MulStateData_AppendAndSwitchState(data, character, DONATO);
    } else if (data->state == DONATO && character == ')') {
        MulStateData_AppendAndSwitchState(data, character, DONATOE);

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
            const int value = MulStateData_Evaluate(&data);
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
