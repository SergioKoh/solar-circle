import pygame
from pygame.draw import *

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
size = [400, 400]
FPS = 30
center = [size[0]/2, size[1]/2]
smiley = 100
mouth = [50, 100, 15]

screen = pygame.display.set_mode(size)
screen.fill(GREY)

circle(screen, YELLOW, center, smiley)
circle(screen, BLACK, center, smiley, 1)
rect(screen, BLACK, [center[0]-mouth[1]/2, center[1]+mouth[0], mouth[1], mouth[2]],
     border_radius=int(mouth[2]/2))

er = smiley/5
em = er/1.5
eyes = ([[center[0] - mouth[1] / 2, center[1] - mouth[0] / 2], er],
        [[center[0] + mouth[1] / 2, center[1] - mouth[0] / 2], em])
eye = ([RED, 0, 1], [BLACK, 1, 1], [BLACK, 0, 3])
for i in eyes:
    for j in eye:
        circle(screen, j[0], i[0], i[1]/j[2], j[1])

line(screen, BLACK, [100, 120], [180, 165], 10)
line(screen, BLACK, [220, 165], [300, 140], 10)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
