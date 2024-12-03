# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com

clear

EXECUTABLE="../aoc24cpp/cmake-build-release/aoc24cpp"
OUTPUT="../profile.txt"
CONDA_ENV="python313"

if [ -f "$OUTPUT" ]; then
    rm "$OUTPUT"
fi

echo -n "Day to profile : "
read -r day

echo -n "Number of runs : "
read -r runs

for ((i=1; i<=runs; i++)); do

    echo
    echo >> "$OUTPUT"
    echo "Run $i of $runs"
    echo "Run $i of $runs" >> "$OUTPUT"

    stdout_stderr=$("$EXECUTABLE" $day 2>&1)
    return_code=$?

    echo "$stdout_stderr"
    echo "$stdout_stderr" >> "$OUTPUT"

    if [ $return_code -ne 0 ]; then
        rm "$OUTPUT"
        echo
        exit 1
    fi

done

eval "$(conda shell.bash hook)"
conda activate "$CONDA_ENV"

which python
python --version

python ../profile.py "$OUTPUT"

rm $OUTPUT
