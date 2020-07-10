# projekt kolegija Racunalna grafika 2019/20
space explore game with pygame and opengl

Explore the Space

1.	Opis projekta

U ovom projektu napravljena je igrica korištenjem skupa modula pygame i OpenGL-a. Ideja je bila napraviti 3D igricu u kojoj igrač upravlja svemirskim brodom te putujući kroz svemir izbjegava sudare s asteroidima i planetima, te skuplja dodatne bodove skupljajući svemirsko smeće. 

Glavni objekt igrice je svemirski brod. Igrač ga kontrolira pritiskom na strelice lijevo i desno na tipkovnici, pritiskom na SPACE brod se pokreće, a pritiskom na 's' brod se zaustavlja. Ukoliko se brod sudari s meteorom, planetom ili radioaktivnim otpadom igra se završava, prikazuje se postignuti rezultat te korisnik ima opciju da pritiskom na 'p' ponovno započne igru ili da pritiskom na 'q' izađe iz cijele aplikacije.

Neprijateljski svemirski brod prikazan je crvenom bojom te ukoliko se sudari s igračem igra se završava. Ako se igrač slučajno sudari s prijateljskim svemirskim brodom, kojeg razlikuje zelena boja,  gubi pola svojih bodova.

Asteroidi su objekti koje igrač mora uspješno zaobići. Sudarom s asteroidom igra se završava. Postoje i posebni asteroidi, razlikuje ih plava boja, koji ukoliko ih igrač pokupi mogu udvostručiti bodove. 

Na svom svemirskom putovanju igrač može doći i do planeta. Ako igrač ne pazi moguć je i sudar sa nekim od planeta te se vraća na početak igre. Igrač ima mogućnost zaobići planet i nastaviti svoje putovanje, ali može i posjetiti planet tako da se pritiskom na tipku 's' zaustavi ispred planeta te pritiskom na tipku 'v ' za 'posjetu'. Posjeta planetu se očituje u bodovima. Međutim, ne može znati je li planet prijateljski ili neprijateljski. Ukoliko je planet bio neprijateljski igraču se oduzima 100 bodova, ako ih nema igra je gotova. Ukoliko se ispostavilo da je posjećeni planet bio prijateljski igrač dobiva dodatne bodove.

Međutim, na svom putovanju svemirom igrač može naići i na svemirski otpad koji pluta svemirom. Otpad je prikazan kao zelene 'bačve' radioaktivnog sadržaja. Ukoliko igrača pogodi nešto od radioaktivnog otpada igra je gotova, ali ukoliko je to bila pozitivna radioaktivnost povećava se brzina broda te se dobivaju dodatni bodovi. Ako igrač naiđe na plastični otpad koji je iscrtan kao plastična boca dobiva dodatne bodove.

2.	Implementacija

Projekt se sastoji od dvije Python datoteke: ui.py i main.py. U ui.py nalazi se kod kojim se definira početno sučelje prilikom pokretanja igre, a u main.py se nalazi glavni kod same igrice. Igrica se pokreće pokretanjem ui.py.

2.1.	Početno sučelje

U Python datoteci ui.py nalazi se korisničko sučelje koje se prikazuje pri pokretanju igre, a u kojem je korišten skup modula pygame za interakciju s korisnikom. Osnovna klasa naziva gameIntro sadrži metode koje omogućavaju korisniku sljedeće opcije: pokretanje nove igre, pregled uputa kako igrati te opciju za izlazak iz programa.

    class gameIntro:
        displayWidth = 1280
        displayHeight = 720
        background = gameDisplay = None
        smallFont = medFont = largeFont = None
        clock = None
        @staticmethod
        def run():
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
            gameIntro.gameDisplay.blit(gameIntro.background, (0,0))
            gameIntro.button("Nova igra", 465,140,350,80, btnColor, lightBlack, "play")
            gameIntro.button("Kako igrati", 465,260,350,80, btnColor, lightBlack, "controls")
            gameIntro.button("Izlaz", 465,500,350,80, btnColor, lightBlack, "quit")
            pygame.display.update()
            gameIntro.clock.tick(30)
    @staticmethod
    def init():
        pygame.init()
        gameIntro.background = pygame.image.load("SKY.jpg")
        gameIntro.gameDisplay = pygame.display.set_mode((gameIntro.displayWidth, gameIntro.displayHeight))
        pygame.display.set_caption("Explore The Space")
        gameIntro.smallFont = pygame.font.SysFont("Ubuntu Medium", 20)
        gameIntro.medFont = pygame.font.SysFont("Ubuntu Medium", 50)
        gameIntro.largeFont = pygame.font.SysFont("Ubuntu Medium", 70)
        gameIntro.clock = pygame.time.Clock()
        gameIntro.run()

    @staticmethod
    def button(text, x, y, width, height, inactiveColor, activeColor, action):
        cur = pygame.mouse.get_pos()  # get mouse position
        click = pygame.mouse.get_pressed()  # get mouse action
        if x + width > cur[0] > x and y + height > cur[1] > y:
            pygame.draw.rect(gameIntro.gameDisplay, activeColor, (x, y, width, height))
            if click[0] == 1:
                if action == "quit":
                    pygame.quit()
                    sys.exit()
                if action == "controls":
                    gameIntro.gameControls()
                if action == "play":
                    pygame.quit()
                    main.main()
                if action == "main":
                    gameIntro.run()
        else:
            pygame.draw.rect(gameIntro.gameDisplay, inactiveColor, (x, y, width, height))
        gameIntro.textToButton(text, darkPurple, x, y, width, height)

    @staticmethod
    def gameControls():
        pygame.display.update()
        gCont = True
        while gCont:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            gameIntro.gameDisplay.blit(gameIntro.background, (0, 0))  # background is an image
            pygame.draw.rect(gameIntro.gameDisplay, btnColor, (300, 120, 700, 500))
            gameIntro.messageToScreen("Kako igrati?", lightBlack, -200, size="large")
            gameIntro.messageToScreen("brod pomakni ulijevo: strelica LIJEVO", lightBlack, -100)
            gameIntro.messageToScreen("brod pomakni udesno: strelica DESNO", lightBlack, -60 )
            gameIntro.messageToScreen("pokreni brod: SPACE", lightBlack, 0)
            gameIntro.messageToScreen("zaustavi brod: s", lightBlack, 35)
            gameIntro.messageToScreen("posjeti planet: v", lightBlack, 70)
            gameIntro.messageToScreen("Nova igra: p", lightBlack, 120)
            gameIntro.messageToScreen("Izlaz iz igre: q", lightBlack, 155)
            gameIntro.button("Nazad", 570, 550, 150, 70, btnColor, lightBlack, "main")
            pygame.display.update()
            gameIntro.clock.tick(30)


    @staticmethod
    def textToButton(msg, color, buttonX, buttonY, buttonWidth, buttonHeight, size="medium"):
        textSurf, textRect = gameIntro.textObjects(msg, (141,238,238), size)
        textRect.center = ((buttonX + (buttonWidth / 2)), buttonY + (buttonHeight / 2))
        gameIntro.gameDisplay.blit(textSurf, textRect)
    @staticmethod
    def messageToScreen(msg, color, yDisplace=0, size="medium"):
        textSurf, textRect = gameIntro.textObjects(msg, color, size)
        textRect.center = (int(gameIntro.displayWidth / 2), int(gameIntro.displayHeight / 2) + yDisplace)
        gameIntro.gameDisplay.blit(textSurf, textRect)

    @staticmethod
    def textObjects(text, color, size="small"):
        if size == "small":
            textSurface = gameIntro.smallFont.render(text, True, color)
        if size == "medium":
            textSurface = gameIntro.medFont.render(text, True, color)
        if size == "large":
            textSurface = gameIntro.largeFont.render(text, True, color)

        return textSurface, textSurface.get_rect()

    if __name__ == "__main__":
    gameIntro.init()
 
2.2.	Sučelje igre

U Python datoteci main.py nalazi se glavni dio igrice.

U klasi GameState provjerava se stanje igre koje može biti PLAY, COLLISION, GAME_OVER i QUIT. Ako je stanje igre GameState.GAME_OVER onda se za svaki objekt igre ponovno postavljaju njihova svojstva te se stanje postavlja u GameState.PLAY da se pokrene nova igra. Tijekom stanja GameState.PLAY ažuriraju se vrijednosti koordinata i boja objekata te se iscrtava pozadina(Sky). Također se provjeravaju sudari igrača sa asteroidima i planetima pozivanjem funkcija sudar_svemirac() i sudar_aster(),a skupljanje otpada se provjerava pozivanjem funkcije skupi(). Navedene funkcije će biti objašnjene malo poslije.

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
 
Klasa Score sprema bodove koje igrač osvaja tijekom igranja i pamti najbolji rezultat (svakim novim pokretanjem aplikacije briše se najbolji rezultat) te ih ispisuje na ekranu u gornjem lijevom kutu. Također kada igra završi tj. kada dođe do stanja GameState.COLLISION na ekranu se ispisuju osvojeni bodovi te poruka da se pritiskom na tikpu 'p' igrica može ponovno pokrenuti ili se može izaći iz aplikacije pritiskom na tipku 'q'. Metoda drawText() ispisuje tekst na ekran prebacivanjem iz 3D projekcije u 2D ortogonalnu projekciju te nakon ispisa teksta se ponovno vraća 3D projekcija. Metode za prebacivanje iz projekcije u projekciju su definirane u klasi Display.
 
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
                glColor3f(0, 1, 0)
                Score.drawText("  Novi rekord!  ", 300, Display.HEIGHT * 6 / 7, 0.6, 4)
                glColor(1, 1, 1, .5)
            Score.drawText("Tvoj rezultat : " + str(Score.currScore), 450 ,Display.HEIGHT * 3/4, 0.4, 2 )
            glColor3f(1, 0, 0)
            Score.drawText("Igra gotova !", Display.WIDTH / 2 - 350, Display.HEIGHT / 2, 1, 8)
            glColor(1, 1, 1, .5)
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
 
Klasa Display sadrži metodu za inicijalizaciju parametara prikaza prozora, pozivaju se funkcije za detekciju pritisnutih tipki na tipkovnici, te se postavlja projekcija i kamera. U ovoj klasi nalaze se metode perProjection() za postavljanje u 3D projekciju za iscrtavanje 3D elemenata igrice te metoda orthoProjection() za postavljanje u 2D projekciju da bi se mogao ispisati tekst rezultata.

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

 
Klasom Sky prikazuje se pozadina igrice te se ona pomiče na osi y da bi se stekao dojam da se igračev svemirski brod zaista kreće svemirom. Pozadina je ustvari .jpg slika dimenzija 8000x4000 piksela, a napravljena je u programu Bojanje(Paint).
 
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

 
2.3. Klase i objekti igre

2.3.1.Brod

Početna ideja

Glavni objekt igrice je svemirski brod Ozon3. Svemirski brod se može uništiti ako mu bodovi padnu na nula, a to se može dogoditi slučajnim sudarom sa planetom, gubljenjem bodova u polju asteroida, svakim pogotkom od strane neprijateljskih brodova.

Implementacija

Klasom Brod definirana su osnova svojstva te metode koje omogućavaju prikaz i upravljanje glavnim objektom igrice – svemirskim brodom. Svojstva koja definiraju brod su: koordinata na osi x, koordinata na osi y, koordinata na osi z, trenutna x koordinata, brzina te svojstvo kojim definiramo kreće li se brod lijevo ili desno. Brod se kreće u koordinatnom sustavu za koji vrijedi da je os y visina na kojoj se nalazi brod, za sve objekte igre y = 0, os x je os po kojoj se brod kreće lijevo-desno, a vrijednosti koje poprima na osi x su -4, 0 i 4, dok negativni dio osi z predstavlja os po kojoj se brod kreće prema naprijed. Za prikaz svemirskog broda korišten je OpenGL te naredbe za crtanje 3D objekata: glutSolidTorus() i glutWireTorus().
 
Igrač može pokretati i zaustavljati svoj svemirski brod te je u tu svrhu implementirana globalna varijabla stop kojom se to detektira. Ako se brod kreće onda se oko glavnog dijela broda iscrtava prsten koji se i rotira da bi se dobio dojam kretanja:
 
Naredba glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, RED) kontrolira osvijetljenost objekta, glRotatef(rotate_brod, 0, 0, 1) rotira objekt oko osi z za iznos rotate_brod koja se povećava svakim update-om za 0.4, a glutWireTorus(0.15, 2, 2, 50) crta prsten unutarnjeg radijusa 0.15, vanjskog radijusa 2, 2 koncentrične kružnice i 50 poprečnih.

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


2.3.2.Otpad

Početna ideja

Na svom putovanju svemirom igrač može naići i na svemirski otpad koji pluta svemirom. Ukoliko igrača pogodi nešto od radioaktivnog otpada igra je gotova ako se brod uništi ili se zbog radioaktivnosti mogu poboljšati performanse broda . Ako igrač naiđe na plastični otpad i pokupi ga od svemirske udruge GRETA dobije za povrat plastike dodatne bodove. 

Implementacija
 
Za objekte koji predstavljaju svemirsko smeće koje korisnik mora skupiti za dodatne bodove napravljene su dvije klase: Otpad i PlasticniOtpad. U klasi otpad objekt je nacrtan naredbom glutSolidCylinder() da bi predstavljao 'bačve' radioaktivnog sadržaja. Nasumičnim odabirom sudarom s objektom može se nauditi bodovima korisnika ili se mogu povećati, a ako je otpad radioaktivan može se i završiti igra. Navedene opcije su implementirane u metodi skupi() koja je prikazana gore. U klasi PlasticniOtpad objekt je iscrtan naredbama glutSolidCylinder() da bi predstavljao plastične boce koje ako igrač skupi donose dodatne bodove. U obje klase (i u ostalim klasama projekta) definirane su metode postavi() i postavi_new(). Metodu postavi() pozivamo kada igrač preleti pokraj tog objekta te se objekt ponovno postavlja na nasumične koordinate na osi x(lijevo-desno) i za u odnosu na igrača pomak na osi z u negativnom smjeru za 500. Metodu postavi_new() pozivamo prilikom inicijalizacije nove igre te se tada iscrtavaju objekti u vidljivom području ispred igrača.

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
        
2.3.3.PlanetSaPrstenom

Početna ideja

Na svom svemirskom putovanju igrač može doći i do planeta. Ako igrač ne pazi moguć je i sudar sa nekim od planeta. Ukoliko se to dogodi igrač gubi sve osvojene bodove te se vraća na početak igre. Igrač ima mogućnost zaobići planet i nastaviti svoje putovanje, ali može i posjetiti planet. Međutim, ne može znati je li planet prijateljski ili neprijateljski. Ukoliko je planet bio neprijateljski te ga igrač odluči posjetiti biva zarobljen te ne može nastaviti igru ukoliko ne plati svojim bodovima, ako ih nema igra je gotova. Ukoliko se ispostavilo da je posjećeni planet bio prijateljski igrač dobiva dodatne bodove za hrabrost.

Implementacija

Igračev svemirski brod kreće se 'stazama' sa vrijednostima -4, 0 i 4 na osi x pa je napravljena klasa za planete koji su nalaze na tim vrijednostima naziva PlanetSaPrstenom i na tim objektima se detektira interakcija s korisnikom, dok objekti klase UdaljeniPlanetSaPrstenom nemaju nikakvu interakciju sa korisnikom već su samo prikazani u daljini.  Planeti su predstavljeni sferom naredbom glutSolidSphere(3, 100, 100) te prstenima oko sfere naredbom glutWireTorus().
 
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

 
2.3.4.UdaljeniPlanetSaPrstenom

Ideja i implementacija

Ova klasa definira planete koji se nalaze izvan okvira u kojima se kreće svemirski brod pa nije potrebno provjeravati sudare te su samo definirane metode kojima se iscrtavaju planeti i generiraju nove koordinate.
 
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
 
2.3.5.SvemirskiBrod

Početna ideja

Neprijateljski svemirski brod VirusX može nauditi bodovima igrača pucanjem na njegov brod ili sudarom s igračevim brodom. Igrač može susresti i prijateljski svemirski brod ProB te ako ga slučajno uništi time uništava i pola svojih bodova.

Implementacija

Neprijateljski i prijateljski svemirski brodovi definirani su klasom SvemirskiBrod te se samo razlikuju po boji i po tome što se dogodi sudarom sa igračem.
 
 
Neprijateljski svemirci imaju crveni brod te se sudarom s njima igra završava te se stanje postavlja u GameState.COLLISION, a prijateljski svemirci imaju zeleni brod te se sudarom s njima bodovi prepolove.

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



2.3.6.Asteroid

Početna ideja

Asteroidi su objekti koje igrač mora uspješno zaobići u poljima asteroida. Postoje i posebni maleni asteroidi sa planeta Omega3 koji ukoliko ih igrač pokupi mogu udvostručiti bodove

Implementacija

 
Asteroid je kugla nacrtana naredbom glutSolidSphere(), a da bi se prikazali 'krateri' na asteroidu korištene su naredbe glutSolidCylinder(). Metoda sudar_aster() detektira sudar igrača s asteroidima te ako se sudari s plavim bodovi se udvostruče, a sudar s ostalima znači kraj igre.
 
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
 
2.4.Globalne varijable – inicijalizacija objekata
 
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

2.5.Kontrole u igri

Početna ideja

Igrač upravlja svemirskim brodom pritiskom na tipke: 

o	lijeva strelica (LEFT ARROW KEY)– brod ide u lijevo,

o	desna strelica (RIGHT ARROW KEY)– brod ide u desno, 

o	tipka razmak (SPACE) – brod ide naprijed

o	tipka S – brod se zaustavlja

o	klikom miša na planet – posjeta planetu

Kontrola igre:

o	Tipka P : pauziranje (ili nastavak) igre

o	Tipka Q ili tipka ESC : izlazak iz igre

Implementacija

Igrač svoj svemirski brod kontrolira pritiskom na tipke :

o	lijeva strelica (LEFT ARROW KEY)– brod ide u lijevo,

o	desna strelica (RIGHT ARROW KEY)– brod ide u desno, 

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
 
o	tipka razmak (SPACE) – brod ide naprijed

o	tipka 's'  – brod se zaustavlja

o	tipka 'v' – posjeta planetu

o	tipka 'q' ili tipka ESC : izlazak iz igre
 

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






