import pgzrun
import pygame
import math
import random

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
        self.czy_aktywna=True
    def draw(self):
        if self.czy_aktywna==True:
            self.pocisk.draw()
    def update(self):
        self.pocisk.x+=math.cos(math.radians(self.kat))*self.PREDKOSC_POCISKU
        self.pocisk.y-=math.sin(math.radians(self.kat))*self.PREDKOSC_POCISKU
    def collidepoint(self,pos):
        if self.pocisk.collidepoint(pos):
            return True
        return False

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
            if i.x<WIDTH and i.y>0 and i.czy_aktywna==True:
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

class Wybuch:
    def __init__(self,x,y):
        self.wybuch=Actor("explosion1",(x,y))
        self.klatka=0
        self.aktywny=True
    def draw(self):
        if self.aktywny==True:
            self.wybuch.draw()
    def update(self):
        if self.klatka<5:
            self.wybuch.image="explosion1"
        elif self.klatka<10:
            self.wybuch.image="explosion2"
        elif self.klatka<15:
            self.wybuch.image="explosion3"
        elif self.klatka<20:
            self.wybuch.image="explosion4"
        elif self.klatka<25:
            self.wybuch.image="explosion5"
        elif self.klatka<30:
            self.wybuch.image="explosion6"
        elif self.klatka<35:
            self.wybuch.image="explosion7"
        elif self.klatka<40:
            self.wybuch.image="explosion8"
        elif self.klatka<45:
            self.wybuch.image="explosion9"
        elif self.klatka<50:
            self.wybuch.image="explosion10"
        elif self.klatka<55:
            self.wybuch.image="explosion11"
        else:
            self.wybuch.image="explosion12"
        self.klatka+=1
        if self.klatka>60:
            self.aktywny=False


class Beczka:
    def __init__(self,x,y):
        self.beczka=Actor("beczka",(x,y))
        self.czy_aktywna=True
    def draw(self):
        if self.czy_aktywna==True:
            self.beczka.draw()
    
    def update(self):
        pass
    

class Gra:
    def __init__(self):
        self.czolg=Czolg(100,HEIGHT-146)
        self.wybuchy=[]
        self.beczki=[Beczka(random.randint(200,600),HEIGHT-146),
                    Beczka(random.randint(600,1200),HEIGHT-146),
                    Beczka(random.randint(1200,1600),HEIGHT-146)]
        self.licznik=0
    def draw(self):
        screen.clear()
        screen.fill("#66e6ff")
        for i in range(WIDTH//64 + 1):
            screen.blit("grass",(i*64,HEIGHT-64))
        self.czolg.draw()
        for i in self.beczki:
            i.draw()
        screen.draw.text(
        str(self.licznik),
        midright=(screen.width - 50, 50),
        color="orange",
        fontsize=90)
        for i in self.wybuchy:
            i.draw()

    def update(self):
    
        if keyboard.RIGHT:
            self.czolg.prawo()
        if keyboard.LEFT:
            self.czolg.lewo()
        if keyboard.UP:
            self.czolg.turretup()
        if keyboard.DOWN:
            self.czolg.turretdown()
        if keyboard.SPACE:
            self.czolg.wystrzel()

        for i in self.czolg.wyrzutnia.pociski:
            for j in self.beczki:
                if j.beczka.collidepoint(i.pocisk.pos):
                    j.czy_aktywna=False
                    i.czy_aktywna=False
                    self.licznik+=10
                    self.wybuchy.append(Wybuch(i.pocisk.pos[0],i.pocisk.pos[1]))
                    self.beczki.append(Beczka(random.randint(200,1600),random.randint(200,HEIGHT-146)))
        tmp=[]
        for i in self.beczki:
            if i.czy_aktywna==True:
                tmp.append(i)
        self.beczki=tmp
        self.czolg.update()
        for i in self.wybuchy:
            i.update()

 
gra=Gra()
def draw():
    gra.draw()

def update():
    gra.update()


pgzrun.go()