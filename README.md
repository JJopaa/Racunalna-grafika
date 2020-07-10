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
 
2.2.	Sučelje igre

U Python datoteci main.py nalazi se glavni dio igrice.

U klasi GameState provjerava se stanje igre koje može biti PLAY, COLLISION, GAME_OVER i QUIT. Ako je stanje igre GameState.GAME_OVER onda se za svaki objekt igre ponovno postavljaju njihova svojstva te se stanje postavlja u GameState.PLAY da se pokrene nova igra. Tijekom stanja GameState.PLAY ažuriraju se vrijednosti koordinata i boja objekata te se iscrtava pozadina(Sky). Također se provjeravaju sudari igrača sa asteroidima i planetima pozivanjem funkcija sudar_svemirac() i sudar_aster(),a skupljanje otpada se provjerava pozivanjem funkcije skupi(). Navedene funkcije će biti objašnjene malo poslije.
 
Klasa Score sprema bodove koje igrač osvaja tijekom igranja i pamti najbolji rezultat (svakim novim pokretanjem aplikacije briše se najbolji rezultat) te ih ispisuje na ekranu u gornjem lijevom kutu. Također kada igra završi tj. kada dođe do stanja GameState.COLLISION na ekranu se ispisuju osvojeni bodovi te poruka da se pritiskom na tikpu 'p' igrica može ponovno pokrenuti ili se može izaći iz aplikacije pritiskom na tipku 'q'. Metoda drawText() ispisuje tekst na ekran prebacivanjem iz 3D projekcije u 2D ortogonalnu projekciju te nakon ispisa teksta se ponovno vraća 3D projekcija. Metode za prebacivanje iz projekcije u projekciju su definirane u klasi Display.
 
Klasa Display sadrži metodu za inicijalizaciju parametara prikaza prozora, pozivaju se funkcije za detekciju pritisnutih tipki na tipkovnici, te se postavlja projekcija i kamera. U ovoj klasi nalaze se metode perProjection() za postavljanje u 3D projekciju za iscrtavanje 3D elemenata igrice te metoda orthoProjection() za postavljanje u 2D projekciju da bi se mogao ispisati tekst rezultata.
 
Klasom Sky prikazuje se pozadina igrice te se ona pomiče na osi y da bi se stekao dojam da se igračev svemirski brod zaista kreće svemirom. Pozadina je ustvari .jpg slika dimenzija 8000x4000 piksela, a napravljena je u programu Bojanje(Paint).
 
2.3. Klase i objekti igre

2.3.1.Brod

Početna ideja

Glavni objekt igrice je svemirski brod Ozon3. Svemirski brod se može uništiti ako mu bodovi padnu na nula, a to se može dogoditi slučajnim sudarom sa planetom, gubljenjem bodova u polju asteroida, svakim pogotkom od strane neprijateljskih brodova.

Implementacija

Klasom Brod definirana su osnova svojstva te metode koje omogućavaju prikaz i upravljanje glavnim objektom igrice – svemirskim brodom. Svojstva koja definiraju brod su: koordinata na osi x, koordinata na osi y, koordinata na osi z, trenutna x koordinata, brzina te svojstvo kojim definiramo kreće li se brod lijevo ili desno. Brod se kreće u koordinatnom sustavu za koji vrijedi da je os y visina na kojoj se nalazi brod, za sve objekte igre y = 0, os x je os po kojoj se brod kreće lijevo-desno, a vrijednosti koje poprima na osi x su -4, 0 i 4, dok negativni dio osi z predstavlja os po kojoj se brod kreće prema naprijed. Za prikaz svemirskog broda korišten je OpenGL te naredbe za crtanje 3D objekata: glutSolidTorus() i glutWireTorus().
 
Igrač može pokretati i zaustavljati svoj svemirski brod te je u tu svrhu implementirana globalna varijabla stop kojom se to detektira. Ako se brod kreće onda se oko glavnog dijela broda iscrtava prsten koji se i rotira da bi se dobio dojam kretanja:
 
Naredba glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, RED) kontrolira osvijetljenost objekta, glRotatef(rotate_brod, 0, 0, 1) rotira objekt oko osi z za iznos rotate_brod koja se povećava svakim update-om za 0.4, a glutWireTorus(0.15, 2, 2, 50) crta prsten unutarnjeg radijusa 0.15, vanjskog radijusa 2, 2 koncentrične kružnice i 50 poprečnih.

2.3.2.Otpad

Početna ideja

Na svom putovanju svemirom igrač može naići i na svemirski otpad koji pluta svemirom. Ukoliko igrača pogodi nešto od radioaktivnog otpada igra je gotova ako se brod uništi ili se zbog radioaktivnosti mogu poboljšati performanse broda . Ako igrač naiđe na plastični otpad i pokupi ga od svemirske udruge GRETA dobije za povrat plastike dodatne bodove. 

Implementacija
 
Za objekte koji predstavljaju svemirsko smeće koje korisnik mora skupiti za dodatne bodove napravljene su dvije klase: Otpad i PlasticniOtpad. U klasi otpad objekt je nacrtan naredbom glutSolidCylinder() da bi predstavljao 'bačve' radioaktivnog sadržaja. Nasumičnim odabirom sudarom s objektom može se nauditi bodovima korisnika ili se mogu povećati, a ako je otpad radioaktivan može se i završiti igra. Navedene opcije su implementirane u metodi skupi() koja je prikazana gore. U klasi PlasticniOtpad objekt je iscrtan naredbama glutSolidCylinder() da bi predstavljao plastične boce koje ako igrač skupi donose dodatne bodove. U obje klase (i u ostalim klasama projekta) definirane su metode postavi() i postavi_new(). Metodu postavi() pozivamo kada igrač preleti pokraj tog objekta te se objekt ponovno postavlja na nasumične koordinate na osi x(lijevo-desno) i za u odnosu na igrača pomak na osi z u negativnom smjeru za 500. Metodu postavi_new() pozivamo prilikom inicijalizacije nove igre te se tada iscrtavaju objekti u vidljivom području ispred igrača.

2.3.3.PlanetSaPrstenom

Početna ideja

Na svom svemirskom putovanju igrač može doći i do planeta. Ako igrač ne pazi moguć je i sudar sa nekim od planeta. Ukoliko se to dogodi igrač gubi sve osvojene bodove te se vraća na početak igre. Igrač ima mogućnost zaobići planet i nastaviti svoje putovanje, ali može i posjetiti planet. Međutim, ne može znati je li planet prijateljski ili neprijateljski. Ukoliko je planet bio neprijateljski te ga igrač odluči posjetiti biva zarobljen te ne može nastaviti igru ukoliko ne plati svojim bodovima, ako ih nema igra je gotova. Ukoliko se ispostavilo da je posjećeni planet bio prijateljski igrač dobiva dodatne bodove za hrabrost.

Implementacija

Igračev svemirski brod kreće se 'stazama' sa vrijednostima -4, 0 i 4 na osi x pa je napravljena klasa za planete koji su nalaze na tim vrijednostima naziva PlanetSaPrstenom i na tim objektima se detektira interakcija s korisnikom, dok objekti klase UdaljeniPlanetSaPrstenom nemaju nikakvu interakciju sa korisnikom već su samo prikazani u daljini.  Planeti su predstavljeni sferom naredbom glutSolidSphere(3, 100, 100) te prstenima oko sfere naredbom glutWireTorus().
 

Metodom sudar() detektira se sudar igračevog broda s planetom :
 
2.3.4.UdaljeniPlanetSaPrstenom

Ideja i implementacija

Ova klasa definira planete koji se nalaze izvan okvira u kojima se kreće svemirski brod pa nije potrebno provjeravati sudare te su samo definirane metode kojima se iscrtavaju planeti i generiraju nove koordinate.
 
2.3.5.SvemirskiBrod

Početna ideja

Neprijateljski svemirski brod VirusX može nauditi bodovima igrača pucanjem na njegov brod ili sudarom s igračevim brodom. Igrač može susresti i prijateljski svemirski brod ProB te ako ga slučajno uništi time uništava i pola svojih bodova.

Implementacija

Neprijateljski i prijateljski svemirski brodovi definirani su klasom SvemirskiBrod te se samo razlikuju po boji i po tome što se dogodi sudarom sa igračem.
 
 
Neprijateljski svemirci imaju crveni brod te se sudarom s njima igra završava te se stanje postavlja u GameState.COLLISION, a prijateljski svemirci imaju zeleni brod te se sudarom s njima bodovi prepolove.

2.3.6.Asteroid

Početna ideja

Asteroidi su objekti koje igrač mora uspješno zaobići u poljima asteroida. Postoje i posebni maleni asteroidi sa planeta Omega3 koji ukoliko ih igrač pokupi mogu udvostručiti bodove

Implementacija

 
Asteroid je kugla nacrtana naredbom glutSolidSphere(), a da bi se prikazali 'krateri' na asteroidu korištene su naredbe glutSolidCylinder(). Metoda sudar_aster() detektira sudar igrača s asteroidima te ako se sudari s plavim bodovi se udvostruče, a sudar s ostalima znači kraj igre.
 
2.4.Globalne varijable – inicijalizacija objekata
 

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
 
o	tipka razmak (SPACE) – brod ide naprijed

o	tipka 's'  – brod se zaustavlja

o	tipka 'v' – posjeta planetu

o	tipka 'q' ili tipka ESC : izlazak iz igre
 







