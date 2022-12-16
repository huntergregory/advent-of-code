ROCK = '#'
SAND = 'o'
# AIR = '.'

def rock_to_xy(rock):
    rock_split = rock.split(',')
    x = int(rock_split[0])
    y = int(rock_split[1])
    return x, y

points = {}
with open('input.txt') as f:
    for i, line in enumerate(f.read().splitlines()):
        rocks = line.split(' -> ')
        prev_x, prev_y = rock_to_xy(rocks[0])
        points[(prev_x, prev_y)] = ROCK
        path = []
        for j in range(1, len(rocks)):
            x, y = rock_to_xy(rocks[j])
            if x == prev_x:
                step = 1 if prev_y <= y else -1
                for c in range(prev_y+step, y+step, step):
                    points[(x, c)] = ROCK
                    path.append((x,c))
            elif y == prev_y:
                step = 1 if prev_x <= x else -1
                for r in range(prev_x+step, x+step, step):
                    points[(r, y)] = ROCK
                    path.append((r,y))
            else:
                Exception('unexpected x,y vs. prev_x,prev_y: ({},{}) vs. ({},{})'.format(x, y, prev_x, prev_y))
            prev_x, prev_y = x, y
        print('line {} has path: {}'.format(i, path))

max_y = 0
# max_x = 0
for p in points.keys():
    x, y = p
    # max_x = max(max_x, x)
    max_y = max(max_y, y)

# down, diagonal down-left, diagonal down-right
deltas = [(0,1), (-1,1), (1,1)]

# part 1
# count = 0
# sand_y = 0
# while sand_y < max_y:
#     # new grain of sand
#     sand_x, sand_y = 500, 0
#     while sand_y < max_y:
#         moved = False
#         for d in deltas:
#             sand = (sand_x + d[0], sand_y + d[1])
#             if sand not in points:
#                 # if not occupied, move the grain
#                 sand_x = sand[0]
#                 sand_y = sand[1]
#                 moved = True
#                 break
#         if not moved:
#             # this grain is stuck, so move on to the next
#             count += 1
#             points[(sand_x, sand_y)] = SAND
#             break

# print(count)

# part 2 (can't run with part 1 uncommented since part 1 modifies points as well)
# only differences from part 1: while loop constraints and how we detect if a point is occupied
count = 0
floor_y = max_y + 2
sand_x, sand_y = 0, 0
while not (sand_x == 500 and sand_y == 0):
    # loop while source is unblocked
    # new grain of sand
    sand_x, sand_y = 500, 0
    while True:
        moved = False
        for d in deltas:
            sand = (sand_x + d[0], sand_y + d[1])
            if not (sand in points or sand[1] >= floor_y):
                # if not occupied, move the grain
                sand_x = sand[0]
                sand_y = sand[1]
                moved = True
                break
        if not moved:
            # this grain is stuck, so move on to the next
            count += 1
            points[(sand_x, sand_y)] = SAND
            break

print(count)
