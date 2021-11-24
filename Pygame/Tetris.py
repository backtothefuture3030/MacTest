import sys
from math import sqrt
from random import randint
import pygame

pygame.init()
smallfont = pygame.font.SysFont(None, 36)
largefont = pygame.font.SysFont(None, 72)

BLACK = (0,0,0)
pygame.key.set_repeat(30,30)
SCREEN_WIDTH = 600
SCREEN_HEIGHT =  800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

WIDTH = 12
HEIGHT = 22
INTERVAL = 40

# TODO Field 값을 채운다
Field = []
COLORS = ((0,0,0), (255,165,0), (0,0,255), (0,255,255), (0,255,0), (255,0,255), (255,255,0), (255,0,0), (128,128,128))
BLOCK = None
NEXT_BLOCK = None
PIECE_SIZE = 24 # 24 X 24
PIECE_GRID_SIZE = PIECE_SIZE + 1

BLOCK_DATA = (
    (
        (0,0,1,
         1,1,1,
         0,0,0)
        (0,1,0,
         0,1,0,
         0,1,1)
        (0,0,0,
         1,1,1,
         1,0,0),
        (1,1,0,
         0,1,0,
         0,1,0),
        )
    )(
        (2,0,0,
         2,2,2,
         0,0,0)
        (0,2,2,
         0,2,0,
         0,2,0)
        (0,0,0,
         2,2,2,
         0,0,2)
        (0,2,0,
         0,2,0,
         2,2,0)
            
        )
    )
)