# 100 --> 276KB
# 1000 --> 2.7MB
DUPLICATE_COUNT=100

cd day06/
rm long-input.txt
for i in $(seq 1 $DUPLICATE_COUNT); do
    cat non-repeating-string.txt >> long-input.txt
done
cat 14-marker-after-first-letter.txt >> long-input.txt

echo "marker will end at character $((2809 * DUPLICATE_COUNT + 15))"
ls -lah long-input.txt
