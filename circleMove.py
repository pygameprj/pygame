import pygame
import sys

SCREEN_WIDTH = 1080 #가로
SCREEN_HEIGHT = 720 #세로
R = 10  #반지름

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0,255, 0)

def main():

    pygame.init()
    pygame.display.set_caption("Simple PyGame Example")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pos_x = SCREEN_WIDTH/2 #시작 x 좌표
    pos_y = SCREEN_HEIGHT/2 #시작 y좌표
    state = 0 #이전 상태
    count = 0 # 같은 상태 몇번 했는지
    clock = pygame.time.Clock() #주기
    while True:
        clock.tick(60) #주기 마다 입력 키값 받음
        for event in pygame.event.get(): #종료키 입력 되면 종료(컨트롤 + C)
            if event.type == pygame.QUIT:
                sys.exit()

        key_event = pygame.key.get_pressed() #무슨 키 입력했는지
        if key_event[pygame.K_LEFT]: #왼쪽
            if state == pygame.K_LEFT: #이전 상태와 같은 상태면 count++
                count += 1
            else: count = 0
            
            state = pygame.K_LEFT #상태
            S = 1 + (count//10)*2   #속도
            pos_x -= S  #이동

            if pos_x <= 0 + R: # 화면 넘어가지 않는 부분
                pos_x = 0 + R

        if key_event[pygame.K_RIGHT]: #오른쪽
            if state == pygame.K_RIGHT: #이전 상태와 같은 상태면 count++
                count += 1
            else: count = 0

            state = pygame.K_RIGHT #상태
            S = 1 + (count//10)*2   #속도
            pos_x += S  #이동

            if pos_x >= SCREEN_WIDTH - R: # 화면 넘어가지 않는 부분
                pos_x = SCREEN_WIDTH - R

        if key_event[pygame.K_UP]: #위쪽
            if state == pygame.K_UP: #이전 상태와 같은 상태면 count++
                count += 1
            else: count = 0

            state = pygame.K_UP #상태
            S = 1 + (count//10)*2   #속도
            pos_y -= S  #이동

            if pos_y <= 0 + R: # 화면 넘어가지 않는 부분
                pos_y = R

        if key_event[pygame.K_DOWN]:    #아래쪽
            if state == pygame.K_DOWN: #이전 상태와 같은 상태면 count++
                count += 1
            else: count = 0

            state = pygame.K_DOWN #상태
            S = 1 + (count//10)*2   #속도
            pos_y += S  #이동

            if pos_y >= SCREEN_HEIGHT - R: # 화면 넘어가지 않는 부분
                pos_y = SCREEN_HEIGHT - R

        screen.fill(BLACK)  #배경 색 검은색으로 그리기
        pygame.draw.circle(screen, GREEN, (pos_x, pos_y), R)    #원 그리기
        pygame.display.update() #화면 업데이트

if __name__ == '__main__':
    main()
