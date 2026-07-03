from copy import deepcopy

class Grid:
    def __init__(self,n):
        self.n = n
        self.rows = []
        for i in range(n):
            row = [0]*n
            self.rows.append(row)

    def __str__(self):
        st = ""
        for row in self.rows:
            row_st = " ".join(map(str,row))
            st += row_st + "\n"

        return st 
    
    def setState(self,data: list):
        self.rows = data

    def getEmpty(self):
        for i,row in enumerate(self.rows):
            if 0 in row:
                j = row.index(0)
                return i,j
    
    def generateNeighbours(self) ->list[Grid]:
        i,j = self.getEmpty()

        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        neighbours = []

        for di,dj in directions:
            ni = i + di
            nj = j + dj

            if ni < 0 or ni >= self.n:
                continue
            if nj <0 or nj >= self.n:
                continue

            ngrid = Grid(self.n)
            nrows = deepcopy(self.rows)
            nrows[i][j],nrows[ni][nj] = nrows[ni][nj],nrows[i][j]
            ngrid.setState(nrows)

            neighbours.append(ngrid)

        return neighbours


    def isSolved(self) ->bool:
        n = self.n
        rows = self.rows
        if rows[n-1][n-1] != 0:
            return False

        for i in range(n):
            for j in range(n):
                val = rows[i][j]
                if val != 0 and val != i*self.n + j + 1:
                    return False
                
        return True
    

    def canBeSolved(self) ->bool:
        inversions = countInversions(self)
        if self.n % 2 == 1:
            return (inversions%2 == 0)
        
        i,_ = self.getEmpty()
        row_height = self.n-i

        return (inversions + row_height)%2 == 1
    
    def getState(self):
        return tuple(tuple(row) for row in self.rows)
    

    
        



def inputGrid() ->Grid:
    n = int(input("Enter grid size: "))
    grid = Grid(n)
    print("Enter grid:")
    rows = []

    for i in range(n):
        row = list(map(int,input("").split(" ")))
        rows.append(row)

    if not verifyGrid(n,rows):
        raise ValueError("invalid values in grid")
    grid.setState(rows)
    return grid

def verifyGrid(n: int, rows: list) ->bool:
    value_map = {}
    for i in range(n**2):
        value_map[i] = False

    for row in rows:
        for val in row:
            try:
                value_map[val] = True
            except:
                raise ValueError("Entry out of bounds")
            
    for val in value_map.values():
        if not val:
            return False

    print("")  
    return True

def countInversions(grid: Grid):
    row_major = []
    for row in grid.rows:
        row_major += row

    count = 0
    n = len(row_major)

    for i in range(n):
        if row_major[i] == 0:
            continue
        for j in range(i+1,n):
            if row_major[i] > row_major[j] and row_major[j]!=0:
                count +=1

    return count

            


if __name__ == '__main__':
    grid = inputGrid()
    print(grid.getState())
    
      





            