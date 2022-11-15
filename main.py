import pygame
from pygame.locals import *
import sys
import random
import time

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 525
WIDTH = 840
ACC = 0.5
FRIC = -0.12
FPS = 60
DEATHS = 0

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Root")
background = pygame.image.load("bg1.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player_jump = pygame.mixer.Sound("jump.mp3")
player_death = pygame.mixer.Sound("death.mp3")
theme = pygame.mixer.Sound("ambiant.mp3")
theme.play(loops=-1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("sprites/wait_right2.png")
        self.surf = pygame.transform.scale(self.surf, (72, 64))
        self.rect = self.surf.get_rect()
        self.pos = vec((108, 400))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 1
        self.direction = "right"
        self._layer = 3

    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load("sprites/wait1.png")
            self.surf = pygame.transform.scale(self.surf, (72 * (1 + (DEATHS * 0.2)), 64 * (1 + (DEATHS * 0.2))))
            self.rect = self.surf.get_rect()
            if -ACC - (DEATHS * 0.1) >= -1:
                self.acc.x = -ACC - (DEATHS * 0.1)
            else:
                self.acc.x = -1
            self.direction = "left"

        elif pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load("sprites/wait_right1.png")
            self.surf = pygame.transform.scale(self.surf, (72 * (1 + (DEATHS * 0.2)), 64 * (1 + (DEATHS * 0.2))))
            self.rect = self.surf.get_rect()
            if ACC + (DEATHS * 0.2) <= 1:
                self.acc.x = ACC + (DEATHS * 0.2)
            else:
                self.acc.x = 1
            self.direction = "right"

        elif pressed_keys[K_SPACE]:
            self.surf = pygame.image.load("sprites/jump3.png")
            self.surf = pygame.transform.scale(self.surf, (72 * (1 + (DEATHS * 0.2)), 64 * (1 + (DEATHS * 0.2))))
            self.rect = self.surf.get_rect()

        else:
            if self.direction == "right":
                self.surf = pygame.image.load("sprites/wait_right2.png")
                self.surf = pygame.transform.scale(self.surf, (72 * (1 + (DEATHS * 0.2)), 64 * (1 + (DEATHS * 0.2))))
                self.rect = self.surf.get_rect()
            else:
                self.surf = pygame.image.load("sprites/wait2.png")
                self.surf = pygame.transform.scale(self.surf, (72 * (1 + (DEATHS * 0.2)), 64 * (1 + (DEATHS * 0.2))))
                self.rect = self.surf.get_rect()

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

#        if self.pos.x > WIDTH:
#            self.pos.x = 0
#        if self.pos.x < 0:
#            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollideany(self, platforms)
        if hits and not self.jumping:
            self.jumping = True
            if -15 - (DEATHS * 2) >= -25:
                self.vel.y = -15 - (DEATHS * 2)
            else:
                self.vel.y = -25

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)

        pygame.sprite.collide_mask
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        #self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

class platform(pygame.sprite.Sprite):
    def __init__(self, width=0, height=18):
        super().__init__()

        if width == 0: width = random.randint(50, 120)

        self.image = pygame.image.load("bg2.png")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))
        self.speed = random.randint(-1, 1)

        self.point = True
        self.moving = True
        self._layer = 1

    def move(self):
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

class checkpoint(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("sprites/sapling1.png")
        self.surf = pygame.transform.scale(self.surf, (100, 100))
        self.rect = self.surf.get_rect(center=(WIDTH / 8, HEIGHT - 40))
        self._layer = 2

    def move(self):
        self.moving = False

def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (
                    abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False


def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50, 100)
        p = platform()
        C = True
        while C:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH),
                             random.randrange(0, HEIGHT))
            C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)

def lvl1_gen():
    lvl1 = platform()
    lvl1.surf = pygame.Surface((WIDTH, 20))
    lvl1.surf.fill((139, 89, 82))
    lvl1.rect = lvl1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
    return lvl1

def lvl2_gen():
    lvl2_sprites = pygame.sprite.Group()
    lvl2_left = platform()
    lvl2_left.surf = pygame.Surface((WIDTH / 4, 20))
    lvl2_left.surf.fill((139, 89, 82))
    lvl2_left.rect = lvl2_left.surf.get_rect(center=(WIDTH / 8, HEIGHT - 10))
    lvl2_sprites.add(lvl2_left)

    lvl2_right = platform()
    lvl2_right.surf = pygame.Surface((WIDTH / 4, 20))
    lvl2_right.surf.fill((139, 89, 82))
    lvl2_right.rect = lvl2_right.surf.get_rect(center=(WIDTH - WIDTH / 8, HEIGHT - 10))
    lvl2_sprites.add(lvl2_right)

    return lvl2_sprites

def lvl3_gen():
    lvl3 = platform()
    lvl3.surf = pygame.Surface((WIDTH, 20))
    lvl3.surf.fill((77, 113, 50))
    lvl3.rect = lvl3.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
    return lvl3

P1 = Player()

all_sprites = pygame.sprite.Group()

layers = pygame.sprite.LayeredUpdates
layers.add(P1)

all_sprites.add(P1)
platforms = pygame.sprite.Group()

lvl1 = lvl1_gen()

all_sprites.add(lvl1)
platforms.add(lvl1)
lvl1.moving = False
lvl1.point = False
new_lvl = False

for x in range(random.randint(4, 5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
layers.add(platforms)

while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
                player_jump.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    if P1.rect.top > HEIGHT:
        player_death.play()
        pygame.time.wait(5000)
        P1.pos = vec((108, 400))
        DEATHS += 1
        P1.vel = vec(0, 0)
        #for entity in all_sprites:

        #    time.sleep(1)
        #    pygame.display.update()
        #    time.sleep(1)
        #    pygame.quit()
        #    sys.exit()

    #if P1.rect.top <= HEIGHT / 3:
    #    P1.pos.y += abs(P1.vel.y)
    #    for plat in platforms:
    #        plat.rect.y += abs(P1.vel.y)
    #        if plat.rect.top >= HEIGHT:
    #            plat.kill()

    if P1.pos.x > WIDTH:
        if P1.score == 3:
            P1.pos.x = WIDTH
        else:
            P1.pos.x = 0
            P1.score += 1
            new_lvl = True
            for plat in platforms:
                plat.kill()
    if P1.pos.x < 0:
        P1.pos.x = 0


    if new_lvl and P1.score == 2:
        new_lvl = False
        lvl2 = lvl2_gen()
        checkpoint1 = checkpoint()
        layers.add(checkpoint1)
        all_sprites.add(checkpoint1)
        for plat in lvl2:
            all_sprites.add(plat)
            platforms.add(plat)
            plat.moving = False
            plat.point = False
    if new_lvl and P1.score == 3:
        new_lvl = False
        lvl3 = lvl3_gen()
        checkpoint1.kill()
        tree = checkpoint()
        tree.surf = pygame.image.load("sprites/bg3.png")
        tree.surf = pygame.transform.scale(tree.surf, (500, 500))
        tree.rect = tree.surf.get_rect(center=(WIDTH / 2, HEIGHT - 250))
        layers.add(tree)
        all_sprites.add(tree)
        all_sprites.add(lvl3)
        platforms.add(lvl3)
        lvl3.moving = False
        lvl3.point = False

    displaysurface.blit(background, (0, 0))

    f = pygame.font.SysFont("Verdana", 20)
    lvl_counter = f.render("Level " + str(P1.score), True, (0, 0, 255))
    displaysurface.blit(lvl_counter, (WIDTH / 2, 10))

    death_counter = f.render("Tries: " + str(DEATHS), True, (0, 0, 255))
    displaysurface.blit(death_counter, (WIDTH / 2, 30))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    pygame.display.update()
    FramePerSec.tick(FPS)
