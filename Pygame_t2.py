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
addressTF = 1 # 상대경로는 0, 절대 경로는 1

#파일 경로
fontFile = ['font\KOTRA_GOTHIC.ttf', 'C:\code\pygame\_font\KOTRA_GOTHIC.ttf']
playerFile = ["image\_figter.png", "C:\code\pygame\image\_figter.png"]
missileFile = ["image\missile.png", "C:\code\pygame\image\missile.png"]
obsFile = ["image\devil.png", "C:\code\pygame\image\devil.png"]
boomFile = ["image\explosion.png", "C:\code\pygame\image\explosion.png"]
boomSoundFile = ["sound\death_devil.mp3", "C:\code\pygame\sound\death_devil.mp3"]
happythemeBGM = ["sound\happythemeBGM.mp3", "C:\code\pygame\sound\happythemeBGM.mp3"]
laserGunSound = ["sound\laserGun.mp3", "C:\code\pygame\sound\laserGun.mp3"]
gameOverSound = ["sound\gameOver.mp3", "C:\code\pygame\sound\gameOver.mp3"]
downHPSound = ["sound\downHP.mp3", "C:\code\pygame\sound\downHP.mp3"]

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

class initVar:
    def __init__(self):
        self.missile_list = []
        self.obstacle_list = []
        self.boomissile_list = []

        self.player_HP = 10
        self.player_SPEED = 7
        self.missile_SPEED = 15
        self.obs_HP = 4

        #objSize
        self.playerSizeX = 80
        self.playerSizeY = 100
        self.missileSizeX = 15
        self.missileSizeY = 20
        self.obsSizeX = 50
        self.obsSizeY = 50
        self.boomX = 50
        self.boomY = 50

        self.obsCount = 0
        self.damageAmount = 0
        self.m_STR = 1
        self.missile_STR = 1
        self.M_PER = 3 # 미사일 생성 확률 퍼센트
        self.obs_SPEED = 2
        
def initPlayer(player):
    init_var = initVar()
    player.put_img(playerFile[addressTF])
    player.change_size(init_var.playerSizeX, init_var.playerSizeY)
    player.x = round((SCREEN_WIDTH - player.sx)/2)
    player.y = SCREEN_HEIGHT - player.sy - 15
    player.move = init_var.player_SPEED
    player.HP = init_var.player_HP

def newMissile(init_var, player):
    missile = obj()  # missile
    missile.put_img(missileFile[addressTF])
    missile.change_size(init_var.missileSizeX, init_var.missileSizeY)
    missile.x = round(player.x + player.sx/2 - missile.sx/2)
    missile.y = player.y - missile.y
    missile.move = init_var.missile_SPEED
    missile.STR = init_var.m_STR
    init_var.missile_list.append(missile)

def newobs(state_var):
    if random.random() < state_var.M_PER/100:
        obstacle = obj()  # devil
        obstacle.put_img(obsFile[addressTF])
        obstacle.change_size(state_var.obsSizeX, state_var.obsSizeY)
        obstacle.x = random.randrange(0, SCREEN_WIDTH - obstacle.sx)
        obstacle.y = 10 + 40
        obstacle.move = state_var.obs_SPEED
        obstacle.HP = state_var.obs_HP
        state_var.obstacle_list.append(obstacle)

def makeBoom(delObj_list, state_var): 
    for i in range(len(delObj_list)):
        state_var.obstacle_list[delObj_list[i]]
        boom = obj()
        boom.put_img(boomFile[addressTF])
        boom.change_size(state_var.boomX, state_var.boomY)
        boom.x = state_var.obstacle_list[delObj_list[i]].x
        boom.y = state_var.obstacle_list[delObj_list[i]].y
        boom.HP = 20 # 폭발 이펙트 지속 시간, 약 0.3초
        state_var.boomissile_list.append(boom)
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
        delObj_list.sort(reverse=True)    #역순으로 읽어야 버그 안 터짐
        for delObj in delObj_list:
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
def hitObs(state_var):
    TF = False
    delobstacle_list = []; delmissile_list = []

    for i in range(len(state_var.missile_list)):
        for j in range(len(state_var.obstacle_list)):
            if oLap(state_var.missile_list[i], state_var.obstacle_list[j]):
                state_var.missile_list[i].HP -= 1; state_var.obstacle_list[j].HP -= 1
                if  state_var.missile_list[i].HP <= 0 and i not in delmissile_list: delmissile_list.append(i) 
                if state_var.obstacle_list[j].HP <= 0 and j not in delobstacle_list: delobstacle_list.append(j)
                TF = True
    makeBoom(delobstacle_list, state_var)
    state_var.obsCount += len(delobstacle_list)
    delObjf(state_var.obstacle_list, delobstacle_list)
    delObjf(state_var.missile_list, delmissile_list)
    
    return TF

def hitPlayer(player, state_var):
    TF = False; delobstacle_list = []
    for j in range(len(state_var.obstacle_list)):
        if oLap(state_var.obstacle_list[j], player):
            state_var.obstacle_list[j].HP -= state_var.obs_HP
            if state_var.obstacle_list[j].HP <= 0 and j not in delobstacle_list: delobstacle_list.append(j)
            TF = True
    delObjf(state_var.obstacle_list, delobstacle_list)
    return TF

#그리기 함수
def drawInit(screen, state = 0):
    screen.fill(BLACK)
    # if state == 0:
    #     writeScore(screen, "게임 시작", 120, 300, color = WHITE, size = 40)
    #     writeScore(screen, "설정", 160, 460, color = WHITE, size = 40)
    if state == 0:
        writeScore(screen, "게임 시작", 140, 300, color = WHITE, size = 60)
        writeScore(screen, "설정", 160, 460, color = WHITE, size = 40)
        writeScore(screen, "게임 종료", 140, 620, color = WHITE, size = 40)
    elif state == 1: 
        writeScore(screen, "게임 시작", 140, 300, color = WHITE, size = 40)
        writeScore(screen, "설정", 160, 460, color = WHITE, size = 60)
        writeScore(screen, "게임 종료", 140, 620, color = WHITE, size = 40)
    elif state == 2: 
        writeScore(screen, "게임 시작", 140, 300, color = WHITE, size = 40)
        writeScore(screen, "설정", 160, 460, color = WHITE, size = 40)
        writeScore(screen, "게임 종료", 140, 620, color = WHITE, size = 60)
    return state

def drawStop(screen, state = 0):
    screen.fill(BLACK)
    if state == 0:
        writeScore(screen, "일시 정지", 150, 100, color = WHITE, size = 35)
        writeScore(screen, "게임 재개", 120, 300, color = WHITE, size = 60)
        writeScore(screen, "처음 으로", 140, 460, color = WHITE, size = 40)
        writeScore(screen, "게임 종료", 140, 620, color = WHITE, size = 40)
    elif state == 1:
        writeScore(screen, "일시 정지", 150, 100, color = WHITE, size = 35)
        writeScore(screen, "게임 재개", 120, 300, color = WHITE, size = 40)
        writeScore(screen, "처음 으로", 140, 460, color = WHITE, size = 60)
        writeScore(screen, "게임 종료", 140, 620, color = WHITE, size = 40)
    elif state == 2:
        writeScore(screen, "일시 정지", 150, 100, color = WHITE, size = 35)
        writeScore(screen, "게임 재개", 120, 300, color = WHITE, size = 40)
        writeScore(screen, "처음 으로", 140, 460, color = WHITE, size = 40)
        writeScore(screen, "게임 종료", 140, 620, color = WHITE, size = 60)
    return state
    
def initDisplay(screen, clock):
    time.sleep(0.2)
    state = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        key_event = pygame.key.get_pressed()
        if drawInit(screen, state) == 0 and (key_event[pygame.K_KP_ENTER]):
            break
        elif drawInit(screen, state) == 2 and (key_event[pygame.K_KP_ENTER]):
            exit(0)
        if key_event[pygame.K_DOWN] and state < 2:
            state +=1
            time.sleep(0.2)
        if key_event[pygame.K_UP] and state > 0:
            state -= 1
            time.sleep(0.2)
        pygame.display.flip()

def stopDisplay(screen, clock):
    state = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        key_event = pygame.key.get_pressed()
        if drawStop(screen, state) == 0 and key_event[pygame.K_KP_ENTER] or key_event[pygame.K_ESCAPE]:
            time.sleep(0.2)
            return 0
        elif drawStop(screen, state) == 1 and (key_event[pygame.K_KP_ENTER]):
            time.sleep(0.2)
            return 1
        elif drawStop(screen, state) == 2 and (key_event[pygame.K_KP_ENTER]):
            exit(0)
        elif key_event[pygame.K_DOWN] and state < 2:
            state +=1
            time.sleep(0.2)
        elif key_event[pygame.K_UP] and state > 0:
            state -= 1
            time.sleep(0.2)
        pygame.display.flip()

def drawGame(screen, player, state_var):
    screen.fill(BLACK)
    player.show(screen)
    delBoomissile_list = []

    for missile in state_var.missile_list:
        missile.show(screen)
    for obstacle in state_var.obstacle_list: 
        obstacle.show(screen)

    for i in range(len(state_var.boomissile_list)):
        state_var.boomissile_list[i].HP -= 1
        if state_var.boomissile_list[i].HP > 0:
            state_var.boomissile_list[i].show(screen)
        elif state_var.boomissile_list[i] not in state_var.boomissile_list: delBoomissile_list.append(state_var.boomissile_list[i])

    delObjf(delBoomissile_list, [i for i in range(len(delBoomissile_list))])

def mainKey_event(player, missile_Sound, count, screen, clock, state_var):
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
        newMissile(state_var, player)
        count = 0
    if key_event[pygame.K_ESCAPE]:
        pygame.mixer.music.stop()
        time.sleep(0.2)
        if stopDisplay(screen, clock):
            pygame.mixer.music.load(happythemeBGM[addressTF])
            pygame.mixer.music.play(-1)
            initDisplay(screen, clock) #Init display
            init_var = initVar()
            state_var.missile_list.clear(), state_var.obstacle_list.clear(), state_var.boomissile_list.clear()
            state_var.damageAmount = init_var.damageAmount
            state_var.obsCount = init_var.obsCount
            initPlayer(player) #player state init
        else:
            pygame.mixer.music.load(happythemeBGM[addressTF])
            pygame.mixer.music.play(-1)

#게임 오버
def ifGameOver(screen, player, size = 40):
    if player.HP <= 0:
        font = pygame.font.Font(fontFile[addressTF], size)
        text = font.render("GAME OVER!", True, RED)
        screen.blit(text,(80, SCREEN_HEIGHT/2))
        pygame.mixer.music.stop()
        pygame.mixer.Sound(gameOverSound[addressTF]).play()
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
    # 1. init game
    pygame.init()
    pygame.mixer.music.load(happythemeBGM[addressTF])
    pygame.mixer.music.play(-1)
    missile_Sound = pygame.mixer.Sound(laserGunSound[addressTF])
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    state_var = initVar()

    # 2. 게임창 옵션 설정
    title = "My Game"
    pygame.display.set_caption(title)

    # 3. 게임내 필요한 설정
    clock = pygame.time.Clock()
    count = 0 #미사일 지연

    initDisplay(screen, clock) #Init display
    player = obj()  # SpaceShip
    initPlayer(player) #player state init

    # 4. 메인 이벤트
    while True:
        count += 1
        # 4-1, FPS setting
        clock.tick(60)
        #check key_event
        mainKey_event(player, missile_Sound, count, screen, clock, state_var)

        # random new obstacle
        if state_var.obsCount/10: state_var.obs_SPEED = 2 + state_var.obsCount/10
        newobs(state_var)

        #move obj
        UPObjf(state_var.missile_list)
        DOWNObjf(state_var.obstacle_list)
    
        #delete obj when out
        outObj(state_var.obstacle_list, player)

        #충돌시 오브젝트 파괴
        if hitObs(state_var):  state_var.damageAmount += 1

        #if player when hit, down HP
        if hitPlayer(player, state_var): downHP(player)

        # 4-4, draw Display
        drawGame(screen, player, state_var)
        writeScore(screen, "총 딜량", 10, 0, count = state_var.damageAmount)
        writeScore(screen, "처리한 악마 수", 10, 20, count = state_var.obsCount)
        writeScore(screen, "player HP", SCREEN_WIDTH-140, 00, count = player.HP, color =  GREEN)
        if ifGameOver(screen, player): break
        
        # 4-5, Display update
        pygame.display.flip()

if __name__ == "__main__":
    main()