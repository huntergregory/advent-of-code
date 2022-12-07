class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = {}
        self.children_size = 0
        self.direct_size = 0
    
    def full_size(self):
        return self.direct_size + self.children_size

root = Dir('/', None)
head = root
with open('day07/input.txt') as f:
    lines = f.read().splitlines()
    i = 1
    while i < len(lines):
        if lines[i] == '$ ls':
            i += 1
            while i < len(lines):
                if lines[i][0] == '$':
                    break
                if lines[i][:4] == 'dir ':
                    name = lines[i][4:]
                    child = Dir(name, head)
                    head.children[name] = child
                else:
                    head.direct_size += int(lines[i].split(' ')[0])
                i += 1
        else:
            # line like '$ cd DIR'
            to_dir = lines[i].split(' ')[2]
            if to_dir == '..':
                head = head.parent
                if head is None:
                    raise Exception('nil parent')
            else:
                head = head.children[to_dir]
            i += 1

def assign_children_size(node):
    if len(node.children) == 0:
        return node.direct_size
    for c in node.children.values():
        node.children_size += assign_children_size(c)
    return node.full_size()

def sum_dirs(node):
    my_size = node.full_size()
    if my_size > 100_000:
        my_size = 0
    return my_size + sum([sum_dirs(c) for c in node.children.values()])

assign_children_size(root)
print('sum of directory sizes < 100k: {}'.format(sum_dirs(root)))

# part 2
current_usage = 70_000_000 - root.full_size()
to_delete = 30_000_000 - current_usage
print('need to free up this much space: {}'.format(to_delete))

def find_min(node, current_min):
    min_node = None
    for c in node.children.values():
        min_child, val = find_min(c, current_min)
        if val < current_min:
            min_node = min_child
            current_min = val

    if node.full_size() >= to_delete and node.full_size() < current_min:
        return node, node.full_size()

    return min_node, current_min

min_node, _ = find_min(root, 999_999_999)
print('smallest directory to delete: {} {}'.format(min_node.full_size(), min_node.name))
    