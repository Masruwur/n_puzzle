from grid import Grid
import math
from copy import deepcopy

class HeuristicCalculator:
    def __init__(self,grid: Grid,mode: str = "linear_conflict",W=1.0):
         self.grid = grid
         self.mode = mode
         if W < 1.0:
             raise ValueError("Weight cannot be less than 1.0")
         self.W = W

    def setGrid(self,grid: Grid):
        self.grid = grid
    
    def targetPosition(self,val):
        n = self.grid.n

        if val == 0:
            return n-1,n-1

        x = (val-1)//n
        y = (val-1)%n   #(x,y) is the ideal co-ord

        return x,y
    
    def targetValue(self,posX,posY):
        if posX == posY and posX == self.grid.n-1:
            return 0

        return posX*self.grid.n + posY + 1
    
    


    def hammingDistance(self):
        n = self.grid.n
        count = 0
        for i in range(n):
            for j in range(n):
                val = self.grid.rows[i][j] 
                if val !=0 and val != n*i + j + 1:
                    count += 1
        
        return count
    
    def manhattanDistance(self):
        n = self.grid.n
        dist = 0

        for i in range(n):
            for j in range(n):
                val = self.grid.rows[i][j]
                if val==0:
                    continue

                x,y = self.targetPosition(val)
                dist += abs(x-i) + abs(y-j)

        return dist 
    
    def euclidianDistance(self):
        n = self.grid.n
        dist = 0

        for i in range(n):
            for j in range(n):
                val = self.grid.rows[i][j]
                if val==0:
                    continue

                x,y = self.targetPosition(val)
                dist += math.sqrt((x-i)**2 + (y-j)**2)

        return dist 
    
    def linearConflict(self):
        n = self.grid.n
        count = 0

        for k in range(n):
            for i in range(n):
                val = self.grid.rows[k][i]
                if val == 0:
                    continue
                x,y = self.targetPosition(val)
                if x != k:
                    continue

                for j in range(i+1,n):
                    val_n = self.grid.rows[k][j]
                    x_n,y_n = self.targetPosition(val_n)

                    if x_n != k:
                        continue

                    if y > y_n:
                        count += 1

        for k in range(n):
            for i in range(n):
                val = self.grid.rows[i][k]
                if val == 0:
                    continue
                x,y = self.targetPosition(val)
                if y != k:
                    continue

                for j in range(i+1,n):
                    val_n = self.grid.rows[j][k]
                    x_n,y_n = self.targetPosition(val_n)

                    if y_n != k:
                        continue

                    if x > x_n:
                        count += 1

            
            return self.manhattanDistance() + 2*count


    # custom heuristic impl 
    def gaschnig(self):
        n = self.grid.n
        currPos = {}
        rows = deepcopy(self.grid.rows)
        count = 0

        for i in range(n):
            for j in range(n):
                value = rows[i][j]
                currPos[value] = (i,j)

        blankTarget = self.targetPosition(0)

        
        while True:
            isSolved = True
            misplaced = None
            for i in range(n):
                if isSolved:
                    for j in range(n):
                        if rows[i][j] != self.targetValue(i,j):
                            misplaced = rows[i][j]
                            isSolved = False
                            break 
            
            if isSolved:
                break

            
            if currPos[0] != blankTarget:
                targetVal = self.targetValue(currPos[0][0],currPos[0][1])
                targetPos = currPos[targetVal]

                r1,c1 = currPos[0]
                r2,c2 = targetPos

                rows[r1][c1],rows[r2][c2] = rows[r2][c2],rows[r1][c1]

                currPos[targetVal] = currPos[0]
                currPos[0] = targetPos

            else:
                r1,c1 = currPos[0]
                r2,c2 = currPos[misplaced]

                rows[r1][c1],rows[r2][c2] = rows[r2][c2],rows[r1][c1]

                currPos[misplaced] = currPos[0]
                currPos[0] = (r2,c2)

            count += 1

        return count
               

    def getHeuristic(self):
        mode = self.mode
        W = self.W

        if mode == "linear_conflict":
            return self.linearConflict()*W
        if mode == "manhattan":
            return self.manhattanDistance()*W
        if mode == "euclidian":
            return self.euclidianDistance()*W
        if mode == "hamming":
            return self.hammingDistance()*W
        if mode == "custom":
            return self.gaschnig()*W

        else:
            raise ValueError("Invalid Heuristic type")
        

        

if __name__ == '__main__':
    pass
