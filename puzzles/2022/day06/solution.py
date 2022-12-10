# optimized approach (sliding window)
# for a 2.7MB file, takes 0.05 seconds (takes ~1 to 5 seconds for approaches in suboptimal-solutions.py)
MARKER_SIZE = 14

with open('input/input.txt') as f:
    line = f.read().splitlines()[0]

i = 0
marker_start = 0
while i < len(line):
    for j in range(i-1, marker_start, -1):
        if line[i] == line[j]:
            marker_start = j+1
            break
    if i - marker_start + 1 == MARKER_SIZE:
        break
    i += 1

if i >= len(line):
    raise ValueError('end of line')

# 2823 for original input
print('marker received at character {}'.format(i+1))
