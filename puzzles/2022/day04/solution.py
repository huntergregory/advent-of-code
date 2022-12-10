# checks if ab1 contains ab2
def contains(ab1, ab2):
    a1, b1 = ab1
    a2, b2 = ab2
    return a1 <= a2 and b1 >= b2

def overlaps(ab1, ab2):
    a1, b1 = ab1
    a2, b2 = ab2
    if a1 <= a2:
        return b1 >= a2
    return b2 >= a1

contain_count = 0
overlap_count = 0
with open('input.txt') as f:
    for i, line in enumerate(f.read().splitlines()):
        elves = line.split(",")
        e1 = [int(x) for x in elves[0].split("-")]
        e2 = [int(x) for x in elves[1].split("-")]

        # part 1
        contain_count += contains(e1, e2) or contains(e2, e1)

        # part 2
        overlap_count += overlaps(e1, e2)

print('contained: {}'.format(contain_count))
print('overlapping: {}'.format(overlap_count))
