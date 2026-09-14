def printgrid(grid):
    for row in grid:
        print(row)

class Node:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.parent = None

    def __str__(self):
        return f"Node {self.row} {self.col} (parent: {self.parent})"

def bfs(grid, start, goal, debug=False):
    queue = []
    root = Node(start[0],start[1])
    grid[start[0]][start[1]] = 2 # Explored
    queue.append(root) # Add to queue
    while len(queue) != 0:
        v = queue.pop(0) # Dequeue
        printgrid(grid)
        print("v node", v)

if __name__ == "__main__":
    maze = [[0,1,0,0,0,0],
            [0,1,0,0,0,0],
            [0,1,1,1,1,1],
            [0,1,0,0,1,0],
            [0,1,1,0,1,0],
            [0,0,0,0,0,0]
           ]
    bfs(maze, (0,1), (2,5))
    #floodfill(grid,1,1,2,debug=True)

