from pygame import *
from random import randint
import os

init()
font.init()
mixer.init()

# розміри вікна
WIDTH, HEIGHT = 900, 600

# картинка фону
bg_image = image.load("images/phone2.jpg")
#картинки для спрайтів
pl_image = image.load("images/boys/boys__1_-removebg-preview.png")
platform_image = image.load("images/platform/platforms (1).png")
platform_image2 = image.load("images/platform/platforms (4).png")
tree_image = image.load("images/trees__2_-removebg-preview.png")
tree_image2 = image.load("images/trees__3_-removebg-preview.png")
tree_image3 = image.load("images/trees__4_-removebg-preview.png")
ch_image = image.load("images/platforms__7_-removebg-preview (1) (2).png")
kc_image = image.load("images\platforms (8) (1).png")
case_image = image.load("images\case.png")
gold_image = image.load("images\gold.png")


# фонова музика
mixer.music.load('music/music1.ogg')
mixer.music.set_volume(0.3)
mixer.music.play(-1)



# класи
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y, speed = 3):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.mask = mask.from_surface(self.image)  

    def draw(self): #відрисовуємо спрайт у вікні
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self, sprite_img, width, height, x, y, speed = 3):
        super().__init__(sprite_img, width, height, x, y, speed)
        self.speed = 3
        self.jump_speed = 10
        self.speed_y = 0
        self.gravity = 1
        self.onground = False

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
    
    def collide (self, platforms):
        for pl in platforms:
            if self.rect.colliderect(pl.rect):
                if self.rect.y <= pl.rect.y:
                    self.onground = True
                    self.rect.bottom = pl.rect.top
                else:
                    self.onground = False
                    self.speed_y = 3
            else:
                self.onground = False 

    def update(self):
        self.speed_x = 0

        keys = key.get_pressed()
        if keys[K_UP] and self.onground:
            self.speed_y = -self.jump_speed
            self.onground = False
        if keys[K_DOWN]:
            self.speed_y = self.speed
        if keys[K_LEFT]:
           self.speed_x = -self.speed
        if keys[K_RIGHT]:
           self.speed_x = self.speed

        if self.speed_y < 10 and not self.onground:
            self.speed_y += self.gravity
        if self.speed_y > 0 and self.onground:
            self.speed_y = 0

        self.collide(platforms)
        self.move(self.speed_x, self.speed_y)

class Platform(GameSprite):
    def __init__(self, platform_img, x, y):
        super().__init__(platform_img, 35, 35, x, y)

class Platform2(GameSprite):
    def __init__(self, platform_img, x, y):
        super().__init__(platform_img, 35, 35, x, y)

class Tree(GameSprite):
    def __init__(self, platform_img, x, y):
        super().__init__(platform_img, 50, 85, x, y)

class Tree2(GameSprite):
    def __init__(self, platform_img, x, y):
        super().__init__(platform_img, 20, 10, x, y)

class Tree3(GameSprite):
    def __init__(self, platform_img, x, y):
        super().__init__(platform_img, 15, 30, x, y)

class Ch(GameSprite):
    def __init__(self, platform_img, x, y):
        super().__init__(platform_img, 15, 30, x, y)

class Kc(GameSprite):
    def __init__(self, platform_img, width, height, x, y):
        super().__init__(platform_img, 15, 15, x, y)
    
class Case(GameSprite):
    def __init__(self, platform_img, x, y):
        super().__init__(platform_img, 15, 15, x, y)

class Gold(GameSprite):
    def __init__(self, platform_img, x, y):
        super().__init__(platform_img, 15, 15, x, y)

# створення вікна
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Платформер")


#додавання фону
bg = transform.scale(bg_image, (WIDTH, HEIGHT))

# створення спрайтів
player = Player(pl_image, width = 100, height = 100, x = 200, y = HEIGHT-150)




# основні змінні для гри
run = True
finish = False
clock = time.Clock()
FPS = 60

platforms = sprite.Group()
trees = sprite.Group()
ch = sprite.Group()
kc = sprite.Group()
pl = sprite.Group()
case = sprite.Group()
gold = sprite.Group()

with open('map.txt', 'r') as file:
    x, y = 0, 0
    map = file.readlines()
    for line in map:
        for symbol in line:
            if symbol == 'W':
                platforms.add(Platform(platform_image, x, y))
            elif symbol == 'S':
                platforms.add(Platform(platform_image2, x, y))
            elif symbol == 'T':
                trees.add(Tree(tree_image, x, y))
            elif symbol == 'E':
                trees.add(Tree(tree_image2, x, y))
            elif symbol == 'Q':
                trees.add(Tree(tree_image3, x, y))
            elif symbol == 'R':
                ch.add(Tree(ch_image, x, y))
            elif symbol == 'Y':
                kc.add(Tree(kc_image, 35, 35, x, y))
            elif symbol == 'U':
                pl.add(Player(pl_image, 30, 30, x, y))
            elif symbol == 'K':
                kc.add(GameSprite(case_image, 50, 35,x, y))
            elif symbol == 'G':
                kc.add(GameSprite(gold_image, 20, 20,x, y))
            x += 35
        y += 35
        x = 0
# ігровий цикл
while run:
    window.blit(bg, (0, 0))
    # перевірка подій
    for e in event.get():
        if e.type == QUIT:
            run = False

    player.update()

    platforms.draw(window)
    trees.draw(window)
    ch.draw(window)
    kc.draw(window)
    pl.draw(window)
    case.draw(window)
    gold.draw(window)
    display.update()
    clock.tick(FPS)