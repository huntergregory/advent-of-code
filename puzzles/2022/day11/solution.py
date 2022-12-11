import numpy as np
from collections import deque

starting_items = []
# not sure how to quickly set the lambdas programmatically
operations = [
    lambda x: x*3,
    lambda x: x+2,
    lambda x: x+1,
    lambda x: x+5,
    lambda x: x+4,
    lambda x: x+8,
    lambda x: x*7,
    lambda x: x*x,
]
divisors = []
destinations = []

with open('input.txt') as f:
    lines = f.read().splitlines()
    i = 0
    while i < len(lines):
        starting = lines[i+1].split(': ')[1].split(', ')
        starting_items.append(deque([int(s) for s in starting]))
        div = int(lines[i+3].split(' ')[-1])
        divisors.append(div)
        true_dst = int(lines[i+4].split(' ')[-1])
        false_dst = int(lines[i+5].split(' ')[-1])
        destinations.append((true_dst, false_dst))
        i += 7

print(starting_items)
print(divisors)
print(destinations)

common_multiple = 1
for div in divisors:
    common_multiple *= div

counts = np.zeros(len(starting_items), dtype=int)
for i in range(10000):
    for j in range(len(starting_items)):
        # print('here. i: {}. j: {}'.format(i, j))
        queue = starting_items[j]
        l = len(queue)
        for _ in range(l):
            item = queue.popleft()
            counts[j] += 1
            item = operations[j](item) # // 3 # for part 1
            true_dst, false_dst = destinations[j]
            dst = true_dst if item%divisors[j] == 0 else false_dst
            if i%100 == 0:
                print('i: {}. j: {}. item: {}'.format(i, j, item))
            starting_items[dst].append(item)

    # to keep numbers from getting too big, take the modulus with a common multiple of all divisors
    # other modulus operations won't be impacted
    for j in range(len(starting_items)):
        queue = starting_items[j]
        for _ in range(l):
            queue.append(queue.popleft()%common_multiple)

# top 2
b_index = np.argmax(counts)
b1 = counts[b_index]
counts[b_index] = 0
b2 = np.max(counts)

print('monkey business:', b1*b2)
