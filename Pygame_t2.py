# -*- coding: utf-8 -*-
# Clone coding
import pygame
import random
import time

#전역 변수
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255, 0)
RED = (255, 0, 0)
M_PER = 3 # 미사일 생성 확률 퍼센트
addressTF = 1 # 상대경로는 0, 절대 경로는 1

#파일 경로
playerFile = ["image\gfigter.png", "C:\code\pygame\image\gfigter.png"]
missileFile = ["image\missile.png", "C:\code\pygame\image\missile.png"]
obsFile = ["image\devil.png", "C:\code\pygame\image\devil.png"]
boomFile = ["image\explosion.png", "C:\code\pygame\image\explosion.png"]
boomSoundFile = ["sound\death_devil.mp3", "C:\code\pygame\sound\death_devil.mp3"]
fontFile = ['font\KOTRA_GOTHIC.ttf', 'C:\code\pygame\_font\KOTRA_GOTHIC.ttf']
happythemeBGM = ["sound\happythemeBGM.mp3", "C:\code\pygame\sound\happythemeBGM.mp3"]
laserGunSound = ["sound\laserGun.mp3", "C:\code\pygame\sound\laserGun.mp3"]
gameOverSound = ["sound\gameOver.mp3", "C:\code\pygame\sound\gameOver.mp3"]
downHPSound = ["sound\downHP.mp3", "C:\code\pygame\sound\downHP.mp3"]

player_HP = 10
player_SPEED = 7
missile_SPEED = 15
obs_HP = 4

#objSize
playerSizeX = 80
playerSizeY = 100
missileSizeX = 15
missileSizeY = 20
obsSizeX = 50
obsSizeY = 50
boomX = 50
boomY = 50

SCREEN_WIDTH = 400 #가로
SCREEN_HEIGHT = 900 #세로

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

    def show(self, screen):
        screen.blit(self.img, (self.x, self.y))

def initPlayer(player):
    player.put_img(playerFile[addressTF])
    player.change_size(playerSizeX, playerSizeY)
    player.x = round((SCREEN_WIDTH - player.sx)/2)
    player.y = SCREEN_HEIGHT - player.sy - 15
    player.move = player_SPEED
    player.HP = player_HP

def newMissile(m_list, m_STR, player):
    missile = obj()  # missile
    missile.put_img(missileFile[addressTF])
    missile.change_size(missileSizeX, missileSizeY)
    missile.x = round(player.x + player.sx/2 - missile.sx/2)
    missile.y = player.y - missile.y
    missile.move = missile_SPEED
    missile.STR = m_STR
    m_list.append(missile)

def newobs(obs_list, obs_SPEED = 2):
    if random.random() < M_PER/100:
        obstacle = obj()  # devil
        obstacle.put_img(obsFile[addressTF])
        obstacle.change_size(obsSizeX, obsSizeY)
        obstacle.x = random.randrange(0, SCREEN_WIDTH - obstacle.sx)
        obstacle.y = 10 + 40
        obstacle.move = obs_SPEED
        obstacle.HP = obs_HP
        obs_list.append(obstacle)

def makeBoom(boom_list, obj_list, delObj_list):
    for i in range(len(delObj_list)):
        obj_list[delObj_list[i]]
        boom = obj()
        boom.put_img(boomFile[addressTF])
        boom.change_size(boomX, boomY)
        boom.x = obj_list[delObj_list[i]].x
        boom.y = obj_list[delObj_list[i]].y
        boom_list.append(boom)
        # pygame.mixer.music.stop()
        pygame.mixer.Sound(boomSoundFile[addressTF]).play()
        # pygame.mixer.music.play(-1)

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

def downHP(player):
    pygame.mixer.Sound(downHPSound[addressTF]).play()
    player.HP -= 1

#오브젝트 삭제
def delObjf(obj_list, delObj_list):
    if len(delObj_list):
        # print("del list: ", delObj_list)

        reversed_delObj_list = delObj_list[::-1]    #역순으로 읽어야 버그 안 터짐
        for delObj in reversed_delObj_list:
            del obj_list[delObj]
            
#오브젝트가 나가면 삭제
def outObj(obj_list, player):
    count = 0
    delObj_list = []
    if len(obj_list):
        for i in range(len(obj_list)):
            if obj_list[i].y < 0:
                delObj_list.append(i)
            if obj_list[i].y + obj_list[i].sy > SCREEN_HEIGHT: 
                delObj_list.append(i)
                count += 1 
    delObjf(obj_list, delObj_list)
    if count: downHP(player)
    return count

#충돌
def hitObs(m_list, obs_list, boom_list):
    TF = False
    delObs_list = []; delM_list = []

    for i in range(len(m_list)):
        for j in range(len(obs_list)):
            if oLap(m_list[i], obs_list[j]):
                m_list[i].HP -= 1; obs_list[j].HP -= 1
                if  m_list[i].HP <= 0 and i not in delM_list: delM_list.append(i) 
                if obs_list[j].HP <= 0 and j not in delObs_list: delObs_list.append(j)
                TF = True
    makeBoom(boom_list, obs_list, delObs_list)
    global obsCount
    obsCount += len(delObs_list)
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
def drawInit(screenInit, state = 0):
    screenInit.fill(BLACK)
    # if state == 0:
    #     writeScore(screenInit, "게임 시작", 120, 300, color = WHITE, size = 40)
    #     writeScore(screenInit, "설정", 160, 460, color = WHITE, size = 40)
    if state == 0:
        writeScore(screenInit, "게임 시작", 120, 300, color = WHITE, size = 60)
        writeScore(screenInit, "설정", 160, 460, color = WHITE, size = 40)
    elif state == 1: 
        writeScore(screenInit, "게임 시작", 120, 300, color = WHITE, size = 40)
        writeScore(screenInit, "설정", 160, 460, color = WHITE, size = 60)
    return state

def initDisplay(screenInit, clock):
    state = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        key_event = pygame.key.get_pressed()
        if drawInit(screenInit, state) == 0 and (key_event[pygame.K_KP_ENTER]):
            break
        if key_event[pygame.K_DOWN] and state < 1:
            state +=1
        if key_event[pygame.K_UP] and state > 0:
            state -= 1
        pygame.display.flip()

def drawGame(screenGame, player, m_list, obs_list, boom_list):
    screenGame.fill(BLACK)
    player.show(screenGame)

    for missile in m_list:
        missile.show(screenGame)
    for obstacle in obs_list: 
        obstacle.show(screenGame)
    for boom in boom_list:
        boom.show(screenGame)
    delObjf(boom_list, [i for i in range(len(boom_list))])

def mainKey_event(player, missile_Sound, missile_list, missile_STR, count):
    # 4-2, 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
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
        missile_Sound.play()
        newMissile(missile_list, missile_STR, player)
        count = 0
    # if key_event[pygame.K_ESCAPE]:

    
#게임 오버
def ifGameOver(screenGame, player, size = 40):
    if player.HP <= 0:
        font = pygame.font.Font(fontFile[addressTF], size)
        text = font.render("GAME OVER!", True, RED)
        screenGame.blit(text,(80, SCREEN_HEIGHT/2))
        pygame.mixer.music.stop()
        pygame.mixer.Sound(gameOverSound[1]).play()
        pygame.display.flip()
        time.sleep(3)
        return True
    return False
      
def writeScore(screen, message, fontX, fontY, count = -1, color = WHITE, size = 20):
    font = pygame.font.Font(fontFile[addressTF], size)
    if count != -1: text = font.render(message + ": "+ str(count), True, color)
    else: text = font.render(message, True, color)
    screen.blit(text,(fontX,fontY))

def main():
    # 1. 게임 초기화
    pygame.init()
    pygame.mixer.music.load(happythemeBGM[addressTF])
    pygame.mixer.music.play(-1)
    missile_Sound = pygame.mixer.Sound(laserGunSound[addressTF])
    screenInit = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screenGame = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 2. 게임창 옵션 설정
    title = "My Game"
    pygame.display.set_caption(title)

    # 3. 게임내 필요한 설정
    missile_list = []; obstacle_list = []; boom_list = []
    clock = pygame.time.Clock()
    count = 0 #미사일 지연
    damageAmount = 0 #총 딜량
    global obsCount; obsCount = 0 #장애물 삭제 갯수
    missile_STR = 1 #미사일 공격력
    obs_SPEED = 2 # 장애물 속도

    initDisplay(screenInit, clock)
    player = obj()  # SpaceShip
    initPlayer(player) #player state init

    # 4. 메인 이벤트
    while True:
        count += 1
        # 4-1, FPS setting
        clock.tick(60)
        #check key_event
        mainKey_event(player, missile_Sound, missile_list, missile_STR, count)

        # random new obstacle
        if obsCount/10: obs_SPEED = 2 + obsCount/10
        newobs(obstacle_list, obs_SPEED)

        #move obj
        UPObjf(missile_list)
        DOWNObjf(obstacle_list)
    
        #delete obj when out
        outObj(obstacle_list, player)

        #충돌시 오브젝트 파괴
        if hitObs(missile_list, obstacle_list, boom_list):  damageAmount += 1

        #if player when hit, down HP
        if hitPlayer(player, obstacle_list): downHP(player)

        # 4-4, draw Display
        drawGame(screenGame, player, missile_list, obstacle_list, boom_list)
        writeScore(screenGame, "총 딜량", 10, 0, count = damageAmount)
        writeScore(screenGame, "처리한 악마 수", 10, 20, count = obsCount)
        writeScore(screenGame, "player HP", SCREEN_WIDTH-140, 00, count = player.HP, color =  GREEN)
        if ifGameOver(screenGame, player): break

        # 4-5, Display update
        pygame.display.flip()

if __name__ == "__main__":
    main()