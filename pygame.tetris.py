import pygame
import random

pygame.font.init()

# Globale verdier
s_bredde = 600                                   # bredde på vindu
s_hoyde = 550                                    # lengde på vindu
blokk_storrelse = 20                             # størrelse på blokk
blokker_bredde = 10                              # antall blokker bortover
blokker_hoyde = 20                               # antall blokker nedover
poeng_level = 200                                # poeng som kreves per level

spill_bredde = blokker_bredde * blokk_storrelse  # spillvindu størrelse
spill_høyde = blokker_hoyde * blokk_storrelse    # spillvindu 
top_venstre_x = (s_bredde - spill_bredde) // 2   # finne start posisjon
top_venstre_y = s_hoyde - spill_høyde - 50

max_score = 0


# Figurer

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

figurer = [S, Z, I, O, J, L, T]
figur_farger = [(0, 255, 0, 0), (255, 0, 0, 0), (0, 255, 255, 0), (255, 255, 0, 0), (255, 165, 0, 0), (0, 0, 255, 0), (128, 0, 128, 0)]
# indeks 0 - 6 representerer figurene


class Blokk(object):                                             # definerer klassen "Blokk" med x-verdi, y-verdi, figur, farger og rotasjon
    def __init__(self, x, y, figur):
        self.x = x
        self.y = y
        self.figur = figur
        self.farge = figur_farger[figurer.index(figur)]
        self.rotasjon = 0
    def getHoyde(self):                                          # får ut høyden til en figur
        (ins, cf) = get_koordinat(self)                          # gjør om til koordinater
        minY = min(y for (x,y) in cf)
        maxY = max(y for (x,y) in cf)
        return maxY - minY + 1

def lage_grid(laast_pos={}):                                     # lager en spill ramme
    global blokker_bredde,blokker_hoyde           
    grid = [[(0,0,0,0) for _ in range(blokker_bredde)] for _ in range(blokker_hoyde)]
    # lager et svart 10x20 rektangel

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in laast_pos:                              # lagrer fargen til ruter som har falt (låst posisjon)
                c = laast_pos[(j,i)]
                grid[i][j] = c
    return grid


def get_koordinat(figur):                                        # gjør om figurene til koordinater
    posisjoner = []
    format = figur.figur[figur.rotasjon % len(figur.figur)]      # få formen av figuren

    for i, line in enumerate(format):                            # splitter figur til lister med indeks til hver rad
        row = list(line)
        for j, column in enumerate(row):                         # splitter radene til enkelte ruter
            if column == '0':
                posisjoner.append((figur.x + j, figur.y + i))    # finner koordinatene til hver rute med farge

    for i, pos in enumerate(posisjoner):
        posisjoner[i] = (pos[0] - 2, pos[1] - 4)
        
    iSkjerm = all(y >= 0 for (x,y) in posisjoner)

    return (iSkjerm, posisjoner)


def gyldig_plass(figur, grid):                                   # sjekker om figurerne er innenfor rammen
    global blokker_bredde, blokker_hoyde
    # finner ledige ruter
    ledig_pos = [[(j, i) for j in range(blokker_bredde) if grid[i][j] == (0,0,0,0)] for i in range(blokker_hoyde)]
    ledig_pos = [j for sub in ledig_pos for j in sub]

    iSkjerm, formatted = get_koordinat(figur)

    for pos in formatted:                                        # sjekker om hver posisjon er gyldig
        if pos not in ledig_pos:
            if pos[1] > -1:
                return False
    return True

def sjekk_tapt(posisjoner):                                      # sjekker om figuren når toppen
    for pos in posisjoner:
        x, y = pos
        if y < 1:
            return True
    return False


def get_figur():                                                 # gir en tilfeldig figur
    return Blokk(5, 0, random.choice(figurer))


def get_skygge_Blokk(fallendeBlokk):                             # skaper en brikke som viser hvor den fallende brikken kommer til å lande
    skyggeBlokk = Blokk(fallendeBlokk.x, fallendeBlokk.y, fallendeBlokk.figur)
    skyggeBlokk.rotasjon = fallendeBlokk.rotasjon
    l = list(fallendeBlokk.farge)
    l[3] = 128                                                   # gjør figuren halvveis gjennomsiktig
    skyggeBlokk.farge = tuple(l)
    skyggeBlokk.y = fallendeBlokk.y + fallendeBlokk.getHoyde()
    return skyggeBlokk

def isSkygge(farge_tuple):                                       # sjekker om figur er en skygge figur
    l = list(farge_tuple)
    return l[3] == 128

def get_farge(farge_tuple):                                      # gjør figur halvveis gjennomsiktig
    l = list(farge_tuple)
    return tuple(l[:3])

def skygge(fallende_Blokk, gammel_skygge_Blokk, grid):           # lage skygge hvis mulig
    if ((gammel_skygge_Blokk != None)                            # sjekker om at den fallende figuren ikke er lik skyggen
        and (fallende_Blokk.y + fallende_Blokk.getHoyde() >= gammel_skygge_Blokk.y) 
        and (fallende_Blokk.figur == gammel_skygge_Blokk.figur)
        and (fallende_Blokk.rotasjon == gammel_skygge_Blokk.rotasjon)
        and (fallende_Blokk.x == gammel_skygge_Blokk.x)):
            return fallende_Blokk;    
    skyggeBlokk = get_skygge_Blokk(fallende_Blokk)               # skaper skygge figur
    funnetGyldig = False
    GyldigY1 = -1                                                
    while (skyggeBlokk.y < 30) and (funnetGyldig == False):      # flytter skyggen nedover til første gyldige y-verdi uten å være lik den fallende figuren
        skyggeBlokk.y += 1
        funnetGyldig = gyldig_plass(skyggeBlokk, grid)           # sjekker om gyldig
    if (funnetGyldig):
        GyldigY1 = skyggeBlokk.y                                 # flytter skyggen til første gyldige y-verdi   
        funnetIGyldig = False
        while (skyggeBlokk.y < 30) and (funnetIGyldig == False): # flytter skygge nedover til noe stopper den
            skyggeBlokk.y += 1
            funnetIGyldig = not gyldig_plass(skyggeBlokk, grid)
        if funnetIGyldig:                                        # stopper skyggeblokken
            skyggeBlokk.y -= 1  
            return skyggeBlokk
        else:
            skyggeBlokk.y = GyldigY1
            return skyggeBlokk
    return fallende_Blokk

def tegne_tekst(overflate, tekst, storrelse, farge):             # funksjon som skriver ut tekster  
    font = pygame.font.SysFont("comicsans", storrelse, bold=True)
    label = font.render(tekst, 1, farge)

    overflate.blit(label, (top_venstre_x + spill_bredde /2 - (label.get_width()/2), top_venstre_y + spill_høyde/2 - label.get_height()/2))


def tegne_ruter(surface, grid):                                  # lager rutene
    sx = top_venstre_x
    sy = top_venstre_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*blokk_storrelse), (sx+spill_bredde, sy+ i*blokk_storrelse))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*blokk_storrelse, sy),(sx + j*blokk_storrelse, sy + spill_høyde))


def slette_rader(grid, laast):                                       # tømmer rutene når en rad er fylt opp
    inc = 0
    rader_pop = []
    for i in range(len(grid)-1, -1, -1):                             # gjør om til rader
        rad = grid[i]
        if all( (c != (0,0,0,0) and not isSkygge(c)) for c in rad):  # sjekker om cellene er okkuperbare 
            inc += 1
            rader_pop.append(i)
            for j in range(len(rad)):                                # tømme rader
                try:
                    del laast[(j,i)]
                except:
                    continue

    if inc > 0:                                                      # flytte rader om rader slettes
        for key in sorted(list(laast), key=lambda x: x[1])[::-1]:    # begynner fra bunnen
            x, y = key
            
            # flytter rader nedover i følge til hvor mange rander som slettes under
            rader_pop_lower = list(filter(lambda r: r > y, rader_pop))
            newKey = (x, y + len(rader_pop_lower))
            laast[newKey] = laast.pop(key)

    score_inc = {                                                    # lager et dictionary med poeng for antall slettede rader
        0: 0,
        1: 10,
        2: 30,
        3: 50,
        4: 80,
        }
    return score_inc.get(inc)


def tegne_neste_figur(figur, overflate):                     # viser den neste fallende figuren
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next figur', 1, (255,255,255))

    sx = top_venstre_x + spill_bredde + 50                   # plasserer figuren
    sy = top_venstre_y + spill_høyde/2 - 100
    format = figur.figur[figur.rotasjon % len(figur.figur)]

    for i, line in enumerate(format):                        # tegne neste figur
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(overflate, figur.farge, (sx + j*blokk_storrelse, sy + i*blokk_storrelse, blokk_storrelse, blokk_storrelse), 0)

    overflate.blit(label, (sx + 10, sy - 30))                # plasserer tekst

def oppdatere_high_score(nscore):                            # opdaterer high score
    global max_score
    if max_score < nscore:
        max_score = nscore

def tegne_vindu(overflate, grid, score=0):                   # tegner vinduet
    overflate.fill((0, 0, 0))

    pygame.font.init()                                       # lager tittel
    font = pygame.font.SysFont('comicsans', 60)
    tittel = font.render('Tetris', 1, (255, 255, 255))

    overflate.blit(tittel, (top_venstre_x + spill_bredde / 2 - (tittel.get_width() / 2), 30))

    # viser score
    font = pygame.font.SysFont('comicsans', 30)
    tekst = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_venstre_x + spill_bredde + 50
    sy = top_venstre_y + spill_høyde/2 - 100

    # viser high score
    overflate.blit(tekst, (sx + 20, sy + 160))
    tekst = font.render('High Score: ' + str(max_score), 1, (255,255,255))

    sx = top_venstre_x - 200
    sy = top_venstre_y + 200

    overflate.blit(tekst, (sx + 20, sy + 160))

    # fargelegging
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            skygge_flate = pygame.Surface((blokk_storrelse, blokk_storrelse))
            if isSkygge(grid[i][j]):
                skygge_flate.set_alpha(128)                  # gjør skyggen halvveis gjennomsiktig
            skygge_flate.fill(get_farge(grid[i][j]))
            overflate.blit(skygge_flate, (top_venstre_x + j*blokk_storrelse, top_venstre_y + i*blokk_storrelse))

    # tegner spillruten
    pygame.draw.rect(overflate, (255, 0, 0), (top_venstre_x, top_venstre_y, spill_bredde, spill_høyde), 5)

    tegne_ruter(overflate, grid)
    

def level_up(fallende_hastighet):                            # fjerner ruter med farger og øker hastighet når spiller når nytt level
    global blokker_bredde,blokker_hoyde
    ny_hastighet = fallende_hastighet - 0.05                 # øker hastighet
    # fjerner alle blokker
    grid = [[(0,0,0,0) for _ in range(blokker_bredde)] for _ in range(blokker_hoyde)]

    return (ny_hastighet, grid, {})        
    


def hoved(win): 
    global poeng_level
    laast_posisjoner = {}                   # koordinatene til okkuperte celler
    grid = lage_grid(laast_posisjoner)      # 10x20 tabell som lagrer fargen til hver celle

    bytte_Blokk = False                     # om skal bytte figur
    run = True                              # holder spillet gående
    fallende_Blokk = get_figur()            # skaper fallende blokk
    neste_Blokk = get_figur()               # skaper neste blokk
    klokke = pygame.time.Clock()            # tar tiden
    fall_tid = 0                            # hvor lenge brikken har falt
    fall_hastighet = 0.5                    # hastigheten brikken faller på                         
    score = 0                               # poeng
    level = 1                               # level
    skygge_Blokk = None                     # skyggeblokk
    
    while run:
        grid = lage_grid(laast_posisjoner)  # lager spill skjerm (der brikkene faller)
        fall_tid += klokke.get_rawtime()    # stopper stoppeklokken for løkken
        klokke.tick()                       # starter stoppeklokken for løkken

        # flytter fallende blokk nedover når fall tiden er nådd
        if fall_tid/1000 > fall_hastighet:
            fall_tid = 0
            if (gyldig_plass(fallende_Blokk, grid)) == True:  
                fallende_Blokk.y += 1
                # stopper blokken når hindret og bytter blokk
                if not(gyldig_plass(fallende_Blokk, grid)) and fallende_Blokk.y > 0:
                    fallende_Blokk.y -= 1
                    bytte_Blokk = True
            else:
                tegne_tekst(win, "GAME OVER", 80, (255,255,255))
                pygame.display.update()
                pygame.time.delay(1500)
                run = False

        # kontroller
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()     
            if event.type == pygame.KEYDOWN:
                # flytter den fallende blokken mot venstre
                if event.key == pygame.K_LEFT:
                    fallende_Blokk.x -= 1
                    if not(gyldig_plass(fallende_Blokk, grid)):
                        fallende_Blokk.x += 1
                # flytter den fallende blokken mot høyre
                if event.key == pygame.K_RIGHT:
                    fallende_Blokk.x += 1
                    if not(gyldig_plass(fallende_Blokk, grid)):
                        fallende_Blokk.x -= 1
                # flytter den fallende blokken nedover kjappere
                if event.key == pygame.K_DOWN:
                    fallende_Blokk.y += 1
                    if not(gyldig_plass(fallende_Blokk, grid)):
                        fallende_Blokk.y -= 1
                # roterer den fallende blokken
                if event.key == pygame.K_UP:
                    fallende_Blokk.rotasjon += 1
                    if not(gyldig_plass(fallende_Blokk, grid)):
                        fallende_Blokk.rotasjon -= 1
                # flytter den fallende blokken rett ned
                if event.key == pygame.K_SPACE:
                    while gyldig_plass(fallende_Blokk, grid): 
                        fallende_Blokk.y += 1
                    fallende_Blokk.y -= 1

        # legger inn fallende figurer
        iSkjerm_fallende, figur_pos = get_koordinat(fallende_Blokk)
        for i in range(len(figur_pos)):
            x, y = figur_pos[i]
            if y > -1:
                grid[y][x] = fallende_Blokk.farge

        if iSkjerm_fallende:
            # Lage ny skygge når fallende blokk er byttet
            skygge_Blokk = skygge(fallende_Blokk, skygge_Blokk, grid)
            if (skygge_Blokk.y > fallende_Blokk.y):
                (iSkjerm_skygge, figur_pos_skygge) = get_koordinat(skygge_Blokk)
                # legger inn skygge hvis gyldig plass 
                if (iSkjerm_skygge): 
                    for i in range(len(figur_pos_skygge)):
                        x, y = figur_pos_skygge[i]
                        grid[y][x] = skygge_Blokk.farge
     
        # låser den fallende blokken og bytter til neste fallende blokk
        if bytte_Blokk:
            for pos in figur_pos:
                p = (pos[0], pos[1])
                laast_posisjoner[p] = fallende_Blokk.farge
            fallende_Blokk = neste_Blokk
            neste_Blokk = get_figur()
            bytte_Blokk = False
            score += slette_rader(grid, laast_posisjoner)
            # level up
            if score >= level*poeng_level:
                level += 1
                fall_hastighet, grid, laast_posisjoner = level_up(fall_hastighet)
                tegne_tekst(win, "Level up", 80, (255,255,255))
                pygame.display.update()
                pygame.time.delay(1500)

        oppdatere_high_score(score)
        tegne_vindu(win, grid, score)
        tegne_neste_figur(neste_Blokk, win)
        pygame.display.update()

        # sjekker om spillet er tapt
        if sjekk_tapt(laast_posisjoner):
            tegne_tekst(win, "GAME OVER", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

# hoved program
def hovedmeny(win):
    run = True
    while run:
        win.fill((0,0,0))
        tegne_tekst(win, 'Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                hoved(win)

    pygame.display.quit()

# setter opp vindu
win = pygame.display.set_mode((s_bredde, s_hoyde))
pygame.display.set_caption('Tetris')
hovedmeny(win)