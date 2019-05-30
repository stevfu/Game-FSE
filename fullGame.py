#mainGame
from pygame import *
from math import *
from random import *
from datetime import datetime

RED=(255,0,0)   
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)
YELLOW=(255,255,0)

init()
#load pictures
mainMenu=image.load("FSE-Assets/mainscreen.jpg")
credMenu=image.load("FSE-Assets/credits.jpg")
instructMenu=image.load("FSE-Assets/instructions.jpg")
levelSelectMenu=image.load("FSE-Assets/levelSelect.jpg")
cross=image.load("FSE-Assets/cross.png")
hudimg=image.load("FSE-Assets/hud.jpg")
hudRect=image.load("FSE-Assets/hudRect.png")
readyPic=image.load("FSE-Assets/readyRect.jpg")
quitP=image.load("FSE-Assets/quitRect.png")
dialogueP=image.load("FSE-Assets/dialogueRect.png")
cancelPic=image.load("FSE-Assets/cancelRect.png")

txtFont=font.SysFont("Stencil",25)
txtFont2=font.SysFont("Stencil",17)

#loading maps
map1=image.load("FSE-Assets/Maps/map1.jpg")
map2=image.load("FSE-Assets/Maps/map2.jpg")
map3=image.load("FSE-Assets/Maps/map3.jpg")
map4=image.load("FSE-Assets/Maps/map4.jpg")
map5=image.load("FSE-Assets/Maps/map5.jpg")

#transform pictures
hud=transform.scale(hudimg,(500,75))
hudRects=transform.scale(hudRect,(200,95))
quitPic=transform.scale(quitP,(150,40))
crossPic=transform.scale(cross,(30,30))
dialoguePic=transform.scale(dialogueP,(400,110))

class enemyType:

    def __init__(self,name,speed,health):
        self.name=name
        self.speed=speed
        self.health=health
        self.filename="FSE-Assets/Enemies/"+name+".png"

infantry=enemyType('infantry',1.5,100)
transport=enemyType('transport',1.7,400)
motorcycle=enemyType('motorcycle',2,250)
lightTank=enemyType('lightTank',1,700)
heavyTank=enemyType('heavyTank',0.7,1000)
tankDestroyer=enemyType('tankDestroyer',0.8,900)

class towerType:

    def __init__(self,name,damage,price):
        self.name=name
        self.damage=damage
        self.price=price
        self.filename="FSE-Assets/Defenses/"+name+".png"

antiTank=towerType('antiTank',80,800)
bunker=towerType('bunker',100,1000)
fortress=towerType('fortress',150,1250)
heavyGun=towerType('heavyGun',200,1500)
heavyMG=towerType('heavyMG',35,500)
soldier=towerType('soldier',25,250)

def genEnemies(enemy):
    global pics
    pics=[]
    for i in enemy:
        img=[]
        img.append(image.load(i[2].filename))
        img.append(transform.rotate(image.load(i[2].filename),-90))
        img.append(transform.rotate(image.load(i[2].filename),-270))
        img.append(transform.rotate(image.load(i[2].filename),-180))
        pics.append(img)
    return pics

def moneyScore(screen):
    money=2000
    score=0
    txtMoney=txtFont.render("$"+str(money),True,RED)
    txtScore=txtFont.render(str(score),True,RED)
    screen.blit(txtMoney,(100,30))
    screen.blit(txtScore,(110,84))

def moveEnemy(screen,enemyList,enemy):
    frame=0
    count=0
    for i in enemy:
        if i[0]<315:
            i[0]+=i[2].speed
            frame=0
        if i[0]>=315 and i[1]>210:
            i[1]-=i[2].speed
            frame=2
        if i[1]<=210 and i[0]<720:
            i[0]+=i[2].speed
            frame=0
        if i[0]>=690 and i[1]<670:
            i[1]+=i[2].speed*2
            frame=1
        if i[1]>=670 and i[0]==690:
            i[0]+=i[2].speed*2
            frame=0
    
        screen.blit(enemyList[count][int(frame)],(i[0],i[1]))
        count+=1

def drawScene1(screen):
    screen.blit(map1,(0,0))
def drawScene2(screen):
    screen.blit(map2,(0,0))
def drawScene3(screen):
    screen.blit(map3,(0,0))
def drawScene4(screen):
    screen.blit(map4,(0,0))
def drawScene5(screen):
    screen.blit(map5,(0,0))

def hudElements(screen):
    screen.blit(hud,(550,20))
    screen.blit(hudRects,(20,20))
    screen.blit(dialoguePic,(600,600))

def prep(screen,towerPos):
    ready=False
    #rectangle defining
    readyRect=Rect(830,120,179,69)
    buyRects=[Rect(607,28,59,63),Rect(682,28,61,63),Rect(758,28,61,63),Rect(834,28,61,63),Rect(908,28,61,63),Rect(982,28,61,63)]

    txtD1=txtFont2.render("Basic Soldier - Cost: $250, Damage: 25",True,BLACK)
    txtD2=txtFont2.render("Machine Gun - Cost: $500, Damage: 35",True,BLACK)
    txtD3=txtFont2.render("Anti-Tank Gun - Cost: $800, Damage: 80",True,BLACK)
    txtD4=txtFont2.render("Bunker - Cost: $1000, Damage: 100",True,BLACK)
    txtD5=txtFont2.render("Fortress - Cost: $1250, Damage: 150",True,BLACK)
    txtD6=txtFont2.render("Heavy AT Gun - Cost: $1500, Damage: 200",True,BLACK)
    towerDescription=[txtD1,txtD2,txtD3,txtD4,txtD5,txtD6]
    
    ##generating defense images
    defenses=[soldier,heavyMG,antiTank,bunker,fortress,heavyGun]
    defensePics=[]
    for i in defenses:
        defensePics.append(image.load(i.filename))
              
    draw.rect(screen,RED,readyRect,2)
    screen.blit(readyPic,(830,120))
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    
    if readyRect.collidepoint(mx,my):
        draw.rect(screen,(255,255,0),readyRect,2)
        if mb[0]==1:
            ready=True

    placeCond=False
    defC="none"
    
    for i in range(len(buyRects)):
        if buyRects[i].collidepoint(mx,my):
            draw.rect(screen,YELLOW,buyRects[i],2)
            #screen.blit(defensePics[i],(630,630))
            screen.blit(towerDescription[i],(620,630))
            if mb[0]==1:
                placeCond=True
                defC=int(i)

    if placeCond==True:
        for i in towerPos:
            draw.rect(screen,RED,i,3)

def lev1():
    ready=False
    running=True
    myclock=time.Clock()
    mixer.init()
    mixer.music.load("FSE-Assets/sound/bgMusic.mp3")
    mixer.music.play(-1)
    quitRect=Rect(260,25,150,40)
    towerPos1=[Rect(115,273,50,50),Rect(264,114,50,50),Rect(319,242,50,50),Rect(217,529,50,50),Rect(388,342,50,50),
            Rect(570,342,50,50),Rect(750,342,50,50),Rect(418,503,50,50),Rect(598,503,50,50),Rect(778,503,50,50)]
    while running:
        myclock.tick(60)
        drawScene1(screen)
        hudElements(screen)
        moneyScore(screen)
        screen.blit(quitPic,(260,25))
        draw.rect(screen,BLACK,quitRect,2)
        for evt in event.get():
            if evt.type==QUIT:
                running=False
                return "exit"
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        if quitRect.collidepoint(mx,my):
            draw.rect(screen,RED,quitRect,3)
            if mb[0]==1:
                running=False
                return "levelSelect"
        #genPics(enemy)
        if ready==False:
            prep(screen,towerPos1)

        display.flip()
    return "main"

def lev2():
    ready=False
    running=True
    myclock=time.Clock()
    mixer.init()
    mixer.music.load("FSE-Assets/sound/bgMusic.mp3")
    mixer.music.play(-1)
    quitRect=Rect(260,25,150,40)
    towerPos2=[Rect(75,430,50,50),Rect(225,430,50,50),Rect(225,300,50,50),Rect(225,125,50,50),Rect(425,125,50,50),
            Rect(600,125,50,50),Rect(425,300,50,50),Rect(600,300,50,50),Rect(750,275,50,50),Rect(825,375,50,50)]
    while running:
        myclock.tick(60)
        drawScene2(screen)
        hudElements(screen)
        moneyScore(screen)
        screen.blit(quitPic,(260,25))
        draw.rect(screen,BLACK,quitRect,2)
        for evt in event.get():
            if evt.type==QUIT:
                running=False
                return "exit"
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        if quitRect.collidepoint(mx,my):
            draw.rect(screen,RED,quitRect,3)
            if mb[0]==1:
                running=False
                return "levelSelect"
        #genPics(enemy)
        prep(screen,towerPos2)
        #moveEnemy(screen,pics,enemy)
        display.flip()
    return "main"

def lev3():
    ready=False
    running=True
    myclock=time.Clock()
    mixer.init()
    mixer.music.load("FSE-Assets/sound/bgMusic.mp3")
    mixer.music.play(-1)
    quitRect=Rect(260,25,150,40)
    towerPos3=[Rect(52,391,50,50),Rect(200,391,50,50),Rect(190,563,50,50),Rect(274,294,50,50),Rect(274,136,50,50),Rect(450,136,50,50),
            Rect(474,325,50,50),Rect(630,305,50,50),Rect(800,305,50,50),Rect(580,136,50,50),Rect(700,136,50,50)]
    while running:
        myclock.tick(60)
        drawScene3(screen)
        hudElements(screen)
        moneyScore(screen)
        screen.blit(quitPic,(260,25))
        draw.rect(screen,BLACK,quitRect,2)
        for evt in event.get():
            if evt.type==QUIT:
                running=False
                return "exit"
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        if quitRect.collidepoint(mx,my):
            draw.rect(screen,RED,quitRect,3)
            if mb[0]==1:
                running=False
                return "levelSelect"
        #genPics(enemy)
        prep(screen,towerPos3)
        #moveEnemy(screen,pics,enemy)
        display.flip()
    return "main"

def lev4():
    ready=False
    running=True
    myclock=time.Clock()
    mixer.init()
    mixer.music.load("FSE-Assets/sound/bgMusic.mp3")
    mixer.music.play(-1)
    quitRect=Rect(260,25,150,40)
    towerPos4=[Rect(107,355,50,50),Rect(193,190,50,50),Rect(331,298,50,50),Rect(331,423,50,50),Rect(457,472,50,50),
            Rect(241,647,50,50),Rect(689,429,50,50),Rect(495,260,50,50),Rect(686,240,50,50),Rect(820,409,50,50)]
    while running:
        myclock.tick(60)
        drawScene4(screen)
        hudElements(screen)
        moneyScore(screen)
        screen.blit(quitPic,(260,25))
        draw.rect(screen,BLACK,quitRect,2)
        for evt in event.get():
            if evt.type==QUIT:
                running=False
                return "exit"
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        if quitRect.collidepoint(mx,my):
            draw.rect(screen,RED,quitRect,3)
            if mb[0]==1:
                running=False
                return "levelSelect"
        #genPics(enemy)
        prep(screen,towerPos4)
        #moveEnemy(screen,pics,enemy)
        display.flip()
    return "main"

def lev5():
    ready=False
    running=True
    myclock=time.Clock()
    mixer.init()
    mixer.music.load("FSE-Assets/sound/bgMusic.mp3")
    mixer.music.play(-1)
    quitRect=Rect(260,25,150,40)
    draw.rect(screen,BLACK,quitRect,2)
    towerPos5=[Rect(30,197,50,50),Rect(232,173,50,50),Rect(382,173,50,50),Rect(228,337,50,50),Rect(332,379,50,50),Rect(332,520,50,50),
            Rect(525,262,50,50),Rect(525,409,50,50),Rect(645,409,50,50),Rect(459,589,50,50),Rect(815,409,50,50)]
    while running:
        myclock.tick(60)
        drawScene5(screen)
        hudElements(screen)
        moneyScore(screen)
        screen.blit(quitPic,(260,25))
        for evt in event.get():
            if evt.type==QUIT:
                running=False
                return "exit"
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        print(mx,my)

        if quitRect.collidepoint(mx,my):
            draw.rect(screen,RED,quitRect,3)
            if mb[0]==1:
                running=False
                return "levelSelect"
        #genPics(enemy)
        prep(screen,towerPos5)
        #moveEnemy(screen,pics,enemy)
        display.flip()
    return "main"

def creds():
    global mx,my
    mixer.init()
    mixer.music.load("FSE-Assets/sound/sovietTheme.mp3")
    mixer.music.play()
    running=True
    while running:
        screen.blit(credMenu,(0,0))
        screen.blit(crossPic,(960,50))
        backButton=Rect(950,40,50,50)
        draw.rect(screen,BLACK,backButton,3)
        for evnt in event.get():
            if evnt.type==QUIT:
                running=False
                return "exit"
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        if backButton.collidepoint(mx,my):
            draw.rect(screen,YELLOW,backButton,3)
            if mb[0]==1:
                running=False
        display.flip()
    return "main"

def instructions():
    mixer.init()
    mixer.music.load("FSE-Assets/sound/menuMusic2.mp3")
    mixer.music.play(-1)
    running=True
    while running:
        screen.blit(instructMenu,(0,0))
        screen.blit(crossPic,(960,50))
        backButton=Rect(950,40,50,50)
        draw.rect(screen,BLACK,backButton,3)
        for evnt in event.get():
            if evnt.type==QUIT:
                running=False
                return "exit"
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        if backButton.collidepoint(mx,my):
            draw.rect(screen,YELLOW,backButton,3)
            if mb[0]==1:
                running=False
        display.flip()
    return "main"

def levelSelect():
    mixer.init()
    mixer.music.load("FSE-Assets/sound/menuMusic2.mp3")
    mixer.music.play(-1)
    levelRects=[Rect(122,260,240,160),Rect(407,262,250,160),Rect(696,262,250,160),Rect(257,493,240,160),Rect(564,492,240,160)]
    levels=["lev1","lev2","lev3","lev4","lev5"]
    running=True
    while running:
        for evnt in event.get():
            if evnt.type==QUIT:
                running=False
                return "exit"
        screen.blit(levelSelectMenu,(0,0))
        screen.blit(crossPic,(960,50))
        backButton=Rect(950,40,50,50)
        draw.rect(screen,BLACK,backButton,3)

        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        if backButton.collidepoint(mx,my):
            draw.rect(screen,YELLOW,backButton,3)
            if mb[0]==1:
                running=False
        for i in range(len(levelRects)):
            if levelRects[i].collidepoint(mx,my):
                draw.rect(screen,RED,levelRects[i],3)
                if mb[0]==1:
                    return levels[i]
        display.flip()
    return "main"
    
def main():
    mixer.init()
    mixer.music.load("FSE-Assets/sound/menuMusic.mp3")
    mixer.music.play(-1)
    buttons=[Rect(57,294,210,47),Rect(57,370,270,49),Rect(57,448,170,49)]
    vals=["levelSelect","instructions","credits"]
    running=True
    click=False
    while running:
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        for evnt in event.get():
            if evnt.type==QUIT:
                return "exit"
            if evnt.type==MOUSEBUTTONDOWN:
                click=True
            if evnt.type==MOUSEBUTTONUP:
                click=False
        screen.blit(mainMenu,(0,0))
        backButton=Rect(950,650,50,50)
        musicButton=Rect(870,650,50,50)
        draw.rect(screen,RED,backButton,3)
        draw.rect(screen,RED,musicButton,3)
        screen.blit(crossPic,(960,660))
        
        for i in range(len(buttons)):
            draw.rect(screen,RED,buttons[i],3)
            if buttons[i].collidepoint(mx,my):
                draw.rect(screen,(255,255,0),buttons[i],3)
                if mb[0]==1 and click==False:
                    return vals[i]
        if backButton.collidepoint(mx,my):
            draw.rect(screen,YELLOW,backButton,3)
            if mb[0]==1:
                return "exit"
        display.flip()

size=width,height=1050,750
screen=display.set_mode(size)
display.set_caption("The Great Patriotic War")
iconPic=image.load("FSE-Assets/icon.png")
display.set_icon(iconPic)
running=True
current="main"

while current!="exit":
    if current=="main":
        current=main()
    if current=="levelSelect":
        current=levelSelect()
    if current=="instructions":
        current=instructions()
    if current=="credits":
        current=creds()
    if current=="lev1":
        current=lev1()
    if current=="lev2":
        current=lev2()
    if current=="lev3":
        current=lev3()
    if current=="lev4":
        current=lev4()
    if current=="lev5":
        current=lev5()

quit()