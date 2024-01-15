import pandas as pd


def sudokuCheck(grid):    
    if not grid:
        return False
    
    #rows by rows checking 
    hset = set()
    for i in range(9):
        for j in range(9):
            if grid[i][j] in hset:
                return False
            else:
                hset.add(grid[i][j])
        hset = set()
            
    #cols by cols checking
    hset = set()
    for i in range(9):
        for j in range(9):
            if grid[j][i] in hset:
                return False
            else:
                hset.add(grid[j][i])
        hset = set()
    
    
    #3 by 3 check    
    subs = [range(0,3), range(3,6), range(6,9)]    
    subgrids = [] 
    for x in subs:
        for y in subs:
            subgrids.append([x,y])   
            
    for (row_range, column_range) in subgrids:
        hset = set()
        for i in row_range:
            for j in column_range:              
                if grid[i][j] in hset:
                    return False
                else:
                    hset.add(grid[i][j])
    
    return True


def find_easy(grid):
    found = False
    for row_i in range(9):
        for col_i in range(9):
            if grid[row_i][col_i]==0:
                #input()
                column = [grid[i][col_i] for i in range(len(grid))]
                
                subgrid_row_start = 3 * (row_i // 3)
                subgrid_col_start = 3 * (col_i // 3)
                sub_grid = [
                    grid[i][subgrid_col_start:subgrid_col_start + 3]
                    for i in range(subgrid_row_start, subgrid_row_start + 3)
                ]
                flat_sub_grid = [value for row in sub_grid for value in row]
                
                
                #check 0s in row
                if pd.Series(grid[row_i]).value_counts()[0] == 1:
                    x = set(range(1,10))-set(grid[row_i])
                    grid[row_i][col_i]=list(x)[0]
                    print("found",row_i,col_i,list(x)[0])
                    found=True
                    continue
                
                
                #check 0s in col
                elif pd.Series(column).value_counts()[0] == 1:
                    x = set(range(1,10))-set(column)
                    grid[row_i][col_i]=list(x)[0]
                    print("found",row_i,col_i,list(x)[0])
                    found=True
                    continue
                
                #check 0s in subgrid
                elif pd.Series(flat_sub_grid).value_counts()[0] == 1:
                    x = set(range(1,10))-set(flat_sub_grid)
                    grid[row_i][col_i]=list(x)[0]
                    print("found",row_i,col_i,list(x)[0])
                    found=True
                    continue
                
    return found
                    
                
        
        
        
        
        
        


from sudoku import Sudoku
puzzle = Sudoku(3).difficulty(0.2)
orig_grid = [[0 if element is None else element for element in row] for row in puzzle.board]



sudokuCheck(orig_grid)

while True:
    if not find_easy(orig_grid):
        break

    print(orig_grid)
print(orig_grid)

