import numpy as np

with open('input.txt') as f:
    lines = f.read().splitlines()
    grid = np.zeros((len(lines), len(lines[0])), dtype=int)
    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            grid[i][j] = int(ch)

def on_edge(i, j):
    return i == 0 or j == 0 or i == grid.shape[0]-1 or j == grid.shape[1]-1

# part 1 in O(nm)
visible = set()
# horizontals (ignore edges)
for i in range(grid.shape[0]):
    # left to right
    tallest = -1
    tallest_pos = 0
    for j in range(grid.shape[1]):
        height = grid[i][j]
        if on_edge(i, j) or tallest < height:
            visible.add((i, j))
        tallest = max(height, tallest)
    
    # right to left
    tallest = -1
    tallest_pos = grid.shape[1]-1
    for j in range(grid.shape[1]-1, -1, -1):
        height = grid[i][j]
        if on_edge(i, j) or tallest < height:
            visible.add((i, j))
        tallest = max(height, tallest)

# verticals (ignore edges)
for j in range(grid.shape[1]):
    # top to bottom
    tallest = -1
    tallest_pos = 0
    for i in range(grid.shape[0]):
        height = grid[i][j]
        if on_edge(i, j) or tallest < height:
            visible.add((i, j))
        tallest = max(height, tallest)
    
    # bottom to top
    tallest = -1
    tallest_pos = grid.shape[0]-1
    for i in range(grid.shape[0]-1, -1, -1):
        height = grid[i][j]
        if on_edge(i, j) or tallest < height:
            visible.add((i, j))
        tallest = max(height, tallest)

print('num visible trees:', len(visible))

# part 2 and brute-forcing part 1 in O(nm(n+m))
top_score = 0
visible_count = 0
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        if on_edge(i, j):
            continue

        any_good = False
        height = grid[i][j]
        score = 1
        # look down
        s = 0
        good = True
        for k in range(i+1, grid.shape[0]):
            s += 1
            if height <= grid[k][j]:
                good = False
                break
        any_good = any_good or good
        score *= s

        # look up
        s = 0
        good = True
        for k in range(i-1, -1, -1):
            s += 1
            if height <= grid[k][j]:
                good = False
                break
        any_good = any_good or good
        score *= s

        # look right
        s = 0
        good = True
        for k in range(j+1, grid.shape[1]):
            s += 1
            if height <= grid[i][k]:
                good = False
                break
        any_good = any_good or good
        score *= s

        # look left
        s = 0
        good = True
        for k in range(j-1, -1, -1):
            s += 1
            if height <= grid[i][k]:
                good = False
                break
        any_good = any_good or good
        score *= s

        top_score = max(top_score, score)
        visible_count += any_good

print('highest visibility score:', np.max(top_score))
print('visible (brute force):', visible_count + 2*grid.shape[0] + 2*grid.shape[1] - 4)
