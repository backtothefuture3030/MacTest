import pygame  # pygame 선언
import random 


pygame.init()  # pygame 초기화

# pygame에 사옹되는 전역변수 선언

BLACK = (0, 0, 0)
RED = (255, 0 , 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CELL_SIZE = 50
COLUMN_COUNT = SCREEN_WIDTH // CELL_SIZE
ROW_COUNT = SCREEN_HEIGHT // CELL_SIZE

grid = [[{'mine':False, 'open':False, 'mine_count_around': 0 , 'flag' : False} for _ in range(COLUMN_COUNT)]for _ in range(ROW_COUNT)]
Mine_Count = 15
for _ in range(Mine_Count):
    while True:    # 지뢰가 중복되지 않도록 먼저 지뢰가 있는지 여부 확인.
        column_index = random.randint(0, COLUMN_COUNT - 1)
        row_index = random.randint(0, ROW_COUNT - 1)
        tile = grid[row_index][column_index]
        if not tile['mine']:
            tile['mine'] = True
            break
clock = pygame.time.Clock()

def in_bound(collumn_index, row_index):   # 접근 가능한 쉘인지 판단.
    if (0 <= collumn_index < COLUMN_COUNT and 0 <= row_index < ROW_COUNT):
        return True
    else:
        return False

def open_tile(collumn_index, row_index):
    if not in_bound(collumn_index, row_index):
        return
    tile = grid[row_index][collumn_index]
    if not tile['open']:
        tile['open']= True
    else:
        return



# pygame 무한 루프

def runGame():
    global done
    while not done:
        clock.tick(10)
        screen.fill(WHITE)

runGame()
pygame.quit()


