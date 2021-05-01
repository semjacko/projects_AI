import copy
import heapq

class uzol:
    def __init__(self, stav, pred, cena, goal):
        self.stav = []                              # stav: aktualne rozmiestnenie policok (dvojrozmerne pole)
        self.pred = pred                            # pred: referencia na predchadzajuci uzol
        self.cena = cena
        for i in range(len(stav)):
            self.stav.append(stav[i])
        self.heuristika = self.count_heu2(stav, goal)     # heuristika

    def __repr__(self):                             # reprezentacia uzla je vypis jeho stavu
        text = ""
        for i in self.stav:
            for j in i:
                text += str(j) + ' '
            text += "\n"
        return text

    def __lt__(self, other):
        return self.cena+self.heuristika < other.cena + other.heuristika

    def count_heu1(self, stav, goal):              # heuristika1: pocet zle umiestnenych policok
        heu1 = 0
        for i in range(ROWS):
            for j in range(COLUMNS):
                if i != goal[stav[i][j] - 1][0] or j != goal[stav[i][j] - 1][1]:    # prepocitanie pozicie
                    heu1 += 1
        return heu1

    def count_heu2(self, stav, goal):                    # heuristika2: sucet vzdialenosti policok od ich cielovej pozicie
        heu2 = 0
        for i in range(len(stav)):
            for j in range(len(stav[i])):
                heu2 += abs(goal[stav[i][j] - 1][0] - i) + abs(goal[stav[i][j] - 1][1] - j)  # vypocitanie vzdialenosti od cielovej pozicie
        return heu2


def posun(stav,smer):               # vrati novy stav, ak sa neda vytvorit vrati -1
    x = y = -1
    for i in range(len(stav)):      # hlada prazdnu poziciu (najvacsie cislo je volne miesto)
        if COLUMNS*ROWS in stav[i]:
            y, x = i, stav[i].index(COLUMNS*ROWS)
            break
    if x < 0 or y < 0:
        return -1

    new_x, new_y = x, y             # nove suradnice pre prazdne policko
    if smer == 'DOLAVA':
        if x < COLUMNS-1:
            new_x += 1
        else:
            return -1
    elif smer == 'DOPRAVA':
        if x > 0:
            new_x -= 1
        else:
            return -1
    elif smer == 'HORE':
        if y < ROWS-1:
            new_y += 1
        else:
            return -1
    elif smer == 'DOLE':
        if y > 0:
            new_y -= 1
        else:
            return -1
    else:
        return -1
    new_stav = copy.deepcopy(stav)
    new_stav[y][x], new_stav[new_y][new_x] = new_stav[new_y][new_x], COLUMNS*ROWS     # prehodenie prazdneho policka
    return new_stav

def zistiPosun(stav1, stav2):
    r1 = r2 = c1 = c2 = 0
    for i in range(ROWS):
        for j in range(COLUMNS):
            if stav1[i][j] == ROWS*COLUMNS:
                r1, c1 = i, j
            if stav2[i][j] == ROWS*COLUMNS:
                r2, c2 = i, j
    if c1 < c2:
        return "DOLAVA"
    elif c1 > c2:
        return "DOPRAVA"
    elif r1 < r2:
        return "HORE"
    elif r1 > r2:
        return "DOLE"
    return "BEZPOHYBU"

def vstupStav(txt):
    vstup = input(txt).split()
    stav = []
    for i in range(ROWS):
        riadok = []
        for j in range(COLUMNS):
            riadok.append(int(vstup[i * COLUMNS + j]))
        stav.append(riadok)
    return stav


#                   ZACIATOK                          #
#######################################################
ROWS = int(input("Pocet riadkov: "))           # konstanta
COLUMNS = int(input("Pocet stlpcov: "))        # konstanta
zac_stav = vstupStav("Pociatocny stav: ")
konc_stav = vstupStav("Koncovy stav: ")

goal = [[0, 0]] * ROWS*COLUMNS                   #pole suradnic, ktore su cielove (pre heuristiky)
for i in range(ROWS):
    for j in range(COLUMNS):
        goal[konc_stav[i][j] - 1] = (i, j)

zaciatok = uzol(zac_stav, None, 0, goal)
koniec = uzol(konc_stav, None, 0, goal)
sprac_stavy = {}                # list uz spracovanych STAVOV
pohyby = ('DOLAVA', 'DOPRAVA', 'HORE', 'DOLE')      # list smerov aby sa dalo nimi iterovat
halda = []              # halda na vyber najvhodnejsieho uzla

heapq.heappush(halda, zaciatok)
final = 0     # koncovy uzol
poc = 0
while len(halda) > 0:
    act = heapq.heappop(halda)       # z haldy sa vyberie najvhodnejsi uzol
    if act.stav == koniec.stav:
        final = act
        break
    for poh in pohyby:
        new_stav = posun(act.stav, poh)     # skusi sa kazdy pohyb (DOLAVA, DOPRAVA, HORE, DOLE)
        if new_stav != -1 and str(new_stav) not in sprac_stavy:  # ak je novy stav platny a este nie je spracovany
            tmp = uzol(new_stav, act, act.cena + 1, goal)
            heapq.heappush(halda, tmp)              # vlozi sa do haldy
    sprac_stavy[str(act.stav)] = poc        # do spracovanych stavov sa prida aktualny
    poc += 1

if final == 0:
    print("Riesenie neexistuje")
    quit()

act = final
riesenie = []
# naplnenie listu riesenie postupnostou stavov
while act is not None:      # dokedy sa nedostaneme k pociatocnemu stavu
    riesenie.append(act.stav)
    act = act.pred      # chod na predosly stav

# vypisanie posunov
for i in range(len(riesenie) - 1, 0, -1):
    print(zistiPosun(riesenie[i], riesenie[i - 1]))

input()
