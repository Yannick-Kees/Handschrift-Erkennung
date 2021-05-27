import pygame as pg
import numpy as np
from collections import defaultdict
from dataclasses import dataclass

# Grundeinstellung fuer das Gitter
RESOLUTION = 700    # Aufloesung der Grafik am Ende
GRID = 70           # Groess des Gitters
distance = RESOLUTION // GRID # Groesse der einzelnen Quadrate

#Starte pygame
pg.init()
screen = pg.display.set_mode([RESOLUTION, RESOLUTION] )

# Bilder importieren
# DATEIPFADE VORHER AENDERN!
cell_normal = pg.transform.scale(pg.image.load('D:\BA\Signature\ms_cell_normal.gif'), (distance, distance))
cell_marked = pg.transform.scale(pg.image.load('D:\BA\Signature\ms_cell_marked.gif'), (distance, distance))


# Anleitung
print('Linksklick: Zeichnen \t Rechtsklick: Rechnen \t n: Reset')


@dataclass
class Cell():
    
    #    Jede Zelle im Gitter wird durch ein Element der Klasse 'cell' dargestellt
    
    row : int # row der Zelle
    column : int # column der Zelle
    selected : bool = False # True=Zelle weiss   False=Zelle Schwarz, am Anfang ist jede Zelle weiss

    def show(self):
        # Zeige Zelle
        pos = (self.column * distance, self.row * distance)
        if self.selected:
            screen.blit(cell_marked, pos) # Zelle schwarz
        else:
            screen.blit(cell_normal, pos) # Zelle weiss



 
#    Als erstes die Signaturen von 0-9 berechnen lassen und in 'pattern' speichern

pattern = [
    # 0
    [1.0, 0.0, -11.5, -1286.5, 1286.5, 7.5, -14.500000000000028, 4358.833333333338, -9354.166666666675, 31690.499999999996, 5029.333333333334, -63598.99999999998, 31913.999999999993, 12.833333333347786, -1285.166666666667, -67850.16666666682, 270487.3333333336, -230457.66666666727, -298334.66666666645, 2060441.3333333328, -1585979.1666666672, -988650.6666666662, 95397.3333333333, -1623425.9999999988, 1125896.5000000002, 2974091.333333333, 246071.0, -2953889.166666666, 976783.8333333337, -27004.833333331306],
    # 1
    [0.0, -52.0, 0.0, 0.0, 0.0, 1352.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -23417.33333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 596598.1666666666],
    # 2
    [35.0, -43.0, 573.5, -488.5, -1016.5, 956.0, 5810.5, -1766.5, -11338.5, 19045.0, -11536.500000000005, -15805.500000000004, 30210.500000000007, -14578.166666666692, 78912.83333333333, -3547.666666666657, -78309.16666666674, 386558.33333333326, -239656.6666666666, -615566.1666666667, 1069041.3333333335, -628240.8333333343, -175675.66666666686, 10673.500000000047, -505239.0, 143717.83333333334, 742886.75, 524497.5833333334, -1047556.9166666667, 317243.5833333339],
    # 3
    [-1.0, -39.0, -27.5, 1048.5, -1009.5, 785.5, -45.166666666666664, -11162.500000000002, 22325.5, -21459.666666666668, -10035.500000000004, 1427.8333333333342, 19243.333333333336, -10839.166666666672, 904.3333333333283, 137765.83333333337, -451675.16666666645, 437642.58333333343, 437444.8333333335, 174774.33333333337, -1066360.6666666665, 679138.2500000001, -116408.16666666673, -187908.66666666666, 199023.33333333334, -287913.4166666667, 381672.5833333331, 218257.58333333334, -569985.4166666667, 207583.91666666692],
    # 4
    [22.0, 22.0, 209.5, 202.5, 281.5, 260.0, 1099.0, -2534.6666666666665, 8114.333333333334, -2350.5000000000014, -953.6666666666669, 9923.999999999998, -1857.0000000000002, 2183.999999999995, 6291.833333333337, -124041.33333333337, 240653.1666666668, -300520.4166666667, -77196.83333333337, 621366.3333333331, -166913.16666666672, -153815.5833333335, 10055.166666666668, -118580.33333333337, 58998.166666666686, 372015.4166666668, 9224.666666666666, -157691.3333333333, 26988.16666666669, 4511.583333333909],
    # 5
    [-28.0, -27.0, 354.5, 773.5, -17.5, 402.0, -2616.3333333333335, -10500.0, 610.0000000000002, -20548.333333333336, 322.499999999999, 19075.166666666668, -9771.33333333333, -4266.500000000016, 23125.833333333332, 191321.50000000006, -28481.50000000012, 594733.8333333333, -42978.99999999996, -617314.6666666666, 530938.3333333335, 631540.1666666672, 20314.666666666697, 11227.666666666555, -454772.3333333331, -666677.8333333336, 213898.9166666664, 125239.9166666666, 136743.91666666704, 50192.33333333291],
    # 6
    [-11.0, -26.0, 42.5, -391.5, 677.5, 356.0, -21.16666666666664, 5217.500000000002, -4982.5, 15423.333333333336, -1325.999999999999, -21018.666666666668, 1690.3333333333333, -3374.0000000000014, -931.8333333333335, -57784.666666666715, 73782.3333333334, -350337.8333333334, -30756.66666666663, 808369.166666667, -498161.833333333, -558521.8333333336, 15316.666666666668, -381188.8333333332, 443725.16666666686, 873071.1666666672, 1835.9166666666467, -318550.0833333332, 72724.9166666666, 22353.916666667006],
    # 7
    [32.0, -23.0, 1622.0, -11.0, -725.0, 6.5, 57156.666666666664, -51585.833333333336, -2978.333333333334, -7293.833333333332, -9221.833333333334, 3031.666666666666, 4486.166666666668, 8527.833333333316, 2627808.999999999, -1577787.4999999995, -1043945.5000000001, 1051482.2500000019, -71554.0000000001, 197399.49999999983, -178282.5000000003, 523441.58333333273, -140466.66666666637, -77081.16666666672, 149800.83333333296, -171160.41666666654, 184910.58333333384, -224432.41666666663, 376819.08333333395, -436398.08333333326],
    # 8
    [1.0, -1.0, -24.0, 152.0, -153.0, 29.5, -27.6666666666667, 261.66666666666777, 846.6666666666682, -14981.166666666666, -1083.3333333333317, 29879.33333333334, -14871.16666666667, -0.16666666664819382, 529.4166666666657, 9779.916666666677, -34103.08333333331, -19636.58333333317, 29806.416666666653, -5016.083333333219, -54160.0833333332, 697197.0833333329, -5256.249999999999, 23347.249999999894, 111433.25000000012, -2037815.2499999993, -66425.7499999999, 2001071.2499999998, -654283.7499999999, -34519.49999999847],
    # 9
    [-25.0, -30.0, 286.0, 758.0, -8.0, 476.5, -1947.666666666667, -8137.166666666666, -1641.666666666666, -21523.66666666667, 1207.8333333333326, 19551.333333333336, -9929.666666666664, -5265.166666666665, 16183.583333333336, 122143.41666666667, 11144.916666666637, 494718.8333333333, -8395.583333333307, -446803.4166666668, 489216.0833333332, 670622.1666666669, -9251.58333333337, -44218.08333333329, -418591.58333333314, -640075.8333333334, 194381.66666666645, 40540.16666666702, 179580.16666666718, 64615.666666667]
    ]


class Tensor():


#    Klasse fuer die Elemente der Tensoralgebra


    def __init__(self):
        # Erstelle ein leeres Element in der Tensoralgebra
        self.entries_ = []
        for i in range(1, 5):
            for _ in range(0, 2**i):
                self.entries_.append(0)  

    def __getitem__(self, key):
        # Greife auf Eintrag zu
        if key == 0 or key == 1:
            key = [key]

        n = len(key)
        index = 0-1

        # Bestimme aus dem Multiindex dein Eintrag im array
        for i in range(0, n):
            index += 2**i + key[i]*2**i

        return self.entries_[index]

    def __setitem__(self, key, value):
        # Setze Eintrag
        if key == 0 or key == 1:
            key = [key]
        n = len(key)
        index = 0-1

        # Bestimme aus dem Multiindex dein Eintrag im array
        for i in range(0, n):
            index += 2**i + key[i]*2**i

        # Setzte Eintrag    
        self.entries_[index] = value

    def __mod__(self, other): 
        #Tensorprodukt mit '%'
        # vgl. Definition 2.4
        solution=Tensor()

        # Level 1
        solution.entries_[0] = self.entries_[0] + other.entries_[0]
        solution.entries_[1] = self.entries_[1] + other.entries_[1]

        #Level 2
        for i in range(2):
            for j in range(2):
                solution[i,j]=self[i,j] + self[i]*other[j] + other[i,j]

        # Level 3
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    solution[i,j,k] = self[i,j,k] + self[i,j]*other[k] + self[i]*other[j,k] + other[i,j,k]

        # Level 4
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    for l in range(2):
                        solution[i,j,k,l] = self[i,j,k,l] + self[i,j,k]*other[l] + self[i,j]*other[k,l] + self[i,j,k]*other[l] + other[i,j,k,l]
        
        return solution


    def print(self): #Gebe Tensor aus
        print(self.entries_)
        return
# Ende Klasse



def signatur(x1, x2, y1, y2 ):
    

#    Berechne die Signatur des lineare Pfades von (x_1,y_1) nach (x_2,y_2)
#   vgl dazu Algorithmus 1 (Seite 36)


    solution = Tensor()

    #Level 1
    solution[0] = x2 - x1
    solution[1] = y2 - y1 

    #Level 2
    for i in range(2):
        for j in range(2):
            a = np.array([i,j])
            solution[i,j] = 1/2 * (((x2-x1)**np.sum(a==0)) * ((y2-y1)**np.sum(a==1)))

    # Level 3
    for i in range(2):
        for j in range(2):
            for k in range(2):
                a = np.array([i,j,k])
                solution[i,j,k]= 1/6 * (((x2-x1)**np.sum(a==0)) * ((y2-y1)**np.sum(a==1)))

    # Level 4
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    a = np.array([i,j,k,l])
                    solution[i,j,k,l]= 1/24 * (((x2-x1)**np.sum(a==0)) * ((y2-y1)**np.sum(a==1)))

    return solution



def tensor_norm(x,y):


#   Berechne den Abstand zwischen zwei Elementen der Tensoralgebra.
#   Dazu nehmen wir fast die euklidische Norm, nur skalieren wir jedes Level noch mit einem Normierungsfaktor


    if not len(x) == 30:
        print('Error')
        return 
    else:
        # Level 1
        error = abs(x[0]-y[0])+abs(x[1]-y[1])

        # Level 2
        for i in range(2, 6):
            error += (1/100) * abs(x[i]-y[i])

        # Level 3
        for i in range(6, 14):
            error += (1/100) * abs(x[i]-y[i])

        # Level 4
        for i in range(14, 30):
            error += (1/10000) * abs(x[i]-y[i])

        return error

# Erstelle ein leeres Gitter
matrix = []
for n in range(GRID*GRID):
    matrix.append(Cell(n // GRID, n % GRID))

weitermachen = True
for cell in matrix:
    cell.show()

Signatur = Tensor() #Signatur am Anfang 1
x = y = -1

while weitermachen:
    event = pg.event.wait()

    if event.type == pg.QUIT:
        weitermachen = False

    # vlg Algorithmus 2
    if event.type == pg.MOUSEMOTION:

        if event.buttons[0]:
            # Bestimme Position
            mouseX, mouseY = event.pos
            column = mouseX // distance
            row = mouseY // distance
            # Bestimme das relevante neue Feld
            i = row*GRID+column

            if i < GRID*GRID:
                cell = matrix[i]

                if not cell.selected:
                    # Markiere Zelle
                    cell.selected = True

                    if x != -1:
                        # Aktualisiere die Signatur
                        Signatur = Signatur % signatur(float(x),float(column),float(y),float(GRID-row-1))

                    x = column
                    y = GRID-row-1
                    cell.show()

   
    if event.type == pg.MOUSEBUTTONDOWN:

        if pg.mouse.get_pressed()[2]:
            print('Signatur: ')
            Signatur.print()
            print('--------')
            dictn = defaultdict(list)
            normen = []

            for k in range(0, 10):
                # Berechne Differenzen zu den vorher kalkulierten Schablonen
                x = tensor_norm(Signatur.entries_ , pattern[k])
                dictn[x].append(k)
                normen.append(x)

            # Finde die Zahl, zu der die berechnete Signatur den geringsten Abstant hat, diese steht nach dem Sortieren am Anfang    
            normen.sort()
            
            print('Das war eine ', dictn[normen[0]][0], )
            print('--------')
            print('Differenzen')
            print(dictn)

    if event.type == pg.KEYDOWN:

        if event.key == pg.K_n:
            # Wenn die Taste 'n' gedrueckt wird, wird alles resetet
            x = y = -1

            for element in matrix:
                    # Zeichen alles wieder weiss
                    element.selected = False
                    element.show()
            
            # Resette Signatur
            Signatur = Tensor()

    pg.display.flip()

pg.quit()