####################################
# 更新日期：2021年07月03日
# 版本：1.0.0
# 作者：gfdgd xi
####################################
import sys
import time
import random
import pygame
import ctypes
import inspect
import threading
import pygame.constants

def RandomTNT():
    global moneySudo
    global TNTPlace
    global close
    global width
    while True:
        TNTPlace = [random.randint(0, width - 100), random.randint(0, height)]
        screen.blit(tnt, TNTPlace)  # 每次循环都重绘屏幕
        time.sleep(TNTSudu)
        if close:
            break

def RandomMoney():
    global moneyPlace
    global moneySudo
    global close
    global width
    while True:
        moneyPlace = [random.randint(0, width - 100), random.randint(0, height)]
        screen.blit(money, moneyPlace)  # 每次循环都重绘屏幕
        time.sleep(moneySudo)
        if close:
            break

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

def stop_thread(thread):
    """终止线程"""
    _async_raise(thread.ident, SystemExit)

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            # pass
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as err:
        print(err)
close = False
pygame.init()
screen = pygame.display.set_mode((1024, 768), 0, 8)
background = (0, 100, 250)
pygame.display.set_caption("Demo")
height = 768
width = 1024
mo = pygame.image.load("bird.png")
mo = pygame.transform.scale(mo, (272, 224))
tnt = pygame.image.load("TNT.png")
tnt = pygame.transform.scale(tnt, (100, 100))
money = pygame.image.load("money.png")
money = pygame.transform.scale(money, (50, 50))
amn = mo.get_rect()
tntamn = tnt.get_rect()
moneyamn = money.get_rect()
TNTPlace = [random.randint(0, width - 100), random.randint(0, height)]
moneyPlace = [random.randint(0, width - 100), random.randint(0, height)]
mo1 = mo
speed = [100, 0]
min = 2000
moneyNumber = 0
dengji = 1
TNTSudu = 30
planmoney = 10
moneySudo = 60
fontObj2 = pygame.font.SysFont('宋体', 20)
textSurfaceObj2 = fontObj2.render("Money: {}/{}, Min: {}ms， Dengji: {}".format(str(moneyNumber), str(planmoney), str(min), str(dengji)), False, (250, 250, 250))
textRectObj2 = textSurfaceObj2.get_rect()
randomtnt = threading.Thread(target=RandomTNT)
randomtnt.start()
randommoney = threading.Thread(target=RandomMoney)
randommoney.start()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = True
            stop_thread(randommoney)
            stop_thread(randomtnt)
            sys.exit(0)
    suDu = 5
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_d]:
        if speed[0] > width - 224:
            continue
        speed[0] += suDu * 2
        mo1 = pygame.transform.flip(mo, True, False)
    elif pressed_keys[pygame.K_a]:
        if speed[0] < 0:
            continue
        speed[0] -= suDu * 2
        mo1 = mo
    elif pressed_keys[pygame.K_w]:
        if speed[1] < 0:
            continue
        speed[1] -= suDu * 2
    elif pressed_keys[pygame.K_s]:
        if speed[1] > height - 224:
            continue
        speed[1] += suDu * 2
    if pressed_keys[pygame.K_ESCAPE]:
        close = True
        stop_thread(randommoney)
        stop_thread(randomtnt)
        sys.exit(0)
    if pressed_keys[pygame.K_RIGHT]:
        if speed[0] > width - 224:
            continue
        speed[0] += suDu
        mo1 = pygame.transform.flip(mo, True, False)
    elif pressed_keys[pygame.K_LEFT]:
        if speed[0] < 0:
            continue
        speed[0] -= suDu
        mo1 = mo
    elif pressed_keys[pygame.K_UP]:
        if speed[1] < 0:
            continue
        speed[1] -= suDu
    elif pressed_keys[pygame.K_DOWN]:
        if speed[1] > height - 224:
            continue
        speed[1] += suDu
    if speed[0] < TNTPlace[0] and speed[0] + 272 > TNTPlace[0] and speed[1] < TNTPlace[1] and speed[1] + 224 > TNTPlace[1]:
        if min > 0:
            min = min - 1
        else:
            close = True
            stop_thread(randommoney)
            stop_thread(randomtnt)
            sys.exit(0)
    if speed[0] < moneyPlace[0] and speed[0] + 272 > moneyPlace[0] and speed[1] < moneyPlace[1] and speed[1] + 224 > moneyPlace[1]:
        moneyNumber = moneyNumber + 1
        moneyPlace = [random.randint(0, width - 100), random.randint(0, height)]
        if moneyNumber > planmoney:
            if dengji < 10:
                dengji = dengji + 1
                TNTSudu = TNTSudu / 2
                moneySudo = moneySudo / 2
                min = min + 1000
                planmoney = int(planmoney * 1.4)
            else:
                print("Win!")
                close = True
                stop_thread(randommoney)
                stop_thread(randomtnt)
                sys.exit(0)
    textSurfaceObj2 = fontObj2.render(
        "Money: {}/{}, Min: {}ms， Dengji: {}".format(str(moneyNumber), str(planmoney), str(min), str(dengji)), False,
        (250, 250, 250))
    screen.fill(background)
    screen.blit(textSurfaceObj2, textRectObj2)
    screen.blit(tnt, TNTPlace)
    screen.blit(money, moneyPlace)
    amn = amn.move(speed)
    screen.blit(mo1, speed)
    # 让最近绘制屏幕可见
    pygame.display.flip()