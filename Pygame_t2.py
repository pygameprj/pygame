# -*- coding: utf-8 -*-
# Clone coding
import pygame
import random

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [400, 900]
screen = pygame.display.set_mode(size)

title = "My Game"
pygame.display.set_caption(title)

# 3. 게임내 필요한 설정
clock = pygame.time.Clock()

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


ss = obj()  # SpaceShip
ss.put_img("image\good.png")
ss.change_size(80, 100)

ss.x = round(size[0] / 2 - ss.sx / 2)
ss.y = size[1] - ss.sy - 15

ss.move = 7

m_list = []
a_list = []

black = (0, 0, 0)
white = (255, 255, 255)

# 4. 메인 이벤트
k = 0 #미사일 지연
while True:
     # 4-1, FPS 설정
    clock.tick(60)

    # 4-2, 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 5 게임종료
            pygame.quit()

    key_event = pygame.key.get_pressed()
    if key_event[pygame.K_LEFT]:
        ss.x -= ss.move
        if ss.x <= 0:
            ss.x = 0

    if key_event[pygame.K_RIGHT]:
        ss.x += ss.move
        if ss.x >= size[0] - ss.sx:
            ss.x = size[0] - ss.sx

    if key_event[pygame.K_SPACE] and k % 6 == 0:
        mm = obj()  # misile
        mm.put_img("image\gbad.png")
        mm.change_size(15, 20)

        mm.x = round(ss.x + ss.sx / 2 - mm.sx / 2)
        mm.y = ss.y - mm.y - 10
        mm.move = 15
        m_list.append(mm)
    k += 1

    d_list = []
    for i in range(len(m_list)):
        m = m_list[i]
        m.y -= m.move

        if m.y <= -m.sy:
            d_list.append(i)
    
    for d in d_list:
        del m_list[d]

    if random.random() > 0.98: # 랜덤하게 생성 되는 장애물
        aa = obj()  # devil
        aa.put_img("image\direction.png")
        aa.change_size(50, 50)

        aa.x = random.randrange(0, size[0] - aa.sx - round(ss.sx / 2))
        aa.y = 10
        aa.move = 1

        a_list.append(aa)
        
    # 장애물 삭제 되는 부분
    d_list = []
    for i in range(len(a_list)):
        a = a_list[i]
        a.y += a.move

        if a.y >= size[1]:
            d_list.append(i)
    
    for d in d_list:
        del a_list[d]

    # 4-4, 그리기       
    screen.fill(black)
    ss.show()

    for m in m_list:
        m.show()
    for a in a_list: 
        a.show()

    # 4-5, 업데이트
    pygame.display.flip()