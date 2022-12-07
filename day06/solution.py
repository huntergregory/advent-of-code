NUM_DISTINCT = 14

with open('input.txt') as f:
    line = f.read().splitlines()[0]

i = NUM_DISTINCT-1
while i < len(line):
    good = True
    # ensure there are NUM_DISTINCT letters
    marker_pool = {line[i]}
    for j in range(i-1, i-NUM_DISTINCT, -1):
        if line[i] == line[j]:
            # optimize by jumping ahead if we find where there's duplication
            # for a 2.7MB file, this drops runtime from 5.2 seconds to 0.7 seconds
            i = j+NUM_DISTINCT
            good = False
            break
        marker_pool.add(line[j])
    if good:
        if len(marker_pool) == NUM_DISTINCT: 
            break
        # there's a non-unique letter somewhere, but we're not sure where, so look at the next letter
        i += 1
if i >= len(line):
    raise ValueError('end of line')

# 2823 for original input
print('marker received at character {}'.format(i+1))