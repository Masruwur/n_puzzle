from gridqueue import GridQueue
from grid import Grid,inputGrid
from heuristics import HeuristicCalculator


HEURISTIC_MODE = "linear_conflict"
WEIGHT = 1.0


def stateToStr(state: tuple) -> str:
    st = ""
    for row in state:
        row_st = " ".join(map(str,row))
        st += row_st + "\n"
    return st 


def solve_puzzle(grid: Grid,hc: HeuristicCalculator):
    
    if grid.canBeSolved() == False:
        print("Unsolvable Puzzle")
        return (None,{},0)
    
    gq = GridQueue()
    gs = set()
    path = {}
    gScore = {}

    init_state = grid.getState()
    path[init_state] = None
    gScore[init_state] = 0
    fn = hc.getHeuristic() #gn=0 initially

    gq.put(fn,0,grid)
    nodes_explored = 0

    while gq.not_empty() == True:
        _,g,curr = gq.get()

        state = curr.getState()
        if state in gs:
            continue

        gs.add(state)

        if curr.isSolved():
            return curr.getState(),path,nodes_explored
        
        ngrids = curr.generateNeighbours()
        nodes_explored +=1

        for ngrid in ngrids:
            child_state = ngrid.getState()
            if child_state not in gScore or gScore[child_state] > g+1:
                 gScore[child_state] = g+1
                 hc.setGrid(ngrid)
                 gq.put(g+1+hc.getHeuristic(),g+1,ngrid)
                 path[child_state] = state


           

    
if __name__ == "__main__":
    grid = inputGrid()
    hc = HeuristicCalculator(grid,HEURISTIC_MODE,WEIGHT)
    state,path,_ = solve_puzzle(grid,hc)
    if state is None:
        exit(0)

    moves = []

    count = -1
    while state is not None:
        count += 1
        moves.insert(0,stateToStr(state))
        state = path[state]


    print(f'Minimum number of moves = {count}')
    print()

    for move in moves:
        print(move)



