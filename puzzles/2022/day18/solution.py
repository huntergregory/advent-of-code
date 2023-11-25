import numpy as np

# 3d points implemented as a map of maps of sets
points = {}
mins = [999999999999999] * 3
maxs = [-999999999999999] * 3
with open('inputs/input.txt') as f:
    for line in f.read().splitlines():
        x, y, z = [int(k) for k in line.split(',')]
        if x not in points:
            points[x] = {}
        if y not in points[x]:
            points[x][y] = set()
        points[x][y].add(z)

        mins[0] = min(mins[0], x)
        maxs[0] = max(maxs[0], x)
        mins[1] = min(mins[1], y)
        maxs[1] = max(maxs[1], y)
        mins[2] = min(mins[2], z)
        maxs[2] = max(maxs[2], z)

## part 1 (space-efficient using maps/sets)
deltas = [
    [1,0,0],
    [-1,0,0],
    [0,1,0],
    [0,-1,0],
    [0,0,1],
    [0,0,-1],
]
exposed_surfaces = 0
for x, all_y in points.items():
    for y, all_z in all_y.items():
        for z in all_z:
            neighbors = 0
            for d_x, d_y, d_z in deltas:
                x_new = x + d_x
                y_new = y + d_y
                z_new = z + d_z
                if x_new in points and y_new in points[x_new] and z_new in points[x_new][y_new]:
                    neighbors += 1
            exposed_surfaces += 6 - neighbors

print('exposed surfaces: {}'.format(exposed_surfaces))

## part 2 (array-based)
LAVA = 1
AIR_BUBBLE = 2
EXTERNAL_AIR = 3

# grid/array representation
shape=(maxs[0]-mins[0]+1, maxs[1]-mins[1]+1, maxs[2]-mins[2]+1)
grid = np.zeros(shape=shape)
for x, all_y in points.items():
    for y, all_z in all_y.items():
        for z in all_z:
            grid[x - mins[0]][y - mins[1]][z - mins[2]] = LAVA

def out_of_bounds(x, y, z):
    return x < 0 or y < 0 or z < 0 or x >= grid.shape[0] or y >= grid.shape[1] or z >= grid.shape[2]

# marking air bubbles and external air
visited = set()
for x in range(grid.shape[0]):
    for y in range(grid.shape[1]):
        for z in range(grid.shape[2]):
            if grid[x,y,z] == LAVA or (x,y,z) in visited:
                continue

            # expand the whole section of air, tracking whether you hit a wall (in which case the section is not an air bubble)
            hit_wall = False
            candidates = []
            stack = [(x,y,z)]
            while len(stack) > 0:
                xyz = stack.pop()
                visited.add(xyz)
                candidates.append(xyz)

                x, y, z = xyz
                for d_x, d_y, d_z in deltas:
                    x_new = x + d_x
                    y_new = y + d_y
                    z_new = z + d_z

                    if out_of_bounds(x_new, y_new, z_new):
                        hit_wall = True
                        continue
                    
                    if grid[x_new,y_new,z_new] == LAVA:
                        continue

                    xyz_new = (x_new, y_new, z_new)
                    if xyz_new in visited:
                        continue

                    stack.append(xyz_new)
            
            for x, y, z in candidates:
                grid[x,y,z] = EXTERNAL_AIR if hit_wall else AIR_BUBBLE

# visualization
print('LAYERS:')
for z in range(grid.shape[2]):
    for x in range(grid.shape[0]):
        print('|', end='')
        for y in range(grid.shape[1]):
            c = '?'
            if grid[x,y,z] == LAVA:
                c = 'O'
            elif grid[x,y,z] == AIR_BUBBLE:
                c = '.'
            elif grid[x,y,z] == EXTERNAL_AIR:
                c = ' '
            print(c, end='')
        print('|')
    print()

# how many surfaces from before were touching air bubbles?
surfaces_touching_air_bubbles = 0
for x in range(grid.shape[0]):
    for y in range(grid.shape[1]):
        for z in range(grid.shape[2]):
            if grid[x,y,z] != LAVA:
                continue

            for d_x, d_y, d_z in deltas:
                x_new = x + d_x
                y_new = y + d_y
                z_new = z + d_z
                if out_of_bounds(x_new, y_new, z_new):
                    continue

                if grid[x_new,y_new,z_new] == AIR_BUBBLE:
                    surfaces_touching_air_bubbles += 1

print('water-exposed surfaces: {}'.format(exposed_surfaces - surfaces_touching_air_bubbles))
