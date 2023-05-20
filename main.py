from pygame import *
from random import randint
import os
import pygame_menu

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
kc_image = image.load("images/platforms (8) (1).png")
case_image = image.load("images/case.png")
gold_image = image.load("images/gold.png")
bomba_image = image.load("images/platform/bomba.png")


# фонова музика
mixer.music.load('music\music2.mp3')
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
        self.right_img = self.image
        self.left_img = transform.flip(self.image, True, False)

        self.speed = 3
        self.jump_speed = 12.5
        self.speed_y = 0
        self.speed_x = self.speed
        self.gravity = 1
        self.onground = False
        self.ch = False

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
    
    def collide (self, platforms):
        hits = sprite.spritecollide(self, platforms, False, sprite.collide_mask)
        if hits:
            if self.speed_y > 0:
                if self.rect.y < hits[0].rect.y:
                    self.rect.bottom = hits[0].rect.top
                self.speed_y = 0
                self.onground = True
            if self.speed_x != 0:
                self.speed_x = 0
        hits = sprite.spritecollide(self, ch, False)
        if hits:
            self.ch = True
        else:
            self.ch = False

    def update(self):
        self.speed_x = 0

        keys = key.get_pressed()

        if keys[K_UP] and self.onground:
            if self.ch:
                self.speed_y = -self.speed
            else:
                self.speed_y = -self.jump_speed
                self.onground = False
        
        if keys[K_LEFT]:
            self.speed_x = -self.speed
            self.image = self.left_img
        if keys[K_RIGHT]:
            self.speed_x = self.speed
            self.image = self.right_img

        self.speed_y += self.gravity
        self.collide(platforms)
        self.move(self.speed_x, self.speed_y)


class Text(sprite.Sprite):
    def __init__(self, text, x, y, font_size=22, font_name="Impact", color = (255, 255, 255)):
        self.font = font.SysFont(font_name, font_size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
    def draw(self):
        window.blit(self.image, self.rect)

    def set_text(self, new_text):
        self.image = self.font.render(new_text, True, self.color)

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
        super().__init__(platform_img, 35, 35, x, y)
    
class Case(GameSprite):
    def __init__(self, platform_img, x, y):
        super().__init__(platform_img, 15, 15, x, y)

class Gold(GameSprite):
    def __init__(self, platform_img, x, y):
        super().__init__(platform_img, 15, 15, x, y)

class Bomba(GameSprite):
    def __init__(self, platform_img, x, y):
        super().__init__(platform_img, 15, 15, x, y)

# створення вікна
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Платформер")

score_text = Text("Зібрано: 0", 20, 50)
#додавання фону
bg = transform.scale(bg_image, (WIDTH, HEIGHT))

# створення спрайтів
player = Player(pl_image, width = 100, height = 100, x = 200, y = HEIGHT-150)

# основні змінні для гри
run = True
finish = False
clock = time.Clock()
FPS = 60
score = 0
result_text = Text("Перемога!", WIDTH / 2 - 100, HEIGHT /2, font_size = 50)

font1 = font.SysFont("Impact", 50)
win = font1.render("YOU WIN!!!", True, (3, 66, 20))
lose = font1.render("YOU LOSE!!!", True, (255, 0, 0))


def load_level(mapfile):
    global player, platforms, trees, ch, kc, pl,case, gold, bomba
    platforms = sprite.Group()
    trees = sprite.Group()
    ch = sprite.Group()
    kc = sprite.Group()
    pl = sprite.Group()
    case = sprite.Group()
    gold = sprite.Group()
    bomba = sprite.Group()
    with open(mapfile, 'r') as file:
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
                    kc.add(Tree(kc_image, x, y))
                elif symbol == 'U':
                    player = Player(pl_image, 30, 30, x, y)
                elif symbol == 'K':
                    case.add(GameSprite(case_image, 50, 35,x, y))
                elif symbol == 'G':
                    gold.add(GameSprite(gold_image, 20, 20,x, y))
                elif symbol == 'B':
                    bomba.add(GameSprite(bomba_image, 20, 20,x, y))
                x += 35
            y += 35
            x = 0

load_level("map.txt")

level = 1

def start_the_game():
    # Do the job here !
    menu.disable()

menu = pygame_menu.Menu('Space Shooter', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='John Doe')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(window)

while run:
    window.blit(bg, (0, 0))
    # перевірка подій
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.key == K_ESCAPE:
                menu.enable()  
                menu.mainloop(window)
    if not finish:
        spritelist = sprite.spritecollide(player, gold, True)
        for collide in spritelist:
            score +=1
            score_text.set_text("Зібрано:"+str(score))
        spritelist = sprite.spritecollide(player, case, True)
        for collide in spritelist:
            result_text.set_text("YOU WIN!!!")
            load_level("map2.txt")
            level = 2
        spritelist = sprite.spritecollide(player, bomba, True)
        for collide in spritelist:
            result_text.set_text("YOU LOSE!!!")
            finish = True

        if player.rect.y > HEIGHT:
            result_text.set_text("YOU LOSE!!!")
            finish = True
        player.update()


    platforms.draw(window)
    trees.draw(window)
    ch.draw(window)
    kc.draw(window)
    case.draw(window)
    bomba.draw(window)


    score_text.draw()
    gold.draw(window)
    player.draw()
    if finish:
        result_text.draw()

    display.update()
    clock.tick(FPS)