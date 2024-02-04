import pygame
import sys

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

orig_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


orig_grid = [[6, 8, 9, 2, 0, 0, 0, 4, 0], [2, 4, 1, 0, 0, 0, 9, 3, 0], [3, 7, 5, 4, 9, 8, 1, 2, 6], [0, 5, 0, 0, 0, 3, 6, 0, 0], [0, 6, 0, 0, 0, 0, 3, 0, 4], [9, 3, 0, 0, 0, 6, 2, 0, 1], [0, 0, 3, 0, 6, 0, 0, 0, 0], [0, 2, 0, 8, 0, 0, 0, 1, 0], [0, 0, 4, 3, 2, 0, 8, 0, 0]]


current_grid = [row.copy() for row in orig_grid]


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




# Main game loop
writing_mode = False
current_number = None
validation_error = False
error_pos = None


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            row = event.pos[1] // CELL_SIZE
            col = event.pos[0] // CELL_SIZE

            if orig_grid[row][col] == 0:  # Check if the cell is empty in orig_grid
                if event.button == 1:
                    # left click
                    # enter writing mode
                    writing_mode = True
                    current_number = None
                    validation_error = False  # Reset the validation error
                    print("Left Click -", event.pos)

        elif event.type == pygame.KEYDOWN and writing_mode:
            #current_number = 0
            # Check if the pressed key is a number between 1 and 9
            if pygame.K_1 <= event.key <= pygame.K_9:
                current_number = int(chr(event.key))
                print("Writing Mode - Entered number:", current_number)
            elif event.key == pygame.K_RETURN:
                current_grid[row][col] = current_number
                # Enter key pressed
                validation_error = small_check(current_grid, (row, col)) == 0
                print(validation_error)
                # Update the grid with the entered number
                if validation_error: error_pos=(row,col)
                print("Entered Number:", current_number)
                writing_mode = False

    # Clear the screen
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
            if current_grid[i][j] != 0:
                if orig_grid[i][j] == 0:
                    color = FADED_GREEN  # Color modified cells faded green
                else:
                    color = GREEN  # Color original cells green

                # Draw the cell with or without a red border based on validation_error
                    

                
                pygame.draw.rect(screen, color,
                                 (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))



                number_text = font.render(str(current_grid[i][j]), True, BLACK)
                text_rect = number_text.get_rect(center=((j + 0.5) * CELL_SIZE, (i + 0.5) * CELL_SIZE))
                screen.blit(number_text, text_rect)
    if validation_error and error_pos:
        pygame.draw.rect(screen, (255,0,0),
                                 (error_pos[1] * CELL_SIZE, error_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        number_text = font.render(str(current_grid[error_pos[0]][error_pos[1]]), True, BLACK)
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
