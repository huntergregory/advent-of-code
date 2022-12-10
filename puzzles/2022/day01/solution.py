import numpy as np

elves = []
with open('input.txt') as f:
    elf = 0
    for i, line in enumerate(f.read().splitlines()):
        if line == '':
            if elf < 0:
                print('integer overflow after line {}'.format(i))
            elves.append(elf)
            elf = 0
        else:
            elf += int(line)

# part 1
print('most calories: {}'.format(max(elves)))

# part 2
top3_total = 0
for _ in range(3):
    j = np.argmax(elves)
    top3_total += elves[j]
    elves[j] = 0

print('top 3 elves have: {}'.format(top3_total))
