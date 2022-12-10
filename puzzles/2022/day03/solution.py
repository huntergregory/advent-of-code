import string

priorities = {}
for i, letter in enumerate(string.ascii_lowercase):
    priorities[letter] = i+1
    priorities[letter.upper()] = i+1+26

# part 1
duplicates = []
with open('input.txt') as f:
    for i, line in enumerate(f.read().splitlines()):
        compartment_size = len(line) // 2
        compartment1 = {x for x in line[:compartment_size]}
        for x in line[compartment_size:]:
            if x in compartment1:
                duplicates.append(x)
                break

duplicate_priorities = [priorities[d] for d in duplicates]
print('sum of duplicate type priorities: {}'.format(sum(duplicate_priorities)))

# part 2
badges = []
with open('input.txt') as f:
    lines = f.read().splitlines()
    i = 0
    while i < len(lines):
        common_items = {x for x in lines[i]}
        i += 1
        for _ in range(2):
            common_items.intersection_update({x for x in lines[i]})
            i += 1
        for x in common_items:
            badges.append(x)
            break # unnecessary since there will only be one common item

badge_priorities = [priorities[b] for b in badges]
print('sum of badge priorities: {}'.format(sum(badge_priorities)))
