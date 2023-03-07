import pygame
import sys

SCREEN_WIDTH = 1080 #가로
SCREEN_HEIGHT = 720 #세로
R = 10  #반지름
STATE = 0 #이전 상태

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0,255, 0)

pygame.init()
pygame.display.set_caption("Simple PyGame Example")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pos_x = SCREEN_WIDTH/2 #시작 x 좌표
pos_y = SCREEN_HEIGHT/2 #시작 y좌표

count = 0 # 같은 상태 몇번 했는지
clock = pygame.time.Clock() #주기
while True:
    clock.tick(60) #주기 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    key_event = pygame.key.get_pressed() #무슨 키 입력했는지
    if key_event[pygame.K_LEFT]: #왼쪽
        if STATE == pygame.K_LEFT: #count++
            count += 1
        else: count = 0
        STATE = pygame.K_LEFT #이전상태
        S = 1 + (count//10)*2   #속도
        pos_x -= S
        if pos_x <= 0 + R: # 화면 넘어가지 않는 부분
            pos_x = 0 + R

    if key_event[pygame.K_RIGHT]: #오른쪽
        if STATE == pygame.K_RIGHT:
            count += 1
        else: count = 0
        STATE = pygame.K_RIGHT
        S = 1 + (count//10)*2   #속도
        pos_x += S
        if pos_x >= SCREEN_WIDTH - R:
            pos_x = SCREEN_WIDTH - R

    if key_event[pygame.K_UP]: #위쪽
        if STATE == pygame.K_UP:
            count += 1
        else: count = 0
        STATE = pygame.K_UP
        S = 1 + (count//10)*2   #속도
        pos_y -= S
        if pos_y <= 0 + R:
            pos_y = R

    if key_event[pygame.K_DOWN]:    #아래쪽
        if STATE == pygame.K_DOWN:
            count += 1
        else: count = 0
        STATE = pygame.K_DOWN
        S = 1 + (count//10)*2   #속도
        pos_y += S
        if pos_y >= SCREEN_HEIGHT - R:
            pos_y = SCREEN_HEIGHT - R

    screen.fill(BLACK)
    pygame.draw.circle(screen, GREEN, (pos_x, pos_y), R)
    pygame.display.update()
