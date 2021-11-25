import pygame
import numpy as np

pygame.init()

# pygame에서 사용되는 변수 선언

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
large_font = pygame.font.SysFont(None, 72)
CELL_SIZE = 100
COLUMN_COUNT = 7
ROW_COUNT = 6
P1_WIN = 1
P2_WIN = 2
DRAW = 3
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

grid = np.zeros((ROW_COUNT, COLUMN_COUNT))
mouse_x , mouse_y = pygame.mouse.get_pos()

clock = pygame.time.Clock()

def is_free_column_index(grid, column_index):
    if column_index < 0 or column_index > COLUMN_COUNT - 1:
        return False
    
    return grid[ROW_COUNT - 1][column_index] == 0 

def get_free_row_index(grid, column_index):
    for row_index in range(ROW_COUNT):
        if grid[row_index][column_index] == 0 :
            return row_index

def is_winner(grid, piece):
    for column_index in range(COLUMN_COUNT - 3):
        for row_index in range(ROW_COUNT):
            if grid[row_index][column_index] == piece and grid[row_index][column_index+1] == piece and grid[row_index][column_index+2] ==piece and grid[row_index][column_index+3] == piece:
                return True

# pygame 무한루프

def runGame():
    global done
    while not done:
        clock.tick(10)
        screen.fill(WHITE)
