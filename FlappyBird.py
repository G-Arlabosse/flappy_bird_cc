import pygame
import random
import math
import os
import time
pygame.font.init()

WIN_WIDTH = 500 # Largeur de la fenêtre
WIN_HEIGHT = 800 # Heuteur de la fenêtre

BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("flappybird", "bg.png")))
BASE = pygame.transform.scale2x(pygame.image.load(os.path.join("flappybird", "base.png")))
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("flappybird", "pipe.png")))

def draw_window(win, bird, base): # Permet d'afficher les éléments souhaités
    win.blit(BACKGROUND, (0, 0)) # L'ordre des draw est important !
    bird.draw(win) # Afficher l'oiseau
    base.draw(win) # Afficher le sol
    pygame.display.update() # Permet d'actualiser la fenêtre


def main():
    run = True # Une variable qui nous permettre de savoir quand stopper le jeu
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # Initialisation de la fenêtre
    clock = pygame.time.Clock() # Permet de calculer le temps entre chaque boucle
    bird = Bird(230, 350) # Création de notre oiseau
    base = Base(730) # Création du sol
    pipes = [Pipe(600)] # Création d'un tableau du tuyau

    while (run):
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Ferme la fenêtre si on clique sur la croix en haut à droite
                run = False
                pygame.quit()
                quit()
    if base.collide(bird):
        pygame.quit()
        quit()
        pipe_ind = 0

        draw_window(win, bird, base)
        bird.move()
        base.move()
        pipe.move()
        add_pipe = False
        rem = []

        for pipe in pipes:
            if pipe.collide(bird):
                main()
            if (not (pipe.passed) and (pipe.x < bird.x)):
                pipe.passed = True
                add_pipe = True

            if (pipe.x + pipe.PIPE_TOP.get_width() < 0):
                rem.append(pipe)
            pipe.move()

        if add_pipe:
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

BIRDS = [pygame.transform.scale2x(pygame.image.load(os.path.join("flappybird", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("flappybird", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("flappybird", "bird3.png")))] # Création d'un tableau qui contient toutes les images de notre oiseau

class Bird:
    IMGS = BIRDS # Initialisation des variables utiles
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x # Initialisation des variables de notre classe Bird
        self.y =y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self): # La fonction qui permettra de sauter
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self): # Cette fonction nous permet de faire bouger l'oiseau, c'est-à-dire le faire tomber si rien ne se passe
        self.tick_count += 1
        d = self.velocity * self.tick_count + 0.5 * 3 * self.tick_count**2

        if d >= 16:
            d = ((d / abs(d)) * 16)
        if d <= 0:
            d -= 2
        self.y = self.y + d
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win): # Cette fonction permet d'animer notre oiseau, le voir battre des ailes
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:             # On commence à la 1ère image, A chaque tour de boucle on change d'image.
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1: # Attention, une fois que nous avons atteint notre 3ème image, il faut retourner au début car notre oiseau n'a que 3 images dans son tableau
            self.img = self.IMGS[0]

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Base:
    VEL = 5
    WIDTH = BASE.get_width()
    IMG = BASE

    def __init__(self, y):
        self.y = y # Initialisation des variables de notre classe Base
        self.x1 = 0
        self.x2 = self.WIDTH


    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
                                           # Comme nous n'avons qu'une image base
        if (self.x1 + self.WIDTH) < 0:     # et que la taille en largeur de la fenêtre
            self.x1 = self.x2 + self.WIDTH # représente une base. Il faut faire en sorte
                                           # de déplacer une fois l'image vers la gauche
        if (self.x2 + self.WIDTH) < 0:     # et ensuite réafficher la même image juste après
            self.x2 = self.x1 + self.WIDTH # pour qu'on ait une impression de déplacement

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

    def collide(self, bird):
        if bird.y > self.y:
            return True
        return False


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.bottom = 0
        self.top = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE, False, True)
        self.PIPE_BOTTOM = PIPE
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top -round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if (t_point or b_point):
            return True
        return False

if __name__ == "__main__":
    main()