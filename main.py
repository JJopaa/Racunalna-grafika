from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin, cos, sqrt
import time
import random
import pygame
from random import randint
import numpy
from numpy import *
from PIL import Image


BLACK = (0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0)
GREEN = (0.0, 1.0, 0.0)
BLUE = (0.0, 0.0, 1.0)
MAGENTA = (1.0, 0.0, 1.0)
YELLOW = (1.0, 0.5, 0.0)
PINK = (1.0,0.43,0.78)
CORAL = (1.0,0.498039,0.0)
KHAKI = (0.6, 0.4, 0.4)
BROWN = (0.9, 0.4, 0.5)
GRAY = (0.4, 0.4, 0.4)
BRONZE=(0.55,0.47,0.14)
DARK_WOOD = (0.35,0.16,0.14)
SKY_BLUE = (0.196078,0.6,0.8)
LIGHT_BLUE = (0.54902,0.547059,0.78)
DARK_GREEN = (0.137255,0.556863,0.137255)
SPRING_GREEN = (0.5,1.0,0.0)
colors = [RED,GREEN,BLUE,MAGENTA,YELLOW,PINK,CORAL,SPRING_GREEN,KHAKI,BRONZE]

ESCAPE = b'\033'
SPACE = b'\040'


rtri_m = 0
v_m = 0.05

stop = True


rotate_brod = 0
v_brod = 0.01

class GameState:
    currState = 1
    PLAY = 1
    COLLISION = 2
    GAME_OVER = 3
    QUIT = 4
    collisionTime = 0

    @staticmethod
    def processState():
        global stop
        if GameState.currState == GameState.QUIT:
            sys.exit()
        if GameState.currState == GameState.GAME_OVER:
            Score.clean()
            brod.postavi()
            for s in smece:
                s.postavi_new()
            for p in planeti:
                p.postavi_new()
            for a in asteroidi:
                a.postavi_new()
            for s in svemirci:
                s.postavi_new()

            for u in udaljeni:
                u.postavi_new()
            stop = True
            GameState.currState = GameState.PLAY

        Sky.draw()
        
        brod.update()
        for s in smece:
            s.update()
        for p in planeti:
            p.update()
        for a in asteroidi:
            a.update()
        for s in svemirci:
            s.update()

        for u in udaljeni:
            u.update()

        Score.update()
        skupi()
        sudar_svemirac()
        sudar_aster()
class Score:
    currScore = 0
    highScore = 0
    @staticmethod
    def clean():
        Score.highScore = max(Score.highScore, Score.currScore)
        Score.currScore = 0

    @staticmethod
    def update():
        glDisable(GL_LIGHTING)
        glColor(1, 1, 1, .5)
        Score.drawText("Rezultat: " + str(Score.currScore), 15, 670, .35)
        Score.drawText("Najbolji rezultat: " + str(Score.highScore), 30, 645, .15, 2)
        
        if GameState.currState == GameState.COLLISION:
            glClearColor(0, 0, 0, 1)
            glClear(GL_COLOR_BUFFER_BIT)
            if Score.currScore > Score.highScore:
                glColor3f(1, 0, 0)
                Score.drawText("  Novi rekord!  ", 300, Display.HEIGHT * 6 / 7, 0.6, 4)
                glColor(1, 1, 1, .5)
            Score.drawText("Tvoj rezultat : " + str(Score.currScore), 450 ,Display.HEIGHT * 3/4, 0.4, 2 )
            Score.drawText("Igra gotova !", Display.WIDTH / 2 - 350, Display.HEIGHT / 2, 1, 8)
            glColor3f(0, 0.5, 0.7)
            Score.drawText("  Pritisni 'p' za novu igru", 500, Display.HEIGHT / 4, 0.15, 2)
            Score.drawText("Pritisni 'q' za izlazak iz igre", 500, Display.HEIGHT / 6, 0.15, 2)
  
        glEnable(GL_LIGHTING)


    @staticmethod
    def drawText(string, xShift=0, yShift=0, scale=1, lineWidth=4):
        glLineWidth(lineWidth)
        Display.orthoProjection()
        glPushMatrix()
        glLoadIdentity()
        glTranslate(xShift, yShift, 0)
        glScale(scale, scale, 1)
        string = string.encode()
        for c in string:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
        glPopMatrix()
        Display.perProjection()
class Sky:
    width = height = 0
    centerX = 0
    centerY = 0
    length = 3500
    skyspeed = 0.5
    texture = None
    @staticmethod
    def init():
        Sky.texture = glGenTextures(1)
        imgLoad = pygame.image.load("SKY.jpg")
        imgRaw = pygame.image.tostring(imgLoad, "RGB", 1)
        Sky.width = imgLoad.get_width()
        Sky.height = imgLoad.get_height()
        glBindTexture(GL_TEXTURE_2D, Sky.texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, Sky.width, Sky.height, 0, GL_RGB, GL_UNSIGNED_BYTE, imgRaw)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 3, Sky.width, Sky.height, GL_RGB, GL_UNSIGNED_BYTE, imgRaw)

    @staticmethod
    def draw():
        glDisable(GL_LIGHTING)
        glColor(1, 1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, Sky.texture)
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glTexCoord(Sky.centerX / Sky.width, Sky.centerY / Sky.height)
        glVertex(-500, -500, brod.z_kor - 500)

        glTexCoord((Sky.centerX + Sky.length) / Sky.width, Sky.centerY / Sky.height)
        glVertex(500, -500, brod.z_kor - 500)

        glTexCoord((Sky.centerX + Sky.length) / Sky.width, (Sky.centerY + Sky.length) / Sky.height)
        glVertex(500, 500, brod.z_kor - 500)

        glTexCoord(Sky.centerX / Sky.width, (Sky.centerY + Sky.length) / Sky.height)
        glVertex(-500, 500, brod.z_kor - 500)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        Sky.centerY += Sky.skyspeed
        glEnable(GL_LIGHTING)

class Brod:
    def __init__(self, y, x, z):
        self.x_kor = x
        self.y_kor = y
        self.z_kor = z
        self.currX = 0
        self.speed = 0.5
        self.goRight = self.goLeft = False
    
    def postavi(self):
        self.x_kor = self.y_kor = self.z_kor = 0
        self.goRight = self.goLeft = False
        self.currX = 0
        self.speed = 0.5
    
    def update(self):
        global stop, rotate_brod
        
        if GameState.currState == GameState.PLAY: 
            if self.goRight:  
                self.x_kor += self.speed
                if self.x_kor >= self.currX:
                    self.goRight = False
                    self.x_kor = self.currX
            if self.goLeft: 
                self.x_kor -= self.speed
                if self.x_kor <= self.currX:
                    self.goLeft = False
                    self.x_kor = self.currX
        

        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, GRAY)
        glTranslated(self.x_kor, self.y_kor, self.z_kor)
        glRotatef(90, 1, 0, 0)
        glutSolidTorus(0.6, 1.2, 2, 150)
        glutSolidTorus(0.3, 0.6, 4, 150)

        if not stop:
            #prsten oko broda koji se vrti kada brod nije u mirovanju
            glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, RED)
            glRotatef(rotate_brod, 0, 0, 1)
            glutWireTorus(0.15, 2, 2, 50)  
            rotate_brod += 0.4           
        glPopMatrix()

      
        if GameState.currState == GameState.PLAY and stop == False:
            self.z_kor -= self.speed
            self.speed = min(self.speed + 0.0001, 1)
        if sudar() and GameState.currState == GameState.PLAY:
            GameState.collisionTime = time.time()
            GameState.currState = GameState.COLLISION

        
        
class Otpad:
    def __init__(self,c,x,z):
        self.color = c
        self.x = x
        self.y = 0
        self.z = z
        self.radijus = 0.4
        self.rotate = 0
    
    #metoda kojom postavljamo nove nasumicne vrijednosti koordinata i boja
    def postavi(self):  
        self.y = 0
        x_cor = [-4, 0, 4]
        rand_x = randint(0,2)
        self.x = x_cor[rand_x]
        self.z = brod.z_kor - 500
        colors = (DARK_GREEN,SPRING_GREEN)
        wgb = randint(0,1)
        self.color = colors[wgb]
    
    def postavi_new(self):
        self.y = 0
        x_cor = [-4, 0, 4]
        z_cor = [-30, -60, -270, -420]
        rand_x = randint(0,2)
        rand_z = randint(0,3)
        self.x = x_cor[rand_x]
        self.z = z_cor[rand_z]
        colors = (DARK_GREEN,SPRING_GREEN)
        wgb = randint(0,1)
        self.color = colors[wgb]
        self.rotate = 0

    def update(self):
        global stop
        glPushMatrix()
        glEnable(GL_COLOR_MATERIAL)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        glTranslated(self.x, self.y, self.z)
        if GameState.currState == GameState.PLAY:
            if(self.z >= brod.z_kor + 50 and stop == False):
                self.postavi()
                
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        glRotatef(90, 1, 0, 0)
        glRotatef(30, 0, 0, 1)
        glRotatef(self.rotate, 0, 1, 0)

        glutSolidCylinder(0.8, 2, 30, 100)
        self.rotate += 0.3
        glPopMatrix()

class PlasticniOtpad:
    def __init__(self,c,x,z):
        self.color = c
        self.x = x
        self.y = 0
        self.z = z
        self.radijus = 0.4
        self.rotate = 0
    
    #metoda kojom postavljamo nove nasumicne vrijednosti koordinata i boja
    def postavi(self):  
        self.y = 0
        x_cor = [-4, 0, 4]
        rand_x = randint(0,2)
        self.x = x_cor[rand_x]
        self.z = brod.z_kor - 500
    
    def postavi_new(self):
        self.y = 0
        x_cor = [-4, 0, 4]
        z_cor = [-30, -60, -270, -420]
        rand_x = randint(0,2)
        rand_z = randint(0,3)
        self.x = x_cor[rand_x]
        self.z = z_cor[rand_z]
        self.rotate = 0

    def update(self):
        global stop
        glPushMatrix()
        glEnable(GL_COLOR_MATERIAL)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        glTranslated(self.x, self.y, self.z)
        if GameState.currState == GameState.PLAY:
            if(self.z >= brod.z_kor + 50 and stop == False):
                self.postavi()    
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        glRotatef(90, 1, 0, 0)
        glRotatef(30, 0, 0, 1)
        glRotatef(self.rotate, 0, 1, 0) 
        glutSolidCylinder(0.4, 1.4, 30, 100)
        glutSolidCylinder(0.2, 1.6, 30, 100)
        self.rotate += 0.3
        glPopMatrix()

class PlanetSaPrstenom:
    def __init__(self,c_pl,c_pr,h,x,z):
        self.color_pl = c_pl
        self.color_pr = c_pr
        self.x = x
        self.y = h
        self.z = z
        self.radijus = 4

    #metoda kojom postavljamo nove nasumicne vrijednosti koordinata i boja
    def postavi(self):
        self.y = 0
        x_cor = [-4, 4]
        rand_x = randint(0,1)
        self.x = x_cor[rand_x]
        self.z = brod.z_kor - 500
        self.color_pl = colors[randint(0,9)]
        
    def postavi_new(self):
        self.y = 0
        x_cor = [-4, 4]
        rand_x = randint(0,1)
        self.x = x_cor[rand_x]
        self.z = -360
        self.color_pl = colors[randint(0,9)]

    def update(self):   
        global stop
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color_pl)
        glTranslated(self.x, self.y, self.z)

        if GameState.currState == GameState.PLAY: #ako je igra jos traje
            if(self.z >= brod.z_kor + 100): #ako igrac prodje planet
                self.postavi()  #postave se nove nasumicne vrijednosti koordinata i boje planeta

        glutSolidSphere(3, 100, 100)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color_pr)
        glRotatef(60, 1, 0, 0)
        glutWireTorus(0.2, 5, 2, 100)
        glutWireTorus(0.4, 5, 2, 100)
        glutWireTorus(0.8, 5, 2, 100)
        glPopMatrix()
    
class UdaljeniPlanetSaPrstenom:
    def __init__(self,c_pl,c_pr,h,x,z):
        self.color_pl = c_pl
        self.color_pr = c_pr
        self.x = x
        self.y = h
        self.z = z
        self.radijus = 4

    #metoda kojom postavljamo nove nasumicne vrijednosti koordinata i boja
    def postavi(self):
        self.y = 0
        if self.x < 0:
            x_cor = [-100, -80, -60]
        elif self.x > 0:
            x_cor = [40, 60, 80]
        rand_x = randint(0,2)
        self.x = x_cor[rand_x]
        self.z = brod.z_kor - 500
        self.color_pl = colors[randint(0,9)]

    def postavi_new(self):
        self.y = 0
        if self.x < 0:
            x_cor = [-100, -80, -60]
            z_cor = [-50, -150, -250]
        elif self.x > 0:
            x_cor = [40, 60, 80]
            z_cor = [-100, -200, -300]
        rand_x = randint(0,2)
        rand_z = randint(0,2)
        self.x = x_cor[rand_x]
        self.z = z_cor[rand_z]
        self.color_pl = colors[randint(0,9)]
    def update(self):   
        global stop
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color_pl)
        glTranslated(self.x, self.y, self.z)

        if GameState.currState == GameState.PLAY: #ako je igra jos traje
            if(self.z >= brod.z_kor): #ako igrac prodje planet
                self.postavi()  #postave se nove nasumicne vrijednosti koordinata i boje planeta

        glutSolidSphere(3, 100, 100)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color_pr)
        glRotatef(60, 1, 0, 0)
        glutWireTorus(0.2, 5, 2, 100)
        glutWireTorus(0.4, 5, 2, 100)
        glutWireTorus(0.8, 5, 2, 100)
        glPopMatrix()

class SvemirskiBrod:
    def __init__(self,r,c,h,x,z):
        self.radius = r
        self.color = c
        self.x = x
        self.y = h
        self.z = z
        self.radijus = 1

    #metoda kojom postavljamo nove nasumicne vrijednosti koordinata
    def postavi(self):
        self.y = 0
        x_cor = [-4, 0, 4]
        rand_x = randint(0,2)
        self.x = x_cor[rand_x]
        self.z = brod.z_kor - 500

    def postavi_new(self):
        self.y = 0
        x_cor = [-4, 0, 4]
        z_cor = [-90, -300]
        rand_x = randint(0,2)
        rand_z = randint(0,1)
        self.x = x_cor[rand_x]
        self.z = z_cor[rand_z]
    def update(self):   
        global stop,rotate_brod
        if GameState.currState == GameState.PLAY:#ako je igra jos traje
            if(self.z >= brod.z_kor + 50): #ako igrac prodje svemirski brod
                self.postavi() #postave se nove nasumicne vrijednosti koordinata 
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        glTranslated(self.x, self.y, self.z)
        glRotatef(90, 1, 0, 0)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        glutSolidTorus(0.6, 1, 3, 100)
        glPopMatrix()


class Asteroid:
    def __init__(self, r, c, x, z):
        self.x = x
        self.y = 0
        self.z = z
        self.radijus = r
        self.color = c

    #metoda kojom postavljamo nove nasumicne vrijednosti koordinata i boja
    def postavi(self):
        self.y = 0
        x_cor = [-4, 0, 4]
        rand_x = randint(0,2)
        self.x = x_cor[rand_x]
        self.z = brod.z_kor - 400

    def postavi_new(self):
        self.y = 0
        x_cor = [-4, 0, 4]
        z_cor = [-150,-180,-210]
        rand_x = randint(0,2)
        rand_z = randint(0,2)
        self.x = x_cor[rand_x]
        self.z = z_cor[rand_z]

    def update(self):   
        global stop
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        glTranslated(self.x, self.y, self.z)
        if GameState.currState == GameState.PLAY:#ako je igra jos traje
            if(self.z >= brod.z_kor + 50): #ako igrac prodje meteor
                self.postavi() #postave se nove nasumicne vrijednosti koordinata
        glutSolidSphere(1.4, 30, 30)
        glPopMatrix()
         
        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        glTranslated(self.x, self.y, self.z)
        glutSolidCylinder(0.4, 1.4, 30, 100)
        glRotatef(90, 1, 0, 0)
        glutSolidCylinder(0.4, 1.4, 30, 100)
        glRotatef(-45, 1, 0, 0)
        glutSolidCylinder(0.4, 1.4, 30, 100)
        glRotatef(120, 1, 0, 0)
        glutSolidCylinder(0.4, 1.4, 30, 100)
        glRotatef(-120, 1, 0, 0)
        glutSolidCylinder(0.4, 1.4, 30, 100)
        glRotatef(270, 1, 0, 0)

        glutSolidCylinder(0.4, 1.4, 30, 100)
        glRotatef(90, 0, 1, 0)
        glutSolidCylinder(0.4, 1.4, 30, 100)
        glRotatef(45, 0, 1, 0)
        glutSolidCylinder(0.4, 1.4, 30, 100)
        glRotatef(-90, 0, 1, 0)
        glutSolidCylinder(0.4, 1.4, 30, 100)
        glRotatef(-120, 0, 1, 0)
        glutSolidCylinder(0.4, 1.4, 30, 100)
        glRotatef(-240, 0, 1, 0)
        glutSolidCylinder(0.4, 1.4, 30, 100)
        glPopMatrix()


#metoda kojom se detektira sudar igracevog broda s planetom, meteorom ili drugim svemirskim brodom
def sudar():
    _sudar = False
    if not stop:  #provjerava sudar ako nije pauzirana igra
        for p in planeti:
            if(brod.z_kor - 1 < p.z + 3 and brod.z_kor > p.z - 3 and #
            brod.z_kor + 1 < p.z + 3 and brod.z_kor > p.z - 3 and
            brod.x_kor + 1 > p.x - 3 and brod.x_kor < p.x + 3 and
            brod.x_kor - 1 > p.x - 3 and brod.x_kor < p.x + 3) and GameState.currState == GameState.PLAY:
                _sudar += True
            else:
                _sudar += False  
    return _sudar #vraca True ako je detektirao sudar s nekim objektom, False ako nije

def sudar_aster():
    if not stop: #provjerava sudar ako nije pauzirana igra
        for a in asteroidi:
            if(brod.z_kor - 1 < a.z + 2 and brod.z_kor > a.z - 2 and
            brod.z_kor + 1 < a.z + 2 and brod.z_kor > a.z - 2 and
            brod.x_kor + 1 > a.x - 2 and brod.x_kor < a.x + 2 and
            brod.x_kor - 1 > a.x - 2 and brod.x_kor < a.x + 2) and GameState.currState == GameState.PLAY:
                if a.color == BLUE: #ako igraca pogodi plavi asteroid poduplaju se bodovi
                    Score.currScore += Score.currScore
                    a.postavi()
                else:                   #ako igraca pogodi smedji asteroid igra je gotova
                    GameState.collisionTime = time.time()
                    GameState.currState = GameState.COLLISION
                


def sudar_svemirac():
    if not stop: #provjerava sudar ako nije pauzirana igra
        for s in svemirci:
            if(brod.z_kor - 1 < s.z + 2 and brod.z_kor > s.z - 2 and
            brod.z_kor + 1 < s.z + 2 and brod.z_kor > s.z - 2 and
            brod.x_kor + 1 > s.x - 2 and brod.x_kor < s.x + 2 and
            brod.x_kor - 1 > s.x - 2 and brod.x_kor < s.x + 2) and GameState.currState == GameState.PLAY:
                if s.color == GREEN: #ako se igrac sudari s prijateljskim svemircem
                    Score.currScore = Score.currScore/2  #smanje se bodovi na pola
                    s.postavi()
                else:                           #ako se sudari s neprijateljem igra je gotova
                    GameState.collisionTime = time.time()
                    GameState.currState = GameState.COLLISION

#metoda kojom se provjerava skuplja li igrac smece
def skupi():
    for s in smece:
        if(brod.z_kor - 1 < s.z + 2 and brod.z_kor > s.z - 2 and
           brod.z_kor + 1 < s.z + 2 and brod.z_kor > s.z - 2 and
           brod.x_kor + 1 > s.x - 2 and brod.x_kor < s.x + 2 and
           brod.x_kor - 1 > s.x - 2 and brod.x_kor < s.x + 2): #ako igrac pokupi smece
            if s.color == DARK_GREEN: #ako je igrac pokupio zeleno smece 
                radioactive = randint(0,1)  #nasumicno se provjerava radioaktivnost otpada
                if radioactive == 1:  #ako je pokupljeno smece radioaktivno igra je gotova
                    GameState.collisionTime = time.time()
                    GameState.currState = GameState.COLLISION
                else:
                    Score.currScore += 20 #ako je radioaktivnost neopasna igracu se povecava brzina i dobije 20 bodova
                    brod.speed += 0.1
            elif s.color == SPRING_GREEN: #ako pokupi zeleni otpad dobije 5 bodova
                Score.currScore += 5  
            elif s.color == LIGHT_BLUE: #ako je igrac pokupio plasticni otpad dobije dodatnih 20 bodova
                Score.currScore += 20
          
            #kada je smece skupljeno postavlja se na novu poziciju
            x_cor = [-4, 0, 4]  
            rand_x = randint(0,2)  
            s.z = brod.z_kor - 500 #objekt se postavlja u odnosu na trenutnu z vrijednost igraca
            s.x = x_cor[rand_x]  #x koordinata se postavlja nasumicno
            

       
class Display:
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    TITLE = b"Explore The Space"
    displayWinID = 0

    
    @staticmethod
    def init():
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowPosition(0, 0)
        glutInitWindowSize(Display.WIDTH, Display.HEIGHT)
        Display.displayWinID = glutCreateWindow(Display.TITLE)
        glutFullScreen()

        glColorMaterial(GL_FRONT, GL_AMBIENT)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glutDisplayFunc(render)
        glutSpecialFunc(handleArrows)
        glutKeyboardFunc(handleKeyboard)
        Display.perProjection()
        Display.positionCamera()
  
        

    @staticmethod
    def perProjection():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, Display.WIDTH / Display.HEIGHT, 1, 2500)
        glMatrixMode(GL_MODELVIEW)

    @staticmethod
    def orthoProjection():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, Display.WIDTH, 0, Display.HEIGHT)
        glMatrixMode(GL_MODELVIEW)

    @staticmethod
    def positionCamera():
        glLoadIdentity()
        #gluLookAt(eyeX,eyeY,eyeZ,centerX,centerY,centerZ,upX,upY,upZ). 
        gluLookAt(0, 5.5, 15 + brod.z_kor,
                  0, 0, brod.z_kor - 15,
                  0, 1, 0)

def handleArrows(key, x, y):
    if GameState.currState == GameState.COLLISION:
        return
    if not brod.goRight and not brod.goLeft and stop == False:
        if key == GLUT_KEY_LEFT and brod.currX - 4 > -6:
            brod.currX -= 4
            brod.goLeft = True
        elif key == GLUT_KEY_RIGHT and brod.currX + 4 < 6:
            brod.currX += 4
            brod.goRight = True
    glutPostRedisplay()

def handleKeyboard(key, x, y):
    global stop
    if key == b'q':
        GameState.currState = GameState.QUIT  #pritiskom na tipku q izlazi se iz igre
    if key == ESCAPE:
        GameState.currState = GameState.QUIT #pritiskom na tipku ESC izlazi se iz igre
    if key == b'p' and GameState.currState == GameState.COLLISION:  #nakon sto se dodje u stanje sudara i pritisne tipka p
        GameState.currState = GameState.GAME_OVER   #igra je gotova, pokrece se nova

    if key == SPACE:
        stop = False  #pritiskom na tipku Space igrac pokrece svoj sv.brod naprijed
    if key == b's':
        stop = True #pritiskom na tipku 's' igrac zaustavlja svoj sv.brod 
    if key == b'v' and stop == True: # ako igrac pritisne tipku v i ako se zaustavi
        for p in planeti:  #provjera da li se igrac zaustavio ispred nekog planeta
            if(brod.z_kor - 1 < p.z + 20 and brod.z_kor > p.z + 3 and
                brod.x_kor + 1 > p.x - 3 and brod.x_kor < p.x + 3 and
                brod.x_kor - 1 > p.x - 3 and brod.x_kor < p.x + 3):
                i = randint(0,1) #nasumicni odabir je li planet prijateljski
                if i:
                    Score.currScore += 100 #ako je planet prijateljski igrac dobije 100 bodova
                else:
                    if Score.currScore - 100 > 0: #ako igrac ima dovoljan broj bodova placa stetu 100 bodova
                        Score.currScore -= 100
                    else:       #ako nema dovoljno za platiti igra gotova
                        GameState.collisionTime = time.time()
                        GameState.currState = GameState.COLLISION

    
    


def render():
    #print(brod.z_kor,';',brod.x_kor)
    Display.positionCamera()
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    GameState.processState()
    glutSwapBuffers()

def timer(x):
    stTime = time.time()
    render()
    glutTimerFunc(max(int(1000 / Display.FPS - (time.time() - stTime) * 1000), 0), timer, 0)


def main():
    Display.init()
    Sky.init()
    glutTimerFunc(0, timer, 0)
    glutMainLoop()

asteroidi = []
planeti = []
smece = []
svemirci=[]
udaljeni = []
       
brod = Brod(0, 0, 0)

otpad1 = Otpad(SPRING_GREEN, 0, -60)
otpad2 = Otpad(DARK_GREEN, -4, -270)
plasticni = PlasticniOtpad(LIGHT_BLUE, 4, -60)
smece.append(otpad1)
smece.append(otpad2)
smece.append(plasticni)

a1 = Asteroid(1,DARK_WOOD,-4, -150)
a2 = Asteroid(1,DARK_WOOD,0, -180)
a3 = Asteroid(0.5,BLUE,0, -210)
asteroidi.append(a1)
asteroidi.append(a2)
asteroidi.append(a3)


                       
pp1 = PlanetSaPrstenom(BLUE,WHITE,0,-4,-500)
planeti.append(pp1)
                   
s1 = SvemirskiBrod(0.2,RED, 0, 0, -140)
s2 = SvemirskiBrod(0.2, GREEN, 0, 4, -210)
svemirci.append(s1)
svemirci.append(s2)


u_pp1 = UdaljeniPlanetSaPrstenom(BLUE,WHITE,0,40,-200)
u_pp2 = UdaljeniPlanetSaPrstenom(GREEN,WHITE,0,60,-100)
u_pp3 = UdaljeniPlanetSaPrstenom(WHITE,WHITE,0,80,-300)
u_pp4 = UdaljeniPlanetSaPrstenom(BRONZE,WHITE,0,-60,-50)
u_pp5 = UdaljeniPlanetSaPrstenom(YELLOW,WHITE,0,-80,-150)
u_pp6 = UdaljeniPlanetSaPrstenom(PINK,WHITE,0,-100,-250)

udaljeni.append(u_pp1)
udaljeni.append(u_pp2)
udaljeni.append(u_pp3)
udaljeni.append(u_pp4)
udaljeni.append(u_pp5)
udaljeni.append(u_pp6)


if __name__ == "__main__":
    main()
