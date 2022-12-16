class Node:
    def __init__(self, name, flow_rate, neighbors) -> None:
        self.name = name
        self.flow_rate = flow_rate
        self.neighbors = neighbors
    
    def __str__(self) -> str:
        return '<name: {}. fr: {}. neighbors: {}>'.format(self.name, self.flow_rate, self.neighbors)

graph = {}
with open('inputs/input.txt') as f:
    for i, line in enumerate(f.read().splitlines()):
        src_valve = line[6:8]
        flow_str = line.split('rate=')[1].split(';')[0]
        dst_valves = line[line.find('valve'):]
        dst_valves = dst_valves[dst_valves.find(' ')+1:].split(', ')
        graph[src_valve] = Node(src_valve, int(flow_str), set(dst_valves))
        # for d in dst_valves:
        #     if d not in graph:
        #         graph[d] = Node(d, -1, set())

# for v in graph.values():
#     print(v)

## SOLUTION
start_valve = 'AA'

START_TIME = 30
DEBUG = False
PATH_DELIM = '->'

def dprint(s):
    if DEBUG:
        print(s)


# without visited, takes exponential time. For t=20, takes >> 155M iterations and 5m
# with visited, takes 1.5M iterations and 4s
visited = set()
max_pressure = 0
best_path = None
steps = 0
def drain(valve_name, t, total_flow, pressure, path):
    global visited, max_pressure, best_path, steps
    dprint('valve={}. t={}. flow={}. pressure={}, path={}'.format(valve_name, t, total_flow, pressure, path))

    steps += 1
    if steps%1_000_000 == 0:
        print(steps)

    if t == 0:
        if pressure > max_pressure:
            max_pressure = pressure
            best_path = path
            dprint('t=0 for path {}. max pressure now: {}'.format(path, max_pressure))
        return

    t -= 1
    pressure += total_flow

    visited.add(valve_name)

    valve = graph[valve_name]
    for neighbor_name in valve.neighbors:
        if neighbor_name in visited:
            continue
        new_path = path + PATH_DELIM + neighbor_name
        dprint('assessing {}. adding neighbor {}. t={}. flow={}. pressure={}. path={}'.format(valve_name, neighbor_name, t, total_flow, pressure, new_path))
        drain(neighbor_name, t, total_flow, pressure, new_path)
        dprint('finished assessing {}. adding neighbor {}. t={}. flow={}. pressure={}. path={}'.format(valve_name, neighbor_name, t, total_flow, pressure, new_path))

    if valve.flow_rate > 0:
        old_flow = valve.flow_rate
        valve.flow_rate = 0
        old_visited = visited
        visited = {valve_name}

        new_path = path + PATH_DELIM + 'OPEN({})'.format(old_flow)
        dprint('starting valve={}. t={}. flow={}. pressure={}, path={}'.format(valve_name, t, total_flow+old_flow, pressure, new_path))
        drain(valve_name, t, total_flow+old_flow, pressure, new_path)
        dprint('finished valve={}. t={}. flow={}. pressure={}, path={}'.format(valve_name, t, total_flow+old_flow, pressure, new_path))

        visited = old_visited
        valve.flow_rate = old_flow

    visited.remove(valve_name)

print('starting drain at {}'.format(start_valve))
drain(start_valve, START_TIME, 0, 0, start_valve)

print()
print('for initial max time: {}...'.format(START_TIME))
print('max pressure: {}. path: {}'.format(max_pressure, best_path))
print('total iterations: {}'.format(steps))


# new ideas
# what about this case:
# 1, 1, 1, 1, 1, 999
# should not open any. should get to 999 first
# but if there are < 6 minutes left, should open each 1 valve
