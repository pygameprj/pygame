# -*- coding: utf-8 -*-
# Clone coding
import pygame
import random

#전역 변수
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255, 0)

SCREEN_WIDTH = 400 #가로
SCREEN_HEIGHT = 900 #세로
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#오브젝트 클래스
class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0

    def put_img(self, address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
            self.sx, self.sy = self.img.get_size()

    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()

    def show(self):
        screen.blit(self.img, (self.x, self.y))

def main():
    # 1. 게임 초기화
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 2. 게임창 옵션 설정

    title = "My Game"
    pygame.display.set_caption(title)

    # 3. 게임내 필요한 설정
    clock = pygame.time.Clock()
    count = 0 #미사일 지연

    player = obj()  # SpaceShip
    player.put_img("image\good.png")
    player.change_size(80, 100)

    player.x = round(SCREEN_WIDTH / 2 - player.sx / 2)
    player.y = SCREEN_HEIGHT - player.sy - 15

    player.move = 7

    misile_list = []
    obstacle_list = []

    # 4. 메인 이벤트
    while True:
        # 4-1, FPS 설정
        clock.tick(60)
        # 4-2, 각종 입력 감지
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        #4-3키입력 움직임
        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_LEFT]:
            player.x -= player.move
            if player.x <= 0:
                player.x = 0

        if key_event[pygame.K_RIGHT]:
            player.x += player.move
            if player.x >= SCREEN_WIDTH - player.sx:
                player.x = SCREEN_WIDTH - player.sx

        if key_event[pygame.K_SPACE] and count % 6 == 0:
            count = 0
            misile = obj()  # misile
            misile.put_img("image\gbad.png")
            misile.change_size(15, 20)

            misile.x = round(player.x + player.sx / 2 - misile.sx / 2)
            misile.y = player.y - misile.y - 10
            misile.move = 15
            misile_list.append(misile)
        count += 1

        #오브젝트 삭제
        delObj_list = []
        for i in range(len(misile_list)):
            misile = misile_list[i]
            misile.y -= misile.move

            if misile.y <= -misile.sy:
                delObj_list.append(i)
        
        for delObj in delObj_list:
            del misile_list[delObj]

        # 랜덤하게 생성 되는 장애물
        if random.random() > 0.98:
            obstacle = obj()  # devil
            obstacle.put_img("image\direction.png")
            obstacle.change_size(50, 50)

            obstacle.x = random.randrange(0, SCREEN_WIDTH - obstacle.sx - round(player.sx / 2))
            obstacle.y = 10
            obstacle.move = 1

            obstacle_list.append(obstacle)
            
        # 장애물 삭제 되는 부분
        delObj_list = []
        for i in range(len(obstacle_list)):
            obstacle = obstacle_list[i]
            obstacle.y += obstacle.move

            if obstacle.y >= SCREEN_HEIGHT:
                delObj_list.append(i)
        
        for delObj in delObj_list:
            del obstacle_list[delObj]

        # 4-4, 그리기       
        screen.fill(BLACK)
        player.show()

        for misile in misile_list:
            misile.show()
        for obstacle in obstacle_list: 
            obstacle.show()

        # 4-5, 업데이트
        pygame.display.flip()

if __name__ == "__main__":
    main()