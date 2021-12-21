import pygame
import random

pygame.init()

pygame.display.set_caption("SupGame") # 게임이름

screen_width = 480  # 가로크기
screen_height = 640 # 세로크기

screen = pygame.display.set_mode((screen_width,screen_height))

background = pygame.image.load("E:\\PythonRunGame\\background.png")
character = pygame.image.load("E:\PythonRunGame\\character.png")  
character_size = character.get_rect().size  # 이미지의 크기를 구해옴
character_width = character_size[0]  # 캐릭터의 가로크기
character_height = character_size[1]   # 캐릭터의 세로크기
character_x_pos = (screen_width / 2) - (character_width/2)  # 화면 가로의 절반, 즉 가운데 (갸로)
character_y_pos = screen_height - character_height # 화면 세로크기 가장 아래에 (세로)

to_x = 0
character_speed = 0.6

enemy = pygame.image.load("E:\PythonRunGame\\enemy.png")  
enemy_size = enemy.get_rect().size  # 이미지의 크기를 구해옴
enemy_width = enemy_size[0]  # 캐릭터의 가로크기
enemy_height = enemy_size[1]   # 캐릭터의 세로크기
enemy_x_pos = random.randint(0, screen_width-enemy_width)  # 랜덤으로 떨어뜨리는 위치
enemy_y_pos = 0  # 화면 가장 상단에 두기

game_font = pygame.font.Font(None, 40)

start_ticks = pygame.time.get_ticks() # 현재 tick 을 받아옴

clock = pygame.time.Clock()  # 프레임

running = True 
while running:
    dt = clock.tick(30)
    enemy_y_pos+=10
    if enemy_y_pos >= 570:
        enemy_x_pos = random.randint(0, screen_width-enemy_width)
        enemy_y_pos=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed

        if event.type == pygame.KEYUP:  # 방향키를 때면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0 


    character_x_pos += to_x * dt

    # 가로 경계값 처리
    if character_x_pos < 0 :
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    character_rect = character.get_rect()   
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()  
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos


    if character_rect.colliderect(enemy_rect):
        print("충돌 했어요! ")
        running = False



    screen.blit(background,(0,0))
    screen.blit(character,(character_x_pos,character_y_pos))
    screen.blit(enemy,(enemy_x_pos,enemy_y_pos))

    elapsed_time = (pygame.time.get_ticks()-start_ticks) / 1000 #초로 환산하기 위해 1000으로 나눈다
    timer = game_font.render(str(int(elapsed_time)), True, (255,255,255)) 
    screen.blit(timer,(220,300))

    pygame.display.update()

pygame.quit()