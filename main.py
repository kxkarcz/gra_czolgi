import pgzrun
import pygame
import math

pygame.display.set_mode((0,0),pygame.RESIZABLE)
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h


class Pocisk:
    def __init__(self,x,y,kat):
        self.x=x+math.cos(math.radians(kat))*48
        self.y=y-math.sin(math.radians(kat))*48
        self.kat=kat
        self.pocisk=Actor("bullet",bottomleft=(self.x,self.y))
        self.pocisk.angle=kat
        self.PREDKOSC_POCISKU=10
    def draw(self):
        self.pocisk.draw()
    def update(self):
        self.pocisk.x+=math.cos(math.radians(self.kat))*self.PREDKOSC_POCISKU
        self.pocisk.y-=math.sin(math.radians(self.kat))*self.PREDKOSC_POCISKU

class Wyrzutnia:
    def __init__(self):
        self.pociski=[]
        self.blokada_strzalu=False
    def zwolnienie_blokady(self):
        self.blokada_strzalu=False
    def wystrzel(self,kat,x,y):
        if(self.blokada_strzalu==False):
            self.pociski.append(Pocisk(x,y,kat))
            self.blokada_strzalu=True
            clock.schedule_unique(self.zwolnienie_blokady,1.0)
    def draw(self):
        for i in self.pociski:
            i.draw()
    def update(self):
        tmp=[]
        for i in self.pociski:
            if i.x<WIDTH and i.y>0:
                tmp.append(i)
        self.pociski=tmp
        for i in self.pociski:
            i.update()




class Czolg:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.body=Actor("tankbody",(self.x,self.y))
        self.track=Actor("tanktrack",(self.x,self.y+50))
        self.turret=Actor("tankturret",(self.x+15,self.y-20),anchor=("left","bottom"))
        self.wyrzutnia=Wyrzutnia()
        self.PREDOSC_PORUSZANIA_CZOLGU=2
        self.DELTA_KAT=2
        self.MIN_KAT_TURRET=0
        self.MAX_KAT_TURRET=80
    def draw(self):
        self.turret.draw()
        self.track.draw()
        self.body.draw()
        self.wyrzutnia.draw()
    def prawo(self):
        if self.body.x<WIDTH-200:
            self.body.x+=self.PREDOSC_PORUSZANIA_CZOLGU
            self.track.x+=self.PREDOSC_PORUSZANIA_CZOLGU
            self.turret.x+=self.PREDOSC_PORUSZANIA_CZOLGU

    def lewo(self):
        if self.body.x>83:
            self.body.x -= self.PREDOSC_PORUSZANIA_CZOLGU
            self.track.x -= self.PREDOSC_PORUSZANIA_CZOLGU
            self.turret.x -= self.PREDOSC_PORUSZANIA_CZOLGU
    def turretup(self):
        if self.turret.angle>=self.MIN_KAT_TURRET and self.turret.angle<=self.MAX_KAT_TURRET:
            self.turret.angle+=self.DELTA_KAT
        if self.turret.angle>self.MAX_KAT_TURRET:
            self.turret.angle=self.MAX_KAT_TURRET
    def turretdown(self):
        if self.turret.angle>=self.MIN_KAT_TURRET and self.turret.angle<=self.MAX_KAT_TURRET:
            self.turret.angle-=self.DELTA_KAT
        if self.turret.angle<self.MIN_KAT_TURRET:
            self.turret.angle=self.MIN_KAT_TURRET
    def wystrzel(self):
        self.wyrzutnia.wystrzel(self.turret.angle,self.turret.x,self.turret.y)
    def update(self):
        self.wyrzutnia.update()

czolg=Czolg(200,HEIGHT-146)

def draw():
    screen.clear()
    screen.fill("#66e6ff")
    for i in range(WIDTH//64 + 1):
        screen.blit("grass",(i*64,HEIGHT-64))
    czolg.draw()


def update():
    if keyboard.RIGHT:
        czolg.prawo()
    if keyboard.LEFT:
        czolg.lewo()
    if keyboard.UP:
        czolg.turretup()
    if keyboard.DOWN:
        czolg.turretdown()
    if keyboard.SPACE:
        czolg.wystrzel()
    czolg.update()

pgzrun.go()