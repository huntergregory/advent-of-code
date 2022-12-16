import numpy as np

# from "x=NUM, y=NUM" to numpy coordinates
def point_to_xy(p):
    xy = p.split(', ')
    x = int(xy[0][2:])
    y = int(xy[1][2:])
    return np.array([x, y], dtype=int)

def manhattan(a, b):
    return sum(np.abs(a - b))

beacons = []
sensors = []
with open('input.txt') as f:
    lines = f.read().splitlines()
    for i, line in enumerate(lines):
        line = line[10:]
        sensor_beacon = line.split(': closest beacon is at ')
        sensors.append(point_to_xy(sensor_beacon[0]))
        beacons.append(point_to_xy(sensor_beacon[1]))

# part 2 range
region_low = 0
region_high = 4_000_000
for y in range(region_high):
    # part 1 can just set y = 2_000_000
    if y%50_000 == 0:
        print('at y: {}'.format(y))
    x_boundaries = []
    for beacon, sensor in zip(beacons, sensors):
        d = manhattan(beacon, sensor)

        y_diff = y - sensor[1]
        if abs(y_diff) > d:
            continue

        x_diff = d - abs(y_diff)
        
        x_low = sensor[0]-x_diff
        x_high = sensor[0]+x_diff
        
        # part 2 only
        x_low = max(region_low, x_low)
        x_high = min(region_high, x_high)

        loc = (x_low, x_high)
        x_boundaries.append(loc)

    x_boundaries.sort()

    # part 1
    # total = 0
    # max_x = x_boundaries[0][0]
    
    # part 2
    max_x = region_low
    done = False

    for b in x_boundaries:
        if b[1] <= max_x:
            continue

        # part 2
        x_prime = max_x+1
        if b[0] > x_prime:
            # value is (2740279, 2625406). Frequency is 10961118625406
            print('value is ({}, {}). Frequency is {}'.format(x_prime, y, y+(x_prime)*region_high))
            done = True
            break

        # part 1
        # b_sum = max(0, b[0] - max_x) + b[1] - max_x
        # total += b_sum

        # both parts
        max_x = b[1]

    # part 2
    if done:
        break

    # part 1
    # number of positions without beacons: 4582667
    # print('number of positions without beacons: {}'.format(total))
