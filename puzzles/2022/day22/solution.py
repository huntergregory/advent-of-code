import numpy as np

USE_TEST_INPUT = False

## constants and helpers
COUNTER_CLOCKWISE = 'L'
CLOCKWISE = 'R'

EMPTY = 0
WALKABLE = 1
WALL = 2

UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'

grid_mapping = {
    ' ': EMPTY,
    '.': WALKABLE,
    '#': WALL,
}

direction_values = {
    RIGHT: 0,
    DOWN: 1,
    LEFT: 2,
    UP: 3,
}

# could have also implemented this as numbers 0 through 4 and a modulo operation
clockwise_direction = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP,
}

counter_clockwise_direction = {
    UP: LEFT,
    LEFT: DOWN,
    DOWN: RIGHT,
    RIGHT: UP,
}

# in row, col format
direction_deltas = {
    UP: [-1,0],
    DOWN: [1,0],
    RIGHT: [0,1],
    LEFT: [0,-1],
}

def in_bounds(r, c, grid_shape):
    return r >= 0 and c >= 0 and r < grid_shape[0] and c < grid_shape[1]

## part 1 wrap behavior
def wrap_part1(r, c, delta_r, delta_c, grid):
    # go backwards until the end of walkable territory
    while in_bounds(r, c, grid.shape) and grid[r][c] != EMPTY:
        r -= delta_r
        c -= delta_c

    # went one too far based on while loop
    r += delta_r
    c += delta_c
    return r, c

## part 2 wrap behavior
BASE = 0
ROOF = 1
NORTH_WALL = 2
EAST_WALL = 3
SOUTH_WALL = 4
WEST_WALL = 5

# actual input
face_size = 50
quadrants = [
    (100,50), # Base
    (0,50),   # Roof
    (50,50),  # North-Wall
    (0,100),  # East-Wall
    (150,0),  # South-Wall
    (100,0),  # West-Wall
]
# easiest to manually find connection data (not sure if this can/should be automated)
# stores connection locations/orientations and a way to transform coordinates from one to the other
connections = {
    (BASE, RIGHT): (
        EAST_WALL,
        RIGHT,
        lambda r_diff, c_diff: ((face_size-1) - r_diff, c_diff)
    ),
    (BASE, DOWN): (
        SOUTH_WALL,
        RIGHT,
        lambda r_diff, c_diff: (c_diff, r_diff),
    ),
    (EAST_WALL, UP): (
        SOUTH_WALL,
        DOWN,
        lambda r_diff, c_diff: ((face_size-1) - r_diff, c_diff),
    ),
    (EAST_WALL, DOWN): (
        NORTH_WALL,
        RIGHT,
        lambda r_diff, c_diff: (c_diff, r_diff),
    ),
    (ROOF, UP): (
        SOUTH_WALL,
        LEFT,
        lambda r_diff, c_diff: (c_diff, r_diff),
    ),
    (ROOF, LEFT): (
        WEST_WALL,
        LEFT,
        lambda r_diff, c_diff: ((face_size-1)-r_diff, c_diff),
    ),
    (NORTH_WALL, LEFT): (
        WEST_WALL,
        UP,
        lambda r_diff, c_diff: (c_diff, r_diff),
    ),
}

# the test input has a different layout...
if USE_TEST_INPUT:
    # test input
    face_size = 4
    quadrants = [
        (4,8),  # Base
        (4,0),  # Roof
        (0,8),  # North-Wall
        (8,12), # East-Wall
        (8,8),  # South-Wall
        (4,4),  # West-Wall
    ]
    connections = {
        (ROOF, LEFT): (
            EAST_WALL,
            DOWN,
            lambda r_diff, c_diff: ((face_size-1)-c_diff, (face_size-1) - r_diff),
        ),
        (ROOF, UP): (
            NORTH_WALL,
            UP,
            lambda r_diff, c_diff: ((face_size-1) - r_diff, (face_size-1) - c_diff),
        ),
        (ROOF, DOWN): (
            SOUTH_WALL,
            DOWN,
            lambda r_diff, c_diff: (r_diff, (face_size-1) - c_diff),
        ),
        (WEST_WALL, DOWN): (
            SOUTH_WALL,
            LEFT,
            lambda r_diff, c_diff: ((face_size-1) - c_diff, (face_size-1) - r_diff),
            # 3, 2 -> 1, 0
            # 1, 0 -> 3, 2
        ),
        (WEST_WALL, UP): (
            NORTH_WALL,
            LEFT,
            lambda r_diff, c_diff: (c_diff, r_diff),
        ),
        (BASE, RIGHT): (
            EAST_WALL,
            UP,
            lambda r_diff, c_diff: ((face_size-1) - c_diff, (face_size-1) - r_diff),
        ),
        (EAST_WALL, RIGHT): (
            NORTH_WALL,
            RIGHT,
            lambda r_diff, c_diff: ((face_size-1) - r_diff, c_diff),
        ),
    }

# include reverse mappings
for k, v in list(connections.items()):
    k2 = (v[0], v[1])
    v2 = (k[0], k[1], v[2])
    connections[k2] = v2

def quadrant(r, c):
    for q, rc in enumerate(quadrants):
        if rc[0] == (r // face_size) * face_size and rc[1] == (c // face_size) * face_size:
            return q
    return -1

def wrap_part2(r, c, direction):
    q_old = quadrant(r, c)
    r_q_old, c_q_old = quadrants[q_old]
    r_diff = r - r_q_old
    c_diff = c - c_q_old
    k = (q_old, direction)
    if k not in connections:
        raise Exception('no connection available for wrapping: ({}, {}, {})'.format(r+1, c+1, k))
    q_new, connected_direction, transform = connections[k]
    r_t, c_t = transform(r_diff, c_diff)
    r_q_new, c_q_new = quadrants[q_new]
    r_new = r_q_new + r_t
    c_new = c_q_new + c_t

    # new direction is the reverse of the connected direction (two 90-degrees rotations)
    new_direction = clockwise_direction[clockwise_direction[connected_direction]]
    return r_new, c_new, new_direction
    

## parse input
filepath = 'inputs/test-input.txt' if USE_TEST_INPUT else 'inputs/input.txt'
with open(filepath) as f:
    lines = f.read().splitlines()
    shape = (len(lines)-2, max([len(l) for l in lines]))
    grid = np.zeros(shape)
    for i, l in enumerate(lines):
        if len(l) == 0:
            continue

        if i == len(lines)-1:
            instructions = l
            break

        for j, ch in enumerate(l):
            grid[i][j] = grid_mapping[ch]

## traverse the path
# set starting point
def starting_pos():
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r][c] == WALKABLE:
                return r, c

r, c = starting_pos()
direction = RIGHT
print('starting position: ({}, {}, {})'.format(r+1, c+1, direction))

i = 0
while i < len(instructions):
    if instructions[i] == CLOCKWISE:
        direction = clockwise_direction[direction]
        print('turned: {}'.format(direction))
        i += 1
        continue

    if instructions[i] == COUNTER_CLOCKWISE:
        direction = counter_clockwise_direction[direction]
        print('turned {}'.format(direction))
        i += 1
        continue

    j = i
    i += 1
    while i < len(instructions) and instructions[i] not in (CLOCKWISE, COUNTER_CLOCKWISE):
        i += 1

    steps = int(instructions[j:i])
    print('steps: {}'.format(steps))

    delta_r, delta_c = direction_deltas[direction]
    for _ in range(steps):
        # try moving forward
        r_new = r + delta_r
        c_new = c + delta_c
        if in_bounds(r_new, c_new, grid.shape):
            if grid[r_new][c_new] == WALKABLE:
                r = r_new
                c = c_new
                continue
            if grid[r_new][c_new] == WALL:
                # don't update current position, and stop trying to move forward
                break
        
        # out of bounds or at an empty square
        # return to previous position, then wrap around if possible
        # r_new, c_new = wrap_part1(r, c, delta_r, delta_c, grid)
        r_new, c_new, direction_new = wrap_part2(r, c, direction)
        if grid[r_new][c_new] == WALL:
            # cannot wrap around. stop trying to move forward
            print('cannot wrap because of wall')
            break

        # successfully wrapped around
        r = r_new
        c = c_new
        direction = direction_new
        delta_r, delta_c = direction_deltas[direction]
        print('wrapped to: ({}, {}, {})'.format(r+1, c+1, direction))

    print('new position: ({}, {}, {})'.format(r+1, c+1, direction))

    if USE_TEST_INPUT:
        grid[r][c] = 7
        print(grid)
        grid[r][c] = WALKABLE

print('final position: ({}, {}, {})'.format(r+1, c+1, direction))
val = 1000*(r+1) + 4*(c+1) + direction_values[direction]
print('value: {}'.format(val))
