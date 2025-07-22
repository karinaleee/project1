#!/usr/bin/env python3
import sys
import heapq
from collections import deque

#global
grid = []
rows = 0
cols = 0
nodes_expand = 0
nodes_gen = 0

def read_file(filename):

    global grid, rows, cols
    with open(filename) as f:  #
        cols = int(f.readline().strip()) # open file and read
        rows = int(f.readline().strip())
        grid = []
        for _ in range(rows):
            line = f.readline().rstrip("\n")
         
            if len(line) < cols:
                line = line.ljust(cols, '_') # empty 
            elif len(line) > cols:
                line = line[:cols]
            grid.append(list(line))

    start = None
    dirty = set()
    for row in range(rows): 
        for col in range(cols):
            if grid[row][col] == '@': #starting location
                start = (row, col)
                grid[row][col] = '_'       # clear to start
            elif grid[row][col] == '*':   #dirty cell 
                dirty.add((row, col))

    return start, frozenset(dirty) # using a built in set -- can't alter [do not want it to change]


def uniform_cost_search(start, dirty): # using a priority queue
   
    global nodes_gen, nodes_expand
    front = []
    order = 0
    initial = (start[0], start[1], dirty)
   
    heapq.heappush(front, (0, order, initial, []))
    best_path = {initial: 0}
    nodes_gen = 1
    nodes_expand = 0

    moves = [('N',(-1,0)), ('S',(1,0)), ('E',(0,1)), ('W',(0,-1))]

    while front:
        cost, _, (row, col, dirt), path = heapq.heappop(front)
       
        if best_path.get((row,col,dirt), float('inf')) < cost:
            continue

        nodes_expand += 1

    
        if not dirt:
            return path

        if (row, col) in dirt:  #priority queue 
            new_dirt = set(dirt) # copy to remove 
            new_dirt.remove((row,col))
            new_state = (row, col, frozenset(new_dirt)) #new unchangeable set w removed cell 
            new_cost = cost + 1
            if new_cost < best_path.get(new_state, float('inf')): #if cheaper do this
                order += 1
                best_path[new_state] = new_cost
                heapq.heappush(front, (new_cost, order, new_state, path + ['V']))
                nodes_gen += 1

    
        for dir, (row_over, col_over) in moves: #check neighbors
            new_row, new_col = row + row_over, col + col_over
            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] != '#': #check neighbors
                new_state = (new_row, new_col, dirt)
                new_cost = cost + 1
                if new_cost < best_path.get(new_state, float('inf')):
                    order += 1
                    best_path[new_state] = new_cost
                    heapq.heappush(front, (new_cost, order, new_state, path + [dir]))
                    nodes_gen += 1

    return None


def depth_first_search(start, dirty):

    global nodes_gen, nodes_expand
    stack = [ (start[0], start[1], dirty, []) ]
    visited = { (start[0], start[1], dirty) }
    nodes_gen = 1
    nodes_expand = 0

    moves = [('N',(-1,0)), ('S',(1,0)), ('E',(0,1)), ('W',(0,-1))]

    while stack:
        row, col, dirt, path = stack.pop()
        nodes_expand += 1

        if not dirt:
            return path

    
        if (row, col) in dirt:  #stack implementation for DFS
            new_dirt = set(dirt) #copy to remove 
            new_dirt.remove((row,col)) 
            new_state = (row, col, frozenset(new_dirt)) #new unchangeable set w remove cell
            
            if new_state not in visited:
                visited.add(new_state)
                stack.append((row, col, frozenset(new_dirt), path + ['V']))
                nodes_gen += 1

        for dir, (row_over, col_over) in moves: #checking all possible dir
            new_row, new_col = row + row_over, col + col_over
            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] != '#': #need to check the neighbors
                new_state = (new_row, new_col, dirt)
                if new_state not in visited: 
                    visited.add(new_state) #push to stack if has not been seen yet 
                    stack.append((new_row, new_col, dirt, path + [dir]))
                    nodes_gen += 1 

    return None


def main(): #call arguments in terminal 
    algo_name = sys.argv[1] #args to call
    world = sys.argv[2]

    start, dirty = read_file(world)

    if algo_name == 'uniform-cost': #arg to call using uniform cost 
        plan = uniform_cost_search(start, dirty)
    else: 
        algo_name == 'depth-first' #call dfs
        plan = depth_first_search(start, dirty)

    # node number output 
    for nodes in plan:
        print(nodes)
    print(f"{nodes_gen} nodes generated") #print statements for the node info 
    print(f"{nodes_expand} nodes expanded")


if __name__ == "__main__":
    main()
