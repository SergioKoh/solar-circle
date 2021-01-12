# refactoring sea view
import pygame
from pygame.draw import *

pygame.init()

width = 1200
height = 800
FPS = 30
x, y = 0, 0
width_landscape, height_landscape = width, height
white = (255, 255, 255)
black = (0, 0, 0)
snow = (255, 250, 250)
x1 = 0.22 * width
y1 = 0.12 * height
x2 = 0.5 * width
y2 = 0.16 * height
r = 0.04 * min(height, width)
x3 = 0.59 * width

def draw_porthole(x, y, r, color=snow, color_border=black ):
    """
    Function draws the porthole of the ship
    x, y - coordinates of the center of the porthole on the bow of the ship
    r - porthole radius
    color - porthole color
    color_border - porthole outline color
    """
    circle(screen, snow, (x, y), r)
    circle(screen, black, (x, y), r, 3)


def draw_hull(x, y, width, height, bow_length, color=(186, 80, 5), color_stripes=(163, 72, 47)):
    """
    Function draws the hull of the ship
    x, y - coordinates of the upper left corner of the hull without stern
    width, height - hull of the ship width, height
    color - hull color
    color_stripes - stripes color
    """
    rect(screen, color, (x, y, width, height))
    polygon(screen, color, ((x+width, y), (x + width + bow_length, y),
                            (x + width, y + height)))
    circle(screen, color, (x, y), height, draw_bottom_left=True)
    line(screen, color_stripes, (x, y), (x, y + height), 1)
    line(screen, color_stripes, (x + width, y), (x+width, y+height), 1)

    draw_porthole(x + width + 0.25*bow_length, y+0.39*height, 0.32*height)


def draw_rigs(x, y, width, height, width_sail, color=black,
              color_sail=(222, 213, 153), color_outline=(185, 178, 128)):
    """
    Function draws the rigs of the ship
    x, y - coordinates of the upper left corner of the mast
    width, height - width and height of the mast
    width_sail - sail width
    color - mast color
    """
    rect(screen, color, (x, y, width, height))
    polygon(screen, color_sail, ((x + width, y), (x + width + width_sail, y + 0.5*height),
            (x + width, y + 0.96*height), (x + width + 0.25*width_sail, y + 0.5*height)))
    polygon(screen, color_outline, ((x + width, y), (x + width + width_sail, y + 0.5*height),
            (x + width, y + 0.96*height), (x + width + 0.25*width_sail, y + 0.5*height)), 2)
    line(screen, color_outline, (x + width + 0.25*width_sail, y + 0.5*height),
         (x + width + width_sail, y + 0.5*height), 2)


def draw_sun(x, y, r, color=(255, 247, 29)):
    """
    Function draws sun on screen.
    x, y - coordinates center of the sun
    r - sun radius
    color - sun color
    """
    circle(screen, color, (x, y), r)


def draw_cloud(x, y, r, color=snow, color_border=(230, 230, 230)):
    """
    Function draws cloud on screen.
    x, y - coordinates of the center of the upper left circle
    color - cloud color
    color_border - circle border color
    """

    xy_cloud = ((x, y), (x + r, y), (x - r, y + r), (x + 0.25 * r, y + 1.1 * r),
                (x + 1.6 * r, y + 1.2 * r), (x + 2.1 * r, y), (x + 2.6 * r, y + r))
    for n in xy_cloud:
        circle(screen, color, n, r)
        circle(screen, color_border, n, r, 2)


def draw_boat(x, y, width, height, bow_length):
    """
    Function draws boat on screen.
    x, y - coordinates of the upper left corner of the boat without stern
    width, height - length and height of the ship without stern and bow
    bow_length - bow length
    color - boat color
    """

    draw_hull(x, y, width, height, bow_length)
    draw_rigs(x + 0.4*width, y - 3*height, 0.05*width, 3*height, 0.4*width)


def draw_umbrella(x, y, width, height, width_umbrella, height_umbrella,color=(227, 130, 25),
              color_umbrella=(244, 81, 81), color_outline=(163, 72, 47)):
    """
    Function draws umbrella on screen.
    x, y - the coordinates of the top of the umbrella
    color - umbrella color
    """
    rect(screen, color, (x, y, width, height))
    polygon(screen, color_umbrella, ((x, y), (x - 0.5*width_umbrella, y+height_umbrella),
                    (x + 0.5*width_umbrella + width, y+height_umbrella), (x + width, y)))
    line(screen, color_outline, (x, y), (x, y + height), 1)
    line(screen, color_outline, (x + width, y), (x + width, y + height), 1)
    xy_top = ((x, x - 0.4 * width_umbrella), (x + width, x + width + 0.1 * width_umbrella))
    step = 0.15
    for xt, xb in xy_top:
        for i in range(3):
            aaline(screen, color_outline, (xt, y),
                 (xb + i * step * width_umbrella, y + height_umbrella))


def draw_background(x, y, width, height, color=(161, 245, 255)):
    """
    Function draws background on screen.
    x, y - coordinates of the upper left corner of the background
    width_background, height_background - background width and height
    color - background color
    """
    rect(screen, color, (x, y, width, height))
    draw_sun(0.89*width, 0.3*height, 0.21*min(height, width))


def draw_middleground(x, y, width, height, color=(68, 35, 223)):
    """
    Function draws middleground on screen.
    x, y - coordinates of the upper left corner of the middleground
    width, height - middleground width and height
    color - middleground color
    """
    rect(screen, color, (x, y, width, height))


def draw_foreground(x, y, width, height, color=(224, 238, 12)):
    """
    Function draws foreground on screen.
    x, y - coordinates of the upper left corner of the foreground
    width_foreground, height_foreground - foreground width and height
    color - foreground color
    """
    rect(screen, color, (x, y, width, height))
    draw_umbrella(0.4 * width, y - 0.3*height, 0.011 * width,
                  1.1 * height, 0.22 * width, 0.25*height)

def draw_landscape(x, y, width, height):
    """
    Function draws landscape on screen.
    x, y - coordinates of the upper left corner of the image
    width, height - image width and height

    """
    height_b = height * 0.46
    height_m = height * 0.24
    height_f = height - height_b - height_m
    y_m = y + height_b
    y_f = y_m + height_m
    draw_background(x, y, width, height_b)
    draw_middleground(x, y_m, width, height_m)
    draw_foreground(x, y_f, width, height_f)


screen = pygame.display.set_mode((width, height))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    draw_landscape(x, y, width_landscape, height_landscape)
    draw_cloud(x1, y1, r)
    draw_cloud(x2, y2, r, black)
    draw_boat(x3, 0.5 * height, 0.24 * width, 0.1 * height, 0.1 * width)
    pygame.display.update()
    if x1 >= width + r:
        # перемещаем его за левую
        x1 = -4*r
    elif x2 >= width + r:
        x2 = -4*r
    elif x3 >= width + 0.1 * height:
        x3 = -0.33 * width
    else:  # Если еще нет,
        # на следующей итерации цикла
        # круг отобразится немного правее
        x1 += 0.5
        x2 += 2
        x3 += 1
pygame.quit()
