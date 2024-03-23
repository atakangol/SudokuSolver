# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 12:07:03 2024

@author: golat
"""

import pygame
import sys
import numpy as np
from sudoku import Sudoku
import pandas as pd
import time


def small_check(current_grid, entered_cell):
    row, col = entered_cell

    r = list(filter(lambda a: a != 0, current_grid[row]))
    # Check for duplicate values in the row
    if len(r) != len(set(r)):
        return 0
    
    # Check for duplicate values in the column
    column = [current_grid[i][col] for i in range(len(current_grid))]
    column = list(filter(lambda a: a != 0, column))
    
    if len(column) != len(set(column)):
        return 0

    # Check for duplicate values in the sub-grid
    subgrid_row_start = 3 * (row // 3)
    subgrid_col_start = 3 * (col // 3)
    sub_grid = [
        current_grid[i][subgrid_col_start:subgrid_col_start + 3]
        for i in range(subgrid_row_start, subgrid_row_start + 3)
    ]
    flat_sub_grid = [value for row in sub_grid for value in row]
    flat_sub_grid = list(filter(lambda a: a != 0, flat_sub_grid))
    if len(flat_sub_grid) != len(set(flat_sub_grid)):
        return 0

    return 1


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
                if len(possibilities) == 0: return []
                for possibility in possibilities:
                    empty_spaces.append((i, j, possibility))

    # Sort the empty spaces based on the number of possibilities
    empty_spaces.sort(key=lambda x: len(find_possibilities(grid, x[0], x[1])))

    return empty_spaces

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 594, 594
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
FADED_GREEN = (164, 209, 162)

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")






puzzle = Sudoku(3).difficulty(.9)
orig_grid = [[0 if element is None else element for element in row] for row in puzzle.board]

grid = [row.copy() for row in orig_grid]

all_moves = []



# Main game loop
writing_mode = False
current_number = None
validation_error = False
error_pos = None


while True:
    if sudokuCheck(grid):
        break
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    
        if True : #event.type == pygame.MOUSEBUTTONDOWN:
            
            #autoplay
            #print(all_moves)
    '''  
    move = find_easy(grid)
    if move :
        grid[move[0]][move[1]] = move[2]
    
        all_moves.append({'type':'m',
         'move':move,
         'possiblities':None
            })
        
        
        validation_error = small_check(grid,(move[0],move[1])) == 0
        #print(validation_error)
        # Update the grid with the entered number
        if validation_error: error_pos=(move[0],move[1])
        
        row,col = move[0:2]
        move=None
        #print("easy")
    else:
        
        move = find_least_possibilities(grid)
        if move:
            if len(move[2])==1:
                #print(move)
                grid[move[0]][move[1]] = move[2][0]
            
                #all_moves.append(('m',move))
                #orig_grid[move[0]][move[1]] = move[2][0]
                all_moves.append({'type':'m',
                 'move':(move[0],move[1],move[2][0]),
                 'possiblities':None
                    }
                                 )
                
                validation_error = small_check(grid,(move[0],move[1])) == 0
                #print(validation_error)
                # Update the grid with the entered number
                if validation_error: error_pos=(move[0],move[1])
                
                row,col = move[0:2]
                move=None
            else:
                moves = find_all_ordered_by_possibilities(grid)
                if moves:
                    move = moves.pop(0)
                    print(move)
                    grid[move[0]][move[1]] = move[2]
                    
                    all_moves.append(
                        {'type':'c',
                         'move':move,
                         'possiblities':moves
                            }
                         )
                    validation_error = small_check(grid,(move[0],move[1])) == 0
            
                    if validation_error: error_pos=(move[0],move[1])
                    
                    row,col = move[0:2]
                    move=None
                else:
                    #backtrack
                    print('backtrack')
                    
                    back_move = (None,None)
                    while len(all_moves)>0:
                        print(all_moves[-1])
                        back_move = all_moves.pop(-1)
                        if back_move['type']=='m':
                            move = back_move['move']
                            grid[move[0]][move[1]] = 0
                        else:
                            move = back_move['move']
                            grid[move[0]][move[1]] = 0
                            
                            possibilities = back_move['possiblities']
                            if len(possibilities) > 0:
                                new_move = possibilities.pop(0)
                                
                                grid[new_move[0]][new_move[1]] = new_move[2]
                
                
                                all_moves.append(
                                    {'type':'c',
                                     'move':new_move,
                                     'possiblities':possibilities
                                        }
                                     )
                                break
                            else:
                                pass
            
    
            
        
        
        
        
        screen.fill(WHITE)

        # Draw the grid lines
        for i in range(1, GRID_SIZE):
            # Draw bolder lines for subgrid boundaries
            line_thickness = 4 if i % 3 == 0 else 2

            # Vertical lines
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), line_thickness)
            # Horizontal lines
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_thickness)

        # Draw the numbers on the grid
        font = pygame.font.Font(None, 36)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] != 0:
                    if orig_grid[i][j] == 0:
                        color = FADED_GREEN  # Color modified cells faded green
                    else:
                        color = GREEN  # Color original cells green

                    # Draw the cell with or without a red border based on validation_error
                        

                    
                    pygame.draw.rect(screen, color,
                                     (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))



                    number_text = font.render(str(grid[i][j]), True, BLACK)
                    text_rect = number_text.get_rect(center=((j + 0.5) * CELL_SIZE, (i + 0.5) * CELL_SIZE))
                    screen.blit(number_text, text_rect)
        if validation_error and error_pos:
            pygame.draw.rect(screen, (255,0,0),
                                     (error_pos[1] * CELL_SIZE, error_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            number_text = font.render(str(grid[error_pos[0]][error_pos[1]]), True, BLACK)
            text_rect = number_text.get_rect(center=((error_pos[1]+ 0.5) * CELL_SIZE, (error_pos[0] + 0.5) * CELL_SIZE))
            screen.blit(number_text, text_rect)

        # Highlight the current cell in writing mode
        if writing_mode:
            pygame.draw.rect(screen, YELLOW, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
        # Draw the grid lines
        for i in range(1, GRID_SIZE):
            # Draw bolder lines for subgrid boundaries
            line_thickness = 4 if i % 3 == 0 else 2

            # Vertical lines
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), line_thickness)
            # Horizontal lines
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_thickness)

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        pygame.time.Clock().tick(60)
        
        #print(all_moves)
        time.sleep(0.1)
    
    
    
    
    
    
    


