# sea view
import pygame
from pygame.draw import *

pygame.init()

yellow = [255, 247, 29]
snow = [255, 250, 250]
cloud_border = [230, 230, 230]
black = [0, 0, 0]
whiten = [222, 213, 153]
bluenose = [161, 245, 255]
aqua = [68, 35, 223]
brown = [186, 80, 5]
tomato = [244, 81, 81]
gold = [224, 238, 12]
coral = [227, 130, 25]
stripes_ship = [163, 72, 47]
sail_outline = [185, 178, 128]
lines_umbrella = [216, 72, 72]

width = 600
height = 400
xc0 = 0.25*width
yc0 = 0.1*height
rc = 0.03*height
nc = 7

FPS = 30
screen = pygame.display.set_mode((width, height))

rect(screen, bluenose, [0, 0, width, 0.45*height])
rect(screen, aqua, [0, 0.45*height, width, 0.2*height])
rect(screen, gold, [0, 0.65*height, width, 0.35*height])
circle(screen, yellow, [0.9*width, 0.15*height], 0.09*height)

# clouds
xy_cloud = ([xc0, yc0], [xc0+rc, yc0], [xc0-rc, yc0+rc], [xc0+0.25*rc, yc0+1.1*rc],
            [xc0+1.5*rc, yc0+1.2*rc], [xc0+2*rc, yc0], [xc0+2.5*rc, yc0+rc])
for n in xy_cloud:
    circle(screen, snow, n, rc)
    circle(screen, cloud_border, n, rc, 2)

#boat
rect(screen, brown, [0.6*width, 0.5*height, 0.25*width, 0.07*height])
polygon(screen, brown, [[0.85*width, 0.5*height], [0.95*width, 0.5*height],
                        [0.85*width, 0.57*height]])
circle(screen, brown, [0.6*width, 0.5*height], 0.07*height, draw_bottom_left=True)
line(screen, stripes_ship, [0.6*width, 0.5*height], [0.6*width, 0.57*height], 1)
line(screen, stripes_ship, [0.85*width, 0.5*height], [0.85*width, 0.57*height], 1)
line(screen, black, [0.65*width, 0.5*height], [0.65*width, 0.3*height], int(width/110))
circle(screen, snow, [0.87*width, 0.525*height], 0.022*height)
circle(screen, black, [0.87*width, 0.525*height], 0.022*height, 3)
polygon(screen, whiten, ([0.655*width, 0.5*height], [0.75*width, 0.4*height],
        [0.655*width, 0.3*height], [0.68*width, 0.4*height]))
polygon(screen, sail_outline, ([0.655*width, 0.5*height], [0.75*width, 0.4*height],
        [0.655*width, 0.3*height], [0.68*width, 0.4*height]), 2)
line(screen, sail_outline, [0.68*width, 0.4*height], [0.75*width, 0.4*height], 2)

# umbrella
line(screen, coral, [0.15*width, 0.55*height], [0.15*width, 0.95*height], int(width/110))
polygon(screen, tomato, [[0.145*width, 0.55*height], [0.05*width, 0.61*height],
        [0.26*width, 0.61*height], [0.155*width, 0.55*height]])
line(screen, stripes_ship, [0.146*width, 0.55*height], [0.146*width, 0.61*height], 1)
line(screen, stripes_ship, [0.155*width, 0.55*height], [0.155*width, 0.61*height], 1)
xy_top = ([0.146*width, 0.0675*width], [0.155*width, 0.1725*width])
step = 0.03
for xt, xb in xy_top:
    for i in range(3):
        line(screen, lines_umbrella, [xt, 0.55*height],
        [xb + i*step*width, 0.61*height], 3)



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()