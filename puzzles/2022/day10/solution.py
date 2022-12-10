cycles_of_interest_list = [20, 60, 100, 140, 180, 220]
cycles_of_interest = set(cycles_of_interest_list)
for c in cycles_of_interest_list:
    cycles_of_interest.add(c+1)

x = 1
cycle = 0
total = 0

# part 2
grid = [[' ']*40 for _ in range(6)]

def print_grid():
    global cycle, x
    print('grid for cycle {} with x={}'.format(cycle, x))
    for r in grid:
        for c in r:
            print(c, end='')
        print()
    print()

def row_col(val):
    return val//40, val%40

def inc_cycle():
    global grid, cycle, x
    r, c = row_col(cycle)
    print('rc:', r, c)
    has_sprite = False
    for k in [x-1, x, x+1]:
        if k < 0:
            continue
        sprite_pos = row_col(k)[1]
        if c == sprite_pos:
            has_sprite = True
            break
    grid[r][c] = '#' if has_sprite else '.'
    cycle += 1
    print_grid()

with open('input.txt') as f:
    for i, line in enumerate(f.read().splitlines()):
        splits = line.split(' ')
        add_val = 0
        if splits[0] == 'noop':
            inc_cycle()
        else:
            # addx
            add_val = int(splits[1])
            inc_cycle()
            inc_cycle()
        if cycle in cycles_of_interest:
            # round cycle down to even number
            total += x * (cycle//2)*2
        x += add_val

print(total)
