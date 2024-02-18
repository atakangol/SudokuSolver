import pandas as pd
import numpy as np
from sudoku import Sudoku

def sudokuCheck(grid):    
    if not grid or any(0 in row for row in grid):
        return False
    
    # Rows by rows checking 
    hset = set()
    for i in range(9):
        for j in range(9):
            if grid[i][j] in hset:
                return False
            else:
                hset.add(grid[i][j])
        hset = set()
            
    # Columns by columns checking
    hset = set()
    for i in range(9):
        for j in range(9):
            if grid[j][i] in hset:
                return False
            else:
                hset.add(grid[j][i])
        hset = set()
    
    # 3 by 3 check    
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
                    #grid[row_i][col_i]=list(x)[0]
                    #print("found",row_i,col_i,list(x)[0])
                    found=True
                    return row_i,col_i,list(x)[0]
                
                
                #check 0s in col
                elif pd.Series(column).value_counts()[0] == 1:
                    x = set(range(1,10))-set(column)
                    #grid[row_i][col_i]=list(x)[0]
                    #print("found",row_i,col_i,list(x)[0])
                    found=True
                    return row_i,col_i,list(x)[0]
                
                #check 0s in subgrid
                elif pd.Series(flat_sub_grid).value_counts()[0] == 1:
                    x = set(range(1,10))-set(flat_sub_grid)
                    #grid[row_i][col_i]=list(x)[0]
                    #print("found",row_i,col_i,list(x)[0])
                    found=True
                    return row_i,col_i,list(x)[0]
                
    return None
#grid[row_i][col_i]                    
def find_only_possible_space(grid):  
    goal = set(range(1,10))
    #grid = orig_grid.copy()  """
    for row_i in range(9):
        if 0 not in grid[row_i]:
            continue
        missing_nums = list(goal -set(grid[row_i]))
        
        
        for col_i in range(9):
            
            if grid[row_i][col_i] !=0:
                continue
            column = [grid[i][col_i] for i in range(len(grid))]
            subgrid_row_start = 3 * (row_i // 3)
            subgrid_col_start = 3 * (col_i // 3)
            sub_grid = [
                grid[i][subgrid_col_start:subgrid_col_start + 3]
                for i in range(subgrid_row_start, subgrid_row_start + 3)
            ]
            flat_sub_grid = [value for row in sub_grid for value in row]
            
            possibles = []
            for ii in missing_nums:
                if ( ii not in column) and ( ii not in flat_sub_grid):
                    possibles.append(ii)
            
            if len(possibles) == 1:
                #grid[row_i][col_i]=possibles[0]
                #print("found0",row_i,col_i,possibles[0])
                found=True
                return (row_i,col_i,possibles[0])
             
    
       
    
    for col_i in range(9):
        column = [grid[i][col_i] for i in range(len(grid))]
        if 0 not in column:
            continue
        missing_nums = list(goal- set(column) )
        
        
        for row_i in range(9):
            if grid[row_i][col_i] !=0:
                continue
            subgrid_row_start = 3 * (row_i // 3)
            subgrid_col_start = 3 * (col_i // 3)
            sub_grid = [
                grid[i][subgrid_col_start:subgrid_col_start + 3]
                for i in range(subgrid_row_start, subgrid_row_start + 3)
            ]
            flat_sub_grid = [value for row in sub_grid for value in row]
            
            possibles = []
            for ii in missing_nums:
                if ( ii not in grid[row_i]) and ( ii not in flat_sub_grid):
                    possibles.append(ii)
            
            if len(possibles) == 1:
                #grid[row_i][col_i]=possibles[0]
                #print("found1",row_i,col_i,possibles[0])
                found=True
                return (row_i,col_i,possibles[0])
            
            
    for ii,kk in np.ndindex((3,2)):
    
        subgrid_row_start = 3 * ii
        subgrid_col_start = 3 * kk
        sub_grid = [
            grid[i][subgrid_col_start:subgrid_col_start + 3]
            for i in range(subgrid_row_start, subgrid_row_start + 3)
        ]
        flat_sub_grid = [value for row in sub_grid for value in row]
        
        if 0 not in flat_sub_grid:
            continue
        missing_nums = list(goal- set(flat_sub_grid) )
        
            
            
        for row_i in range(subgrid_row_start,subgrid_row_start+3):
            for col_i in range(subgrid_row_start,subgrid_row_start+3):
                
                if grid[row_i][col_i] !=0:
                    continue
                column = [grid[i][col_i] for i in range(len(grid))]
                
                
                possibles = []
                for jj in missing_nums:
                    if ( jj not in column) and ( jj not in grid[row_i]):
                        possibles.append(jj)
                
                if len(possibles) == 1:
                    #grid[row_i][col_i]=possibles[0]
                    #print("found2",row_i,col_i,possibles[0])
                    found=True
                    return (row_i,col_i,possibles[0])
                 
              
    return None    
        



def find_possibilities(grid, row, col):
    possibilities = set(range(1, 10))  # All numbers from 1 to 9 are initially possible

    # Check the numbers in the same row and column
    for i in range(9):
        if grid[row][i] in possibilities:
            possibilities.remove(grid[row][i])
        if grid[i][col] in possibilities:
            possibilities.remove(grid[i][col])

    # Check the numbers in the 3x3 square
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] in possibilities:
                possibilities.remove(grid[i][j])

    return list(possibilities)

def find_least_possibilities(grid):
  least_possibilities = float('inf')  # Start with positive infinity
  best_candidate = None

  for i in range(9):
      for j in range(9):
          if grid[i][j] == 0:
              possibilities = find_possibilities(grid, i, j)
              num_possibilities = len(possibilities)

              if num_possibilities < least_possibilities:
                  least_possibilities = num_possibilities
                  best_candidate = (i, j, possibilities)

  return best_candidate      

def find_all_ordered_by_possibilities(grid):
    empty_spaces = []

    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                possibilities = find_possibilities(grid, i, j)
                for possibility in possibilities:
                    empty_spaces.append((i, j, possibility))

    # Sort the empty spaces based on the number of possibilities
    empty_spaces.sort(key=lambda x: len(find_possibilities(grid, x[0], x[1])))

    return empty_spaces
#find_all_ordered_by_possibilities(orig_grid)



def backtrack(all_moves,grid):
    back = all_moves.pop()
    last_move = back[1]
    ty = back[0]
    
    while True:
        if ty=='m':
            orig_grid[last_move[0]][last_move[1]] = 0
            back = all_moves.pop()
            last_move = back[1]
            ty = back[0]
            continue
        if ty=='c':
            
            last_choice = last_move.pop(0)
            orig_grid[last_choice[0]][last_choice[1]] = 0
            
            if len(last_move)==0:
                back = all_moves.pop()
                last_move = back[1]
                ty = back[0]
                continue
            
            new_move = last_move[0]
            
            
            orig_grid[new_move[0]][new_move[1]] = new_move[2]
            
            all_moves.append(('c',last_move))
            
            break
            
            
    



#back_move=[(5, 6, []), (5, 8, [1, 9]), (8, 6, [1, 9]), (8, 8, [1, 9])]


puzzle = Sudoku(3).difficulty(0.8)
orig_grid = [[0 if element is None else element for element in row] for row in puzzle.board]


sum(row.count(0) for row in orig_grid)

all_moves = []
ii=0
while not sudokuCheck(orig_grid) :
    print(ii,sum(row.count(0) for row in orig_grid))
    if sum(row.count(0) for row in orig_grid) == 0:
        #break
        print("full")
        backtrack(all_moves, orig_grid)
    ii+=1
    
    move = find_easy(orig_grid)
    if move :
        orig_grid[move[0]][move[1]] = move[2]
    
        all_moves.append(('m',move))
        
        move=None
        continue
    
    '''
    move = find_only_possible_space(orig_grid)
    
    if move :
        orig_grid[move[0]][move[1]] = move[2]
    
        all_moves.append(('m',move))
        
        move=None
        continue
    '''
    move = find_least_possibilities(orig_grid)
    if move:
        if len(move[2])==1:
            orig_grid[move[0]][move[1]] = move[2][0]
            all_moves.append(('m',(move[0],move[1],move[2][0])))

    #move = find_least_possibilities(orig_grid)
    
    
    moves = find_all_ordered_by_possibilities(orig_grid)
    
    if moves:
        #move = moves[0]
        
        
        moves[0]
        
        
        
        
        orig_grid[moves[0][0]][moves[0][1]] = moves[0][2]
        
        all_moves.append(('c',moves))
        move=None
        moves = None
        continue
   
    #break
    #backtrack
    backtrack(all_moves,orig_grid)
    
print(sudokuCheck(orig_grid))   

print("done")








































    
    




