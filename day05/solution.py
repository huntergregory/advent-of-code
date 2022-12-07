from collections import deque

stacks = []
with open('day05/input.txt') as f:
    lines = f.read().splitlines()
    num_stacks = (len(lines[0])+1) // 4
    for _ in range(num_stacks):
        stacks.append(deque())

    for i, line in enumerate(lines):
        if line[0:2] == ' 1':
            break
        if len(line) != 4*num_stacks-1:
            raise ValueError('unexpected line length for line {}. expected {}, got {}.'.format(i, 4*num_stacks-1, len(line)))
        for j in range(num_stacks):
            item = line[j*4:(j+1)*4]
            if item.strip() == '':
                continue
            stacks[j].appendleft(item[1:2])
    
    start_index = i+2
    print('starting on line: {}'.format(lines[start_index]))
    for i in range(start_index, len(lines)):
        line = lines[i].split(' ')
        amt = int(line[1])
        src = int(line[3])-1
        dst = int(line[5])-1
        
        if len(stacks[src]) < amt:
            raise ValueError('stack {} does not have enough items. have {}, need {}'.format(src, len(stacks[src]), amt))
        
        # part 1
        # for _ in range(amt):
        #     item = stacks[src].pop()
        #     stacks[dst].append(item)

        # part 2
        items = []
        for _ in range(amt):
            item = stacks[src].pop()
            items.append(item)
        items.reverse()
        for item in items:
            stacks[dst].append(item)

result = ''
for s in stacks:
    result += s.pop()
print('containers on top at finish: {}'.format(result))
