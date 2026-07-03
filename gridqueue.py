from queue import PriorityQueue
from grid import Grid
from itertools import count

class GridQueue:
    def __init__(self):
        self.pq = PriorityQueue()
        self.counter = count()

    def put(self,fn,g,grid: Grid):
        self.pq.put((fn,next(self.counter),g,grid))

    def get(self) -> tuple[float,int,Grid]:
        fn,_,g,grid = self.pq.get()
        return fn,g,grid
    
    def not_empty(self) -> bool:
        return not self.pq.empty()
