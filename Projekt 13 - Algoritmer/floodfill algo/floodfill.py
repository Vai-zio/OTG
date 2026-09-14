def printgrid(grid):
    for row in grid:
        print(row)


def floodfill(grid, row, col, value, debug=False):
    org_val = grid[row][col]
    grid[row][col] = value
    if debug:
        print(f"# floodfill(grid,{row},{col},{value})")
        printgrid(grid)
        print()

    """
    try:
        if grid[row+1][col] == org_val:
            floodfill(grid, row+1,col,value,debug=debug)
    except:
        return None
    try:
        if grid[row][col-1] == org_val:
            floodfill(grid, row,col-1,value,debug=debug)
    except:
        return None
    try:
        if grid[row-1][col] == org_val:
            floodfill(grid, row-1,col,value,debug=debug)
    except:
        return None
    try:
        if grid[row][col+1] == org_val:
            floodfill(grid, row,col+1,value,debug=debug)
    except:
        return None
    try:
        if grid[row+1][col+1] == org_val:
            floodfill(grid, row+1,col+1,value,debug=debug)
    except:
        return None
    try:
        if grid[row+1][col-1] == org_val:
            floodfill(grid, row+1,col-1,value,debug=debug)
    except:
        return None
    try:
        if grid[row-1][col-1] == org_val:
            floodfill(grid, row-1,col-1,value,debug=debug)
    except:
        return None
    try:
        if grid[row-1][col+1] == org_val:
            floodfill(grid, row-1,col+1,value,debug=debug)
    except:
        return None
    
    """
    try:
        if row+1 < len(grid) and col+1 < len(grid[0]) and grid[row+1][col+1] == org_val:
            floodfill(grid, row+1,col+1,value,debug=debug)
        if grid[row+1] < len(grid) and grid[row+1][col] == org_val:
            floodfill(grid, row+1,col,value,debug=debug)
        if grid[row+1]  and grid[row+1][col-1] < 0 and grid[row+1][col-1] == org_val:
            floodfill(grid, row+1,col-1,value,debug=debug)
        if grid[col-1] < 0 and grid[row][col-1] == org_val:
            floodfill(grid, row,col-1,value,debug=debug)
        if grid[row-1][col-1] < 0 and grid[row-1][col-1] == org_val:
            floodfill(grid, row-1,col-1,value,debug=debug)
        if grid[row-1] < 0 and grid[row-1][col] == org_val:
            floodfill(grid, row-1,col,value,debug=debug)
        if grid[row-1][col+1] < 0 and grid[row-1][col+1] == org_val:
            floodfill(grid, row-1,col+1,value,debug=debug)
        if grid[col+1] < 0 and grid[row][col+1] == org_val:
            floodfill(grid, row,col+1,value,debug=debug)
    except:
        return None


if __name__ == "__main__":
    grid = [[0,0,0,0,2,0],
            [0,0,0,0,2,0],
            [0,0,0,0,2,0],
            [0,0,0,0,2,0],
            [2,2,2,2,2,0],
            [0,0,0,0,0,0]
           ]
    floodfill(grid,1,1,2,debug=True)

