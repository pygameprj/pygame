# -*- coding: utf-8 -*-
# Clone coding
import pygame
import random

#전역 변수
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255, 0)
M_PER = 10 # 미사일 생성 확률 퍼센트
player_HP = 100
player_SPEED = 7
misile_SPEED = 15
obs_HP = 5
obs_SPEED = 1

#objSize
playerSizeX = 80
playerSizeY = 100
misileSizeX = 15
misileSizeY = 20
obsSizeX = 50
obsSizeY = 50

SCREEN_WIDTH = 400 #가로
SCREEN_HEIGHT = 900 #세로
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#오브젝트 클래스
class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
        self.HP = 1
        self.STR = 1

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

def initPlayer(player):
    player.put_img("image\good.png")
    player.change_size(playerSizeX, playerSizeY)
    player.x = round((SCREEN_WIDTH - player.sx)/2)
    player.y = SCREEN_HEIGHT - player.sy - 15
    player.move = player_SPEED
    player.HP = player_HP

def newMisile(m_list, m_STR, player):
    misile = obj()  # misile
    misile.put_img("image\gbad.png")
    misile.change_size(misileSizeX, misileSizeY)
    misile.x = round(player.x + player.sx/2 - misile.sx/2)
    misile.y = player.y - misile.y
    misile.move = misile_SPEED
    misile.STR = m_STR
    m_list.append(misile)

def newobs(obs_list):
    if random.random() < M_PER/100:
        obstacle = obj()  # devil
        obstacle.put_img("image\direction.png")
        obstacle.change_size(obsSizeX, obsSizeY)
        obstacle.x = random.randrange(0, SCREEN_WIDTH - obstacle.sx)
        obstacle.y = 10
        obstacle.move = obs_SPEED
        obstacle.HP = obs_HP
        obs_list.append(obstacle)

#충돌여부
def oLap(obj1, obj2):
    if obj1.x <= obj2.x + obj2.sx and obj1.x + obj1.sx >= obj2.x and obj1.y <= obj2.y + obj2.sy and obj1.y + obj1.sy >= obj2.y:
        return True
    return False

#오브젝트 이동
def UPObjf(obj_list):
    for i in range(len(obj_list)):
        obj = obj_list[i]
        obj.y -= obj.move

def DOWNObjf(obj_list):
    for i in range(len(obj_list)):
        obj = obj_list[i]
        obj.y += obj.move

#오브젝트 삭제
def delObjf(obj_list, delObj_list):
    if len(delObj_list):
        # print("del list: ", delObj_list)

        reversed_delObj_list = delObj_list[::-1]    #역순으로 읽어야 버그 안 터짐
        for delObj in reversed_delObj_list:
            del obj_list[delObj]

#오브젝트가 나가면 삭제
def outOfObj(obj_list):
    delObj_list = []
    if len(obj_list):
        for i in range(len(obj_list)):
            if obj_list[i].y < 0 or obj_list[i].y + obj_list[i].sy > SCREEN_HEIGHT: 
                delObj_list.append(i)
    delObjf(obj_list, delObj_list)

#충돌
def hitObs(m_list, obs_list):
    TF = False
    delObs_list = []; delM_list = []

    for i in range(len(m_list)):
        for j in range(len(obs_list)):
            if oLap(m_list[i], obs_list[j]):
                m_list[i].HP -= 1; obs_list[j].HP -= 1
                if  m_list[i].HP <= 0 and i not in delM_list: delM_list.append(i) 
                if obs_list[j].HP <= 0 and j not in delObs_list: delObs_list.append(j)
                TF = True

    delObjf(obs_list, delObs_list)
    delObjf(m_list, delM_list)
    return TF

def hitPlayer(player, obs_list):
    TF = False; delObs_list = []
    for j in range(len(obs_list)):
        if oLap(obs_list[j], player):
            obs_list[j].HP -= obs_HP
            if obs_list[j].HP <= 0 and j not in delObs_list: delObs_list.append(j)
            TF = True
    delObjf(obs_list, delObs_list)
    return TF

#그리기 함수
def drawf(screen, player, m_list, obs_list):
    screen.fill(BLACK)
    player.show()

    for misile in m_list:
        misile.show()
    for obstacle in obs_list: 
        obstacle.show()

#게임 오버
def ifGameOver(player):
    if player.HP <= 0:
        print("player HP is 0 \n GAME OVER!")
        exit(0)

def main():
    # 1. 게임 초기화
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 2. 게임창 옵션 설정
    title = "My Game"
    pygame.display.set_caption(title)

    # 3. 게임내 필요한 설정
    misile_list = []; obstacle_list = []
    clock = pygame.time.Clock()
    count = 0 #미사일 지연
    obsCount = 0 #장애물 삭제 갯수
    misile_STR = 1 #미사일 공격력

    player = obj()  # SpaceShip
    initPlayer(player) #플래이어 상태 초기화

    # 4. 메인 이벤트
    while True:
        # 4-1, FPS 설정
        clock.tick(60)
        # 4-2, 각종 입력 감지
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        ifGameOver(player)
        # print("player HP: ", player.HP, end ="\n")

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

        #스패이스바 입력시 미사일 생성
        if key_event[pygame.K_SPACE] and count % 6 == 0:
            newMisile(misile_list, misile_STR, player)
            count = 0
        count += 1

        # 랜덤하게 생성 되는 장애물
        newobs(obstacle_list)

        #move obj
        UPObjf(misile_list)
        DOWNObjf(obstacle_list)
    
        #del obj 
        outOfObj(misile_list)
        outOfObj(obstacle_list)

        #충돌시 오브젝트 파괴
        if hitObs(misile_list, obstacle_list): obsCount += 1
        #플래이어 체력 감소
        if hitPlayer(player, obstacle_list): player.HP -= 1
        # print("obs del count: ",obsCount)

        # 4-4, 그리기 
        drawf(screen, player, misile_list, obstacle_list)      

        # 4-5, 업데이트
        pygame.display.flip()

if __name__ == "__main__":
    main()