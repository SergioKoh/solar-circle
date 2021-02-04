# game hit the balls

import pygame
from pygame.draw import *
from random import randint
from tkinter import *

pygame.init()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
FPS = 75
WIDTH = 1200
HEIGHT = 800
score = 0
bang_rect = [0] * 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.time.set_timer(pygame.USEREVENT, 500)


class Ball(pygame.sprite.Sprite):
    """Class of colored balls"""

    def __init__(self):
        super().__init__()
        self.x = randint(int(0.1 * WIDTH), int(0.9 * WIDTH))
        self.y = randint(int(0.1 * HEIGHT), int(0.9 * HEIGHT))
        self.radius = randint(10, min(WIDTH, HEIGHT) // 10)
        self.d = self.radius * 2
        self.color = COLORS[randint(0, 5)]
        self.speed = [randint(-3, 3) for sp in range(2)]
        if self.speed == [0, 0]:
            self.speed = [1, 1]
        self.image = pygame.Surface((self.d, self.d))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        circle(self.image, self.color, (self.radius, self.radius), self.radius)

    def update(self):
        self.rect.move_ip(self.speed)
        screen.blit(self.image, self.rect)

        # accidental reflection off walls

        if self.rect.right > WIDTH:
            self.speed[0] = -self.speed[0]
            self.speed[1] = randint(-3, 3)
        elif self.rect.left < 0:
            self.speed[0] = -self.speed[0]
            self.speed[1] = randint(-3, 3)
        elif self.rect.bottom > HEIGHT:
            self.speed[1] = -self.speed[1]
            self.speed[0] = randint(-3, 3)
        elif self.rect.top < 0:
            self.speed[1] = -self.speed[1]
            self.speed[0] = randint(-3, 3)

        # collision of balls

        coll_ball = pygame.sprite.spritecollideany(self, balls,
                                                   pygame.sprite.collide_circle)
        if coll_ball:
            coll_ball.speed[0], self.speed[0] = self.speed[0], coll_ball.speed[0]
            coll_ball.speed[1], self.speed[1] = self.speed[1], coll_ball.speed[1]

        pygame.sprite.spritecollide(ball, rockets, True, pygame.sprite.collide_circle)


class Rocket(pygame.sprite.Sprite):
    """Color rocket class"""

    def __init__(self):
        super().__init__()
        self.x = randint(int(0.1 * WIDTH), int(0.9 * WIDTH))
        self.y = randint(int(1.1 * HEIGHT), int(1.5 * HEIGHT))
        self.w = randint(10, min(WIDTH, HEIGHT) // 10)
        self.h = self.w + randint(10, min(WIDTH, HEIGHT) // 10)
        self.color = COLORS[randint(0, 5)]
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.speedy = [randint(-1, 1), randint(-5, -1)]
        self.rect.center = self.x, self.y

    def update(self):
        self.rect.move_ip(self.speedy)
        screen.blit(self.image, self.rect)

        # accidental reflection off walls

        if self.rect.bottom < 0:
            self.x = randint(int(0.1 * WIDTH), int(0.9 * WIDTH))
            self.y = randint(int(1.1 * HEIGHT), int(1.5 * HEIGHT))
            self.rect.center = self.x, self.y
        if self.rect.right > WIDTH:
            self.speedy[0] = -self.speedy[0]
            self.speedy[1] = self.speedy[1]
        elif self.rect.left < 0:
            self.speedy[0] = -self.speedy[0]
            self.speedy[1] = self.speedy[1]

        # collision of rockets

        coll_rocket = pygame.sprite.spritecollideany(self, rockets, pygame.sprite.collide_rect)
        if coll_rocket:
            coll_rocket.speedy[0], self.speedy[0] = self.speedy[0], coll_rocket.speedy[0]
            coll_rocket.speedy[1], self.speedy[1] = self.speedy[1], coll_rocket.speedy[1]

        pygame.sprite.spritecollide(rocket, balls, True, pygame.sprite.collide_circle)


def click():
    """click handling"""
    global score, finished
    flag = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.USEREVENT:
            for j in range(4):
                bang_rect[j] = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            score -= 1
            for ball in balls:
                if ball.rect.collidepoint(event.pos):
                    score += 1 + 100 // ball.radius
                    for k in range(3):
                        bang_rect[k] = ball.rect[k]
                    bang_rect[3] = ball.color
                    sound1 = pygame.mixer.Sound('bang1.mp3')
                    sound1.play(maxtime=1000)
                    flag = True
                    ball.kill()
                    ball = Ball()
                    balls.add(ball)
                for rocket in rockets:
                    if rocket.rect.collidepoint(event.pos):
                        score += 5 + int(100 / rocket.w)
                        for n in range(3):
                            bang_rect[n] = rocket.rect[n]
                        bang_rect[3] = rocket.color
                        sound1 = pygame.mixer.Sound('bang1.mp3')
                        sound1.play(maxtime=1000)
                        flag = True
                        rocket.kill()
                        rocket = Rocket()
                        rockets.add(rocket)
            if not flag:
                sound2 = pygame.mixer.Sound('swish1.mp3')
                sound2.play(maxtime=1000)


def scoreboard():
    """scoring
    """

    font = pygame.font.Font(None, 36)
    text = font.render('SCORE:  ' + str(score), True, (180, 180, 180))
    text_rect = text.get_rect()
    text_rect.center = (600, 40)
    screen.blit(text, text_rect)


def surface_bang(b_rect):
    x, y, d, color = b_rect
    imageb = pygame.Surface((d, d))
    imageb.set_colorkey(BLACK)
    rectb = imageb.get_rect()
    rectb.topleft = x, y
    polygon(imageb, color, [(0, 0), (d // 3, d // 5), (d // 2, d // 8),
                            (d // 1.5, d // 4), (d // 1.1, d // 8),
                            (d // 1.3, d // 2), (d // 1.1, d // 1.1),
                            (d // 2, d // 1.8), (d // 4, d // 1.5),
                            (d // 3, d // 2), (d // 12, d // 2.2),
                            (d // 6, d // 2.2)], 2)
    screen.blit(imageb, rectb)


def name_entry(event):

    players[len(players)-1][0] = str(player_name.get())
    root.destroy()




# main loop
balls = pygame.sprite.Group()
rockets = pygame.sprite.Group()
for i in range(5):
    ball = Ball()
    balls.add(ball)
    rocket = Rocket()
    rockets.add(rocket)

balls.draw(screen)
pygame.display.update()

players = []
for i in open('victors.txt'):
    players.append(eval(i))
if len(players) < 10:
    players.append([f'Player № 0{len(players)+1}', score])

root = Tk()

tk_size = [0] * 2
tk_size = root.winfo_screenwidth(), root.winfo_screenheight()
str_geometry = f'{WIDTH // 3}x{HEIGHT // 3}+{tk_size[0] // 2 - WIDTH // 6}+{tk_size[1] // 2 - HEIGHT // 3}'
root.geometry(str_geometry)
request = Label(root, text="Enter your name:", height=3, font=("Comic Sans MS", 10, "bold"))
request.pack(side=TOP)
player_name = Entry(root, bd=5, font=("Comic Sans MS", 12, "bold"))
player_name.pack(side=TOP)
player_name.insert(0, players[len(players)-1][0])
inter_name = Button(root, text="PLAY", width=15, font=("Comic Sans MS", 12, "bold"))
inter_name.pack(side=TOP)
inter_name.bind('<Button-1>', name_entry)
winners = ""
#for s in range(len(players[:3])):
if len(players[:3]) == 1:
    winners = f'1. {players[0]}'
elif len(players[:3]) == 2:
    winners = f'''1. {players[0]}
2.  {players[1]}'''
elif len(players[:3]) == 3:
    winners = f'''1. {players[0]}
2.  {players[1]}
3.  {players[2]}'''
print(players[0][0])
print(players[0][1])
print(players[0][-1])
winners_table = Label(root, text=winners, width=20, height=5, bg='green', fg='black', font=("Comic Sans MS", 12, "bold"))
winners_table.pack(side=TOP)

root.mainloop()

clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    click()
    if len(rockets) < 5:
        rocket = Rocket()
        rockets.add(rocket)
        score -= 1
    if len(balls) < 5:
        ball = Ball()
        balls.add(ball)
        score -= 1
    rockets.draw(screen)
    balls.draw(screen)
    if bang_rect != [0, 0, 0, 0]:
        surface_bang(bang_rect)
    scoreboard()
    pygame.display.update()
    screen.fill(BLACK)
    rockets.update()
    balls.update()

players[len(players)-1][1] = score
players = sorted(players, key=lambda i: i[1], reverse=True)
with open('victors.txt', 'w') as f:
    for player in players:
#        f.write(str(player))
        print(player, file=f)
f.close()
pygame.quit()
