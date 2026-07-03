from grid import Grid
from heuristics import HeuristicCalculator
from puzzle import solve_puzzle

HEURISTIC_MODE = "linear_conflict"
WEIGHTS = (1.0, 1.2, 2.0, 5.0)

grids = []
with open("cases.txt",'r') as input:
    for i in range(10):
        rows = []

        for j in range(4):
            line: str = input.readline()
            row = [int(num) for num in line.strip().split()]
            rows.append(row)

        grid = Grid(4)
        grid.setState(rows)
        grids.append(grid)

        input.readline()

with open("data.txt",'w') as output:
    for i,grid in enumerate(grids):
        print(f'processing grid no. {i+1} ')
        print(f'Grid no. {i+1}',file=output)
        print(file=output)
        print(grid,file=output)
        print(file=output)
        print("-----------------",file=output)
        for w in WEIGHTS:
            hc = HeuristicCalculator(grid,W=w)
            state,path,nodes = solve_puzzle(grid,hc)

            count = -1
            while state is not None:
                count += 1
                state = path[state]

            print(f'Weight = {w}',file=output)
            print(f'Minimum number of moves = {count}',file=output)
            print(f'Number of nodes explored = {nodes}',file=output)
            print("--------------------------------------",file=output)
        
        print(file=output)



