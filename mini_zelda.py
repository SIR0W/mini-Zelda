import pygame
import sys
import random

class Arbre:
    def __init__(self, x, y):
        self.rect_a = pygame.Rect(x, y, 40, 70)
        self.x = x
        self.y = y

    def dessiner(self, ecran):
        pygame.draw.rect(ecran, (30, 100, 30), pygame.Rect(self.x - 4, self.y + 10, 20, 20))
        pygame.draw.rect(ecran, (40, 160, 30), pygame.Rect(self.x, self.y, 40, 50))
        pygame.draw.rect(ecran, (30, 100, 30), pygame.Rect(self.x + 24, self.y + 20, 20, 20))
        pygame.draw.rect(ecran, (80, 60, 10), pygame.Rect(self.x+12,self.y+50,16,20))

class Caillou:
    def __init__(self, x, y):
        self.rect_c = pygame.Rect(x, y, 44, 46)
        self.x = x
        self.y = y

    def dessiner(self, ecran):
        pygame.draw.rect(ecran, (158, 158, 158), pygame.Rect(self.x, self.y, 40, 40))
        pygame.draw.rect(ecran, (100, 100, 100), pygame.Rect(self.x+20,self.y+26,24,20))

class TP:
    def __init__(self, x, y, x_new, y_new, long, larg, carte):
        self.rect_tp = pygame.Rect(x, y, long, larg)
        self.x = x
        self.y = y
        self.x_new = x_new
        self.y_new = y_new
        self.carte = carte

    def dessiner(self, ecran):
        pygame.draw.rect(ecran, (255, 0, 255), pygame.Rect(self.x, self.y, 40, 20))

    def new_xy(self,x_joueur, y_joueur):
        return self.x_new, self.y_new

    def new_map(self):
        return self.carte

class Fantome:
    def __init__(self, x, y, vie_fantome, inv_f):
        self.rect_f = pygame.Rect(x-10, y-10, 20, 25)
        self.rect_f_d = pygame.Rect(x-200, y-200, 400, 400)
        self.x = x
        self.y = y
        self.vie_fantome = vie_fantome
        self.inv_f = inv_f

    def dessiner(self, ecran):
        if self.inv_f <= 0:
            color_f = (255, 255, 255)
        else:
            color_f = (255, 0, 0)
        #pygame.draw.rect(ecran, (158, 158, 158), self.rect_f_d)
        pygame.draw.rect(ecran, color_f, self.rect_f)
        pygame.draw.rect(ecran, (100, 100, 100), pygame.Rect(self.x-8, self.y-6, 6, 4))
        pygame.draw.rect(ecran, (100, 100, 100), pygame.Rect(self.x+2, self.y-6, 6, 4))
        pygame.draw.rect(ecran, (100, 100, 100), pygame.Rect(self.x-6, self.y, 12, 2))

        pygame.draw.rect(ecran, color_f, pygame.Rect(self.x -10, self.y + 15, 4, 2))
        pygame.draw.rect(ecran, color_f, pygame.Rect(self.x -10, self.y + 17, 2, 2))
        pygame.draw.rect(ecran, color_f, pygame.Rect(self.x -4, self.y + 15, 8, 2))
        pygame.draw.rect(ecran, color_f, pygame.Rect(self.x -2, self.y + 17, 4, 2))
        pygame.draw.rect(ecran, color_f, pygame.Rect(self.x + 6, self.y + 15, 4, 2))
        pygame.draw.rect(ecran, color_f, pygame.Rect(self.x + 8, self.y + 17, 2, 2))

    def animation_f(self, ecran):
        pygame.draw.rect(ecran, (100, 100, 100), pygame.Rect(self.x-6, self.y, 12, 8))

    def touch(self):
        return joueur_rect.colliderect(self.rect_f)

    def touch_degat(self, attaque_rect, degat_attaque):
        if attaque_rect.colliderect(self.rect_f) and self.inv_f <= 0:
            return Fantome(self.x, self.y, self.vie_fantome - degat_attaque, 60)
        return Fantome(self.x, self.y, self.vie_fantome, self.inv_f)

    def mort(self):
        if self.vie_fantome <= 0:
            return Fantome(0,0,100,0)
        return Fantome(self.x, self.y, self.vie_fantome, self.inv_f)

    def target(self, x_joueur, y_joueur, ecran):
        if joueur_rect.colliderect(self.rect_f):
            return Fantome(self.x + random.choice((-170,170)), self.y + random.choice((-170,170)), self.vie_fantome, self.inv_f)

        new_xf=0
        new_yf=0
        if x_joueur <= self.x :
            new_xf = self.x - 1
        elif x_joueur > self.x :
            new_xf = self.x + 1
        if y_joueur <= self.y :
            new_yf = self.y - 1
        elif y_joueur > self.y :
            new_yf = self.y + 1
        return Fantome(new_xf , new_yf, self.vie_fantome, self.inv_f-1)

class Vie:

    def __init__(self, vie_max, vie_joueur):
        self.vie_max = vie_max
        self.vie_joueur = vie_joueur

    def dessiner(self):
        pygame.draw.rect(ecran, (0, 0, 0), pygame.Rect(10, 20, 4, 16))
        pygame.draw.rect(ecran, (0, 0, 0), pygame.Rect(10,32,self.vie_max//2+4,4))
        pygame.draw.rect(ecran, (0, 0, 0), pygame.Rect(10,20,self.vie_max//2+4,4))
        pygame.draw.rect(ecran, (0, 0, 0), pygame.Rect(self.vie_max//2+14, 20, 4, 16))
        pygame.draw.rect(ecran, (255, 0, 0), pygame.Rect(14, 24, self.vie_joueur//2, 8))

class Attaque:
    def __init__(self, x_joueur, y_joueur, face, arme):
        if arme == 1:
            if face == 0:
                x_att = -10
                y_att = -40
                x_arme = 50
                y_arme = 40
            elif face == 1:
                x_att = 30
                y_att = -10
                x_arme = 40
                y_arme = 50
            elif face == 2:
                x_att = -10
                y_att = 30
                x_arme = 50
                y_arme = 40
            elif face == 3:
                x_att = -40
                y_att = -10
                x_arme = 40
                y_arme = 50
        elif arme == 2:
            if face == 0:
                x_att = 0
                y_att = -70
                x_arme = 30
                y_arme = 70
            elif face == 1:
                x_att = 30
                y_att = 0
                x_arme = 70
                y_arme = 30
            elif face == 2:
                x_att = 0
                y_att = 30
                x_arme = 30
                y_arme = 70
            elif face == 3:
                x_att = -70
                y_att = 0
                x_arme = 70
                y_arme = 30
        elif arme == 3:
            if face == 0:
                x_att = -25
                y_att = -30
                x_arme = 80
                y_arme = 50
            elif face == 1:
                x_att = 10
                y_att = -25
                x_arme = 50
                y_arme = 80
            elif face == 2:
                x_att = -25
                y_att = 10
                x_arme = 80
                y_arme = 50
            elif face == 3:
                x_att = -30
                y_att = -25
                x_arme = 50
                y_arme = 80

        self.rect_att = pygame.Rect(x_joueur + x_att, y_joueur + y_att, x_arme, y_arme)
        self.x_joueur = x_joueur
        self.y_joueur = y_joueur
        self.face = face

    def dessiner(self):
        if arme == 1:
            color_att = (254, 27, 0)
            pygame.draw.rect(ecran, color_att, self.rect_att )
        elif arme == 2:
            color_att = (170, 211, 233)
            pygame.draw.rect(ecran, color_att, self.rect_att )
        elif arme == 3:
            color_att = (80, 41, 0)
            pygame.draw.rect(ecran, color_att, self.rect_att )
            if face == 0:
                pygame.draw.rect(ecran, (158, 158, 158), pygame.Rect(x_joueur - 10 , y_joueur -10, 5, 5) )
            elif face == 1:
                pygame.draw.rect(ecran, (158, 158, 158), pygame.Rect(x_joueur + 10, y_joueur , 5, 5) )
            elif face == 2:
                pygame.draw.rect(ecran, (158, 158, 158), pygame.Rect(x_joueur + 10, y_joueur +10, 5, 5) )
            elif face == 3:
                pygame.draw.rect(ecran, (158, 158, 158), pygame.Rect(x_joueur - 10, y_joueur + 5, 5, 5) )

    def collision(self):
        return self.rect_att

def type_arme(arme):
    if arme == 1:
        return 50, 15, 10
    elif arme == 2:
        return 20, 7, 5
    elif arme == 3:
        return 70, 20, 25


def terrain(ecran):
    ecran.fill((120, 210, 140))

def routes(n_map):
    if n_map == 0:
        pygame.draw.rect(ecran, (220, 173, 127), pygame.Rect(370, 0, 35, 200))
        pygame.draw.rect(ecran, (220, 173, 127), pygame.Rect(370, 200, 200, 35))
        pygame.draw.rect(ecran, (220, 173, 127), pygame.Rect(535, 235, 35, 365))
        pygame.draw.rect(ecran, (220, 173, 127), pygame.Rect(0, 400, 300, 35))
        pygame.draw.rect(ecran, (220, 173, 127), pygame.Rect(265, 435, 35, 35))
        pygame.draw.rect(ecran, (220, 173, 127), pygame.Rect(265, 470, 300, 35))

pygame.init()

largeur, hauteur = 800, 600
ecran = pygame.display.set_mode((largeur, hauteur), pygame.FULLSCREEN)
pygame.display.set_caption("Mini Zelda")

rouge = (255, 0, 0)

arme = 3
degat_attaque, durée_imob, durée_no_attaque = type_arme(arme)

imob = -1
no_attaque = -1

n_map = 0
face = 0
vie_max = 300
vie_joueur = 300
x_joueur, y_joueur = 50, 50
x_joueur_precedent, y_joueur_precedent = x_joueur, y_joueur

monde = [[
[Arbre(200, 150), Arbre(400, 300), Arbre(600, 100), Arbre(100, 500)]
,[Caillou(60, 320), Caillou(650, 460), Caillou(450, 30)]
,[TP(0,-20 , 380, 570, 800, 20, 1),TP(0,600 , 380, 0, 800, 20, 1)]
,[Fantome(200, 250, 100, 0)]]
,[[Arbre(20, 150), Arbre(40, 300), Arbre(600, 10), Arbre(10, 500)]
,[Caillou(260, 350), Caillou(650, 40), Caillou(450, 30)]
,[TP(0,-20 , 380, 570, 800, 20, 0),TP(0,600 , 380, 0, 800, 20, 0)]
,[Fantome(100, 100, 100, 0)]
]]

arbres = monde[0][0]
cailloux = monde[0][1]
tps = monde[0][2]
fantomes = monde[0][3]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    terrain(ecran)
    routes(n_map)

    touches = pygame.key.get_pressed()

    # imobilisation sans attaquer

    if no_attaque >= 0 or imob == 0:
        if imob == 0:
            imob = -1
            no_attaque = durée_no_attaque
        no_attaque -= 1

    # l attaque doit durée et etre detecter
    elif touches[pygame.K_m] or imob > 0 :
        if imob < 0:
            imob = durée_imob
        attaque_rect = Attaque(x_joueur, y_joueur, face, arme)
        Attaque.dessiner(attaque_rect)
        imob -= 1



    else:
        attaque_rect = Attaque(800, 800, 0, arme)
        if touches[pygame.K_q]:
            x_joueur -= 2
            face = 3
        if touches[pygame.K_d]:
            x_joueur += 2
            face = 1
        if touches[pygame.K_z]:
            y_joueur -= 2
            face = 0
        if touches[pygame.K_s]:
            y_joueur += 2
            face = 2


    joueur_rect = pygame.Rect(x_joueur, y_joueur, 30, 30)
    for arbre in arbres:
        arbre.dessiner(ecran)

        if joueur_rect.colliderect(arbre.rect_a):
            x_joueur, y_joueur = x_joueur_precedent, y_joueur_precedent

    for caillou in cailloux:
        caillou.dessiner(ecran)

        if joueur_rect.colliderect(caillou.rect_c):
            x_joueur, y_joueur = x_joueur_precedent, y_joueur_precedent

    for tp in tps:
        tp.dessiner(ecran)

        if joueur_rect.colliderect(tp.rect_tp):
            x_joueur, y_joueur = TP.new_xy(tp,x_joueur, y_joueur)
            n_map = TP.new_map(tp)
            arbres = monde[n_map][0]
            cailloux = monde[n_map][1]
            tps = monde[n_map][2]
            fantomes = monde[n_map][3]

    z=0
    for fantome in fantomes:

        if joueur_rect.colliderect(fantome.rect_f_d):
            fantomes[z] = fantome.target(x_joueur, y_joueur, ecran)
            fantome = fantomes[z]
            fantomes[z] = fantome.touch_degat(Attaque.collision(attaque_rect), degat_attaque)
            fantome = fantomes[z]
            if fantome.touch():
                vie_joueur -= 150

        fantomes[z] = fantome.mort()
        fantome.dessiner(ecran)

        if joueur_rect.colliderect(fantome.rect_f_d):
            fantome.animation_f(ecran)

        z+=1

    Vie.dessiner(Vie(vie_max,vie_joueur))

    pygame.draw.rect(ecran, rouge, (x_joueur, y_joueur, 30, 30))

    pygame.display.flip()

    x_joueur_precedent, y_joueur_precedent = x_joueur, y_joueur

    pygame.time.Clock().tick(60)


