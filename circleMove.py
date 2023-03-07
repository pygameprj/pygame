import pygame
import sys

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
R = 10  #반지름
STATE = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0,255, 0)

pygame.init()
pygame.display.set_caption("Simple PyGame Example")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pos_x = SCREEN_WIDTH/2
pos_y = SCREEN_HEIGHT/2

count = 0
clock = pygame.time.Clock()
while True:
    S = 1 + (count//10)*2
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    key_event = pygame.key.get_pressed()
    if key_event[pygame.K_LEFT]:
        pos_x -= S
        if pos_x <= 0 + R: # 화면 넘어가지 않는 부분
            pos_x = 0 + R
        
        if STATE == pygame.K_LEFT: #count++
            count += 1
        else: count = 0

        STATE = pygame.K_LEFT #이전상태

    if key_event[pygame.K_RIGHT]:
        pos_x += S
        if pos_x >= SCREEN_WIDTH - R:
            pos_x = SCREEN_WIDTH - R
        if STATE == pygame.K_RIGHT:
            count += 1
        else: count = 0
        STATE = pygame.K_RIGHT

    if key_event[pygame.K_UP]:
        pos_y -= S
        if pos_y <= 0 + R:
            pos_y = R
        if STATE == pygame.K_UP:
            count += 1
        else: count = 0
        STATE = pygame.K_UP

    if key_event[pygame.K_DOWN]:
        pos_y += S
        if pos_y >= SCREEN_HEIGHT - R:
            pos_y = SCREEN_HEIGHT - R
        if STATE == pygame.K_DOWN:
            count += 1
        else: count = 0
        STATE = pygame.K_DOWN

    screen.fill(BLACK)
    pygame.draw.circle(screen, GREEN, (pos_x, pos_y), R)
    pygame.display.update()