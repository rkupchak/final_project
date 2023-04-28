from pygame import *
from random import randint
import os

init()
font.init()
mixer.init()

# розміри вікна
WIDTH, HEIGHT = 900, 600

# картинка фону
bg_image = image.load("images\phone2.jpg")
#картинки для спрайтів
fire_image = image.load("images/fieboy.png")
water_image = image.load("images/watergirl2.png")


# фонова музика
mixer.music.load('music\music1.ogg')
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

class Player1(GameSprite):
    def update(self): #рух спрайту
        keys_pressed = key.get_pressed() 
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < WIDTH - 70:
            self.rect.x += self.speed
    
class Player2(GameSprite):
    def update(self): #рух спрайту
        keys_pressed = key.get_pressed() 
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < WIDTH - 70:
            self.rect.x += self.speed
        

        
    def draw(self): #відрисовуємо спрайт у вікні
        window.blit(self.image, self.rect)
    


# створення вікна
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Вогонь і вода")



#додавання фону
bg = transform.scale(bg_image, (WIDTH, HEIGHT))

# створення спрайтів
player = Player1(fire_image, width = 100, height = 100, x = 200, y = HEIGHT-150)
player = Player2(water_image, width = 100, height = 100, x = 300, y = HEIGHT-150)



# основні змінні для гри
run = True
finish = False
clock = time.Clock()
FPS = 60


# ігровий цикл
while run:
    window.blit(bg, (0, 0))
    # перевірка подій
    for e in event.get():
        if e.type == QUIT:
            run = False
    display.update()
    clock.tick(FPS)