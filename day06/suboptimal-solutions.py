# for a 2.7MB file, this approach takes 5.2 seconds without the optimization
# and 0.7 seconds with the optimization
i = NUM_DISTINCT-1
while i < len(line):
    good = True
    # ensure there are NUM_DISTINCT letters
    marker_pool = {line[i]}
    for j in range(i-1, i-NUM_DISTINCT, -1):
        if line[i] == line[j]:
            # optimize by jumping ahead if we find where there's duplication
            i = j+NUM_DISTINCT
            good = False
            break
        marker_pool.add(line[j])
    if good:
        if len(marker_pool) == NUM_DISTINCT: 
            break
        # there's a non-unique letter somewhere, but we're not sure where, so look at the next letter
        i += 1

# this approach takes 3.0 seconds for the 2.7MB file
i = 0
markers = []
while i < len(line):
    good = True
    for j, l in enumerate(markers):
        if l == line[i]:
            bad_index = j
            new_markers = [markers[k] for k in range(j+1, len(markers))]
            good = False
            break
    if not good:
        markers = new_markers
    markers.append(line[i])
    if len(markers) == NUM_DISTINCT:
        break
    i += 1
