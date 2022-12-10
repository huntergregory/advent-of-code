import numpy as np

# possible reactions (tail starting at origin)
# head (1,0)-->(2,0): tail to (1,0)
#           -->(2,1): tail to (1,1)
# head (0,1)--> X is similar...
# head (1,1)-->(2,1): tail to (1,1)
#           -->(1,2): tail to (1,1)
#           -->(2,2): tail to (1,1)
#           -->(2,0): tail to (1,0)
#           -->(0,2): tail to (0,1)
# formula: np.sign(diff)

head_deltas = {
    'D': np.array([0, -1], dtype=int),
    'U': np.array([0, 1], dtype=int),
    'R': np.array([1, 0], dtype=int),
    'L': np.array([-1, 0], dtype=int),
}

# head to tail
knots = np.zeros((10, 2), dtype=int)

positions = set()
# make sure origin is included
positions.add((0, 0))

DEBUG = False

with open('input.txt') as f:
    lines = f.read().splitlines()
    for i, line in enumerate(lines):
        dir, amt_str = line.split(' ')
        amt = int(amt_str)
        for j in range(amt):
            delta = head_deltas[dir]
            for k in range(knots.shape[0]-1):
                knots[k] += delta
                diff = knots[k] - knots[k+1]
                delta = np.zeros(2, dtype=int)
                if np.abs(diff[0]) == 2 or np.abs(diff[1]) == 2:
                    delta = np.sign(diff)
            knots[knots.shape[0]-1] += delta
            tail = knots[knots.shape[0]-1]
            positions.add((tail[0], tail[1]))

            if DEBUG or (i == len(lines)-1 and j == amt-1):
                print('going {}: round {}'.format(dir, j+1))
                print('head:', knots[0])
                for l in range(1, knots.shape[0]-1):
                    print('knot {}: {}'.format(l, knots[l]))
                print('tail:', tail)
                print()

print('unique tail positions:', len(positions))
